#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daedalus NeoForge 1.21.1 - Round 5
修复最后 2 个错误
"""
import re
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SRC = P / "src" / "main" / "java" / "com" / "kzjy" / "daedalus"

# =====================================================================
# 1. DaedalusEvents.java: Event.Result.DENY → TriState.FALSE
#    （TriState 在 NeoForge 1.21.1 中位于 net.neoforged.neoforge.common）
# =====================================================================
ev = SRC / "event" / "DaedalusEvents.java"
c = ev.read_text(encoding="utf-8")
c = c.replace(
    "event.setResult(net.neoforged.bus.api.Event.Result.DENY);",
    "event.setResult(net.neoforged.neoforge.common.TriState.FALSE);"
)
ev.write_text(c, encoding="utf-8")
print("[修改] DaedalusEvents.java: Event.Result.DENY → TriState.FALSE")

# =====================================================================
# 2. DaedalusGlowRenderer.java: setNormal(Matrix3f, ...) → setNormal(float, float, float)
#    去掉 Matrix3f 参数，改用三参数版本
# =====================================================================
gr = SRC / "client" / "renderer" / "DaedalusGlowRenderer.java"
c = gr.read_text(encoding="utf-8")

# 替换 addVertexWithColor 方法：去掉 Matrix3f 参数
old_method_re = re.compile(
    r'private static void addVertexWithColor\(VertexConsumer vertexConsumer, Matrix4f matrix, Matrix3f normal, float x, float y, float z, float u, float v, int r, int g, int b, int alpha\) \{.*?\n    \}',
    re.DOTALL
)
new_method = '''private static void addVertexWithColor(VertexConsumer vertexConsumer, Matrix4f matrix, float x, float y, float z, float u, float v, int r, int g, int b, int alpha) {
        vertexConsumer.addVertex(matrix, x, y, z)
                .setColor(r, g, b, alpha)
                .setUv(u, v)
                .setOverlay(OverlayTexture.NO_OVERLAY)
                .setLight(LightTexture.FULL_BRIGHT)
                .setNormal(0.0F, 1.0F, 0.0F);
    }'''
if old_method_re.search(c):
    c = old_method_re.sub(new_method, c)
    print("[修改] DaedalusGlowRenderer.addVertexWithColor 方法签名")
else:
    print("[警告] 未找到 addVertexWithColor 方法，请手工检查")

# 所有调用处去掉 normal 参数
# 原调用：addVertexWithColor(vertexConsumer, matrix, normal, x, y, z, u, v, r, g, b, alpha)
c = re.sub(
    r'addVertexWithColor\(vertexConsumer, matrix, normal, ',
    'addVertexWithColor(vertexConsumer, matrix, ',
    c
)

# 移除不再使用的 Matrix3f 变量声明（如果报"unused"警告，保留也问题不大）
# renderRingWave 和 renderGlowRay 里的 `Matrix3f normal = poseStack.last().normal();` 保留无副作用

# 确保 import 存在
if "import net.minecraft.client.renderer.LightTexture;" not in c:
    c = c.replace(
        "import net.minecraft.client.renderer.MultiBufferSource;",
        "import net.minecraft.client.renderer.MultiBufferSource;\nimport net.minecraft.client.renderer.LightTexture;\nimport net.minecraft.client.renderer.texture.OverlayTexture;"
    )

gr.write_text(c, encoding="utf-8")
print("[修改] DaedalusGlowRenderer.java 调用处")

print("\n" + "=" * 60)
print("Round 5 修复完成")
print("=" * 60)
print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: final 2 errors for NeoForge 1.21.1"')
print("  git push")