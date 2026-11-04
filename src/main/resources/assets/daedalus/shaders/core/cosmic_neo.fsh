#version 150

#define M_PI 3.1415926535897932384626433832795

const int cosmiccount = 10;
const int cosmicoutof = 81;
const float lightmix = 1.5f;

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;

uniform float time;

uniform float yaw;
uniform float pitch;
uniform float externalScale;

uniform float opacity;

uniform mat2 cosmicuvs[cosmiccount];

uniform int useCosmicType;
uniform vec4 cosmicColor0;

uniform vec2 screenSize;

in float vertexDistance;
in vec2 texCoord0;
in vec3 fPos;

out vec4 fragColor;

// --- 辅助函数 ---

vec4 linear_fog(vec4 inColor, float vertexDistance, float fogStart, float fogEnd, vec4 fogColor) {
    if (vertexDistance <= fogStart) {
        return inColor;
    }
    float fogValue = vertexDistance < fogEnd ? smoothstep(fogStart, fogEnd, vertexDistance) : 1.0;
    return mix(inColor, fogColor, fogValue * fogColor.a);
}

vec3 applyCamera(vec3 pos, float yaw, float pitch) {
    float sp = sin(pitch);
    float cp = cos(pitch);
    vec3 p = vec3(pos.x, pos.y * cp - pos.z * sp, pos.y * sp + pos.z * cp);
    float sy = sin(-yaw);
    float cy = cos(-yaw);
    return vec3(p.z * sy + p.x * cy, p.y, p.z * cy - p.x * sy);
}

// HSB 转 RGB
vec3 hsb2rgb(vec3 c) {
    vec3 rgb = clamp(abs(mod(c.x * 6.0 + vec3(0.0, 4.0, 2.0), 6.0) - 3.0) - 1.0, 0.0, 1.0);
    rgb = rgb * rgb * (3.0 - 2.0 * rgb);
    return c.z * mix(vec3(1.0), rgb, c.y);
}

// --- 噪声算法 ---
vec3 hash3(vec3 p) {
    p = fract(p * 0.3183099 + vec3(0.1, 0.2, 0.3));
    p *= 17.0;
    return fract(p * (p.x + p.y + p.z)) * 2.0 - 1.0;
}

float perlinNoise(vec3 p) {
    vec3 i = floor(p);
    vec3 f = fract(p);
    vec3 u = f * f * (3.0 - 2.0 * f);
    float n000 = dot(hash3(i + vec3(0.0, 0.0, 0.0)), f - vec3(0.0, 0.0, 0.0));
    float n100 = dot(hash3(i + vec3(1.0, 0.0, 0.0)), f - vec3(1.0, 0.0, 0.0));
    float n010 = dot(hash3(i + vec3(0.0, 1.0, 0.0)), f - vec3(0.0, 1.0, 0.0));
    float n110 = dot(hash3(i + vec3(1.0, 1.0, 0.0)), f - vec3(1.0, 1.0, 0.0));
    float n001 = dot(hash3(i + vec3(0.0, 0.0, 1.0)), f - vec3(0.0, 0.0, 1.0));
    float n101 = dot(hash3(i + vec3(1.0, 0.0, 1.0)), f - vec3(1.0, 0.0, 1.0));
    float n011 = dot(hash3(i + vec3(0.0, 1.0, 1.0)), f - vec3(0.0, 1.0, 1.0));
    float n111 = dot(hash3(i + vec3(1.0, 1.0, 1.0)), f - vec3(1.0, 1.0, 1.0));
    return mix(mix(mix(n000, n100, u.x), mix(n010, n110, u.x), u.y), mix(mix(n001, n101, u.x), mix(n011, n111, u.x), u.y), u.z);
}

float perlinNoiseOctaves(vec3 p, int octaves, float persistence, float contrast) {
    float total = 0.0;
    float amplitude = 1.0;
    float frequency = 1.0;
    float maxValue = 0.0;
    for (int i = 0; i < 8; i++) {
        if (i >= octaves) break;
        total += perlinNoise(p * frequency) * amplitude;
        maxValue += amplitude;
        amplitude *= persistence;
        frequency *= 2.0;
    }
    float n = total / maxValue * 0.5 + 0.5;
    n = (n - 0.5) * contrast + 0.5;
    return clamp(n, 0.0, 1.0);
}

vec3 blend3BW(vec3 dark, vec3 mid, vec3 midAlt, vec3 bright, float n, vec2 uv, float time) {
    vec3 blobPos = vec3(uv * 0.4, time * 0.02);
    float blobNoise = perlinNoise(blobPos) * 0.5 + 0.5;
    blobNoise = smoothstep(0.35, 0.65, blobNoise);
    vec3 midMix = mix(mid, midAlt, blobNoise);
    float t1 = smoothstep(0.2, 0.5, n);
    float t2 = smoothstep(0.2, 1.0, n);
    vec3 col1 = mix(dark, midMix, t1);
    vec3 col2 = mix(midMix, bright, t2);
    vec3 tint = mix(col1, col2, n);
    return mix(vec3(n), tint, 1.0);
}

vec3 galaxy(vec2 fragCoord, float mult, float speed, vec2 res, float time) {
    vec2 uv = fragCoord * mult;
    float tSpeed = speed < 3.0 ? speed * 3.0 : speed;
    vec3 p = vec3(uv + time / speed, time / tSpeed);
    float n = 1.0 - abs(perlinNoiseOctaves(p * 0.15, 8, 0.6, 4.0));
    n = pow(n, 2.0);
    return blend3BW(vec3(0.0, 0.0, 0.1), vec3(0.4, 0.0, 0.6), vec3(0.2, 0.0, 0.6), vec3(1.6, 1.0, 1.6), n, uv, time);
}

void main(void)
{
    vec4 mask = texture(Sampler0, texCoord0.xy);
    vec4 col = vec4(0.0, 0.0, 0.0, 1.0);

    if (useCosmicType == 14) {
        // 1. 坐标计算
        vec2 uv = (gl_FragCoord.xy / screenSize) * 2.0 - 1.0;
        uv.x *= screenSize.x / screenSize.y;
        vec3 rayDir = normalize(vec3(uv, 1.0));
        vec3 viewDir = applyCamera(rayDir, yaw, pitch);
        vec2 galaxyUV = viewDir.xy * 2.0;

        // 2. 生成基础星系纹理 (黑白/单色)
        // 这里我们只取 galaxy 函数的亮度信息，或者将其视为灰度图
        vec3 galaxyBase = galaxy(galaxyUV * 500.0, 0.01, 0.5, screenSize, time);
        galaxyBase += galaxy(galaxyUV * 800.0 + 100.0, 0.005, 3.0, screenSize, time) * 0.5;

        // 提取亮度
        float brightness = dot(galaxyBase, vec3(0.33, 0.33, 0.33));

        // 3. 生成动态彩虹色
        // 基于坐标和时间生成色相 (Hue)
        float hue = (galaxyUV.x * 0.5 + galaxyUV.y * 0.5 + time * 0.1);
        // 添加一些噪声扰动，让颜色分布更自然
        hue += perlinNoise(vec3(galaxyUV * 5.0, time * 0.05)) * 0.2;

        // 转换为 RGB (饱和度 0.8，亮度 1.0)
        vec3 rainbowColor = hsb2rgb(vec3(hue, 0.8, 1.0));

        // 4. 混合
        // 用彩虹色给星系纹理上色，并保留高光 (brightness > 0.8 的部分趋向于白色)
        col.rgb = mix(rainbowColor * brightness, vec3(1.0), smoothstep(0.8, 1.2, brightness));

        // 整体增亮
        col.rgb *= 1.5;
    }
    else {
        col = cosmicColor0;
    }

    col.rgb *= lightmix;
    col.a *= mask.r * opacity;
    col = clamp(col, 0.0, 1.0);
    fragColor = linear_fog(col, vertexDistance, FogStart, FogEnd, FogColor);
}
