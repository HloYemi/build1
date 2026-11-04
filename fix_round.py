#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 18: 删除残留的 DaedalusGlowRenderer 以修复编译错误
"""
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SRC = P / "src/main/java/com/kzjy/daedalus"

print("=" * 60)
print("Round 18: 清理残留的自定义渲染类")
print("=" * 60)

# 1. 删除依赖已废弃 DaedalusRenderTypes 的类
glow = SRC / "client/renderer/DaedalusGlowRenderer.java"
if glow.exists():
    glow.unlink()
    print(f"[删除] {glow.relative_to(P)}")

# 2. 检查是否还有别的引用（简单扫一下）
for java_file in SRC.rglob("*.java"):
    c = java_file.read_text(encoding="utf-8")
    if "DaedalusGlowRenderer" in c or "DaedalusRenderTypes" in c:
        print(f"[警告] {java_file.name} 中仍有引用残留！")

print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: remove DaedalusGlowRenderer to fix missing RenderTypes"')
print("  git push")