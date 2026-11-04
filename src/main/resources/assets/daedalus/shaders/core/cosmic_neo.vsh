#version 150

in vec3 Position;
in vec4 Color;
in vec2 UV0;
in ivec2 UV2;
in vec3 Normal;

uniform sampler2D Sampler2;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;
uniform int FogShape;

out float vertexDistance;
out vec4 vertexColor;
out vec2 texCoord0;
out vec3 fPos;

// 手动实现 fog_distance
float fog_distance(mat4 modelViewMat, vec3 pos, int shape) {
    vec4 viewPos = modelViewMat * vec4(pos, 1.0);
    float dist = length(viewPos.xyz);
    return dist;
}

// 手动实现 minecraft_sample_lightmap
vec4 minecraft_sample_lightmap(sampler2D lightMap, ivec2 uv) {
    return texture(lightMap, clamp(uv / 256.0, vec2(0.5 / 16.0), vec2(15.5 / 16.0)));
}

void main() {
    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1.0);
    fPos = (ModelViewMat * vec4(Position, 1.0)).xyz;

    vertexDistance = fog_distance(ModelViewMat, Position, FogShape);
    texCoord0 = UV0;
    // 如果需要 vertexColor (虽然 cosmic_neo.fsh 好像没怎么用)，可以加上
    vertexColor = Color * minecraft_sample_lightmap(Sampler2, UV2);
}
