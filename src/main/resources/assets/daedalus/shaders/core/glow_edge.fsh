#version 150

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;
uniform vec4 uColor;
uniform int uType;
uniform vec2 screenSize;
uniform float time;
uniform float yaw;
uniform float pitch;

in vec4 vertexColor;
in vec2 texCoord0;

out vec4 fragColor;

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
    vec2 viewOffset = vec2(yaw, pitch) * 500.0;
    vec2 uv = (fragCoord + viewOffset) * mult;
    float tSpeed = speed < 3.0 ? speed * 3.0 : speed;
    vec3 p = vec3(uv + time / speed, time / tSpeed);

    float n = 1.0 - abs(perlinNoiseOctaves(p * 0.15, 8, 0.6, 4.0));
    n = pow(n, 2.0);

    return blend3BW(vec3(0.0, 0.0, 0.1), vec3(0.4, 0.0, 0.6), vec3(0.2, 0.0, 0.6), vec3(1.6, 1.0, 1.6), n, uv, time);
}

void main() {
    vec4 color = texture(Sampler0, texCoord0);

    if (color.a < 0.1) discard;

    if (uType == 1) {
        vec2 fragCoord = gl_FragCoord.xy;
        vec3 galaxyColor = galaxy(fragCoord, 0.03, 0.5, screenSize, time) / 4.0 + galaxy(fragCoord, 0.01, 3.0, screenSize, time);
        fragColor = vec4(galaxyColor * uColor.rgb, 1.0);
    } else {
        fragColor = uColor;
    }
}
