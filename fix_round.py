#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 16: 移除导致黑块的 Shader 特效，恢复纯净贴图
"""
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
RES = P / "src/main/resources"

print("=" * 60)
print("Round 16: 剥离 Shader，恢复纯净贴图")
print("=" * 60)

def write(rel, content):
    p = RES / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[写入] {rel}")

# 1. 剑：去掉所有 loader 和特效，只保留纯贴图
write("assets/daedalus/models/item/love_poem_sword.json", """{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "daedalus:item/love_poem_sword"
  }
}
""")

# 2. 附魔书：恢复原版材质和纯贴图
write("assets/minecraft/models/item/enchanted_book.json", """{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "minecraft:item/enchanted_book"
  }
}
""")

print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: strip shader to prevent black item models"')
print("  git push")