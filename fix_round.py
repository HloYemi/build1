#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 11: 直接使用 RenderBlender 原生的 cosmic loader，恢复特效
"""
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
RES = P / "src/main/resources"

print("=" * 60)
print("Round 11: 使用 RenderBlender 原生 Loader 恢复特效")
print("=" * 60)

def write(rel, content):
    p = RES / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[写入] {rel}")

# 1. 修改爱之诗剑的模型（使用 handheld 并加上 cosmic 和光晕）
write("assets/daedalus/models/item/love_poem_sword.json", """{
  "parent": "minecraft:item/handheld",
  "textures": {
    "layer0": "daedalus:item/love_poem_sword",
    "halo_tex": "daedalus:item/love_poem_sword_mask"
  },
  "loader": "renderblender:halo_cosmic",
  "halo": {
    "texture": "halo_tex",
    "color": 2003199,
    "size": 1.0,
    "pulse": true
  },
  "cosmic": {
    "mask": "daedalus:item/love_poem_sword_mask"
  }
}
""")

# 2. 修改附魔书的模型（覆盖原版，加上 cosmic）
write("assets/minecraft/models/item/enchanted_book.json", """{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "minecraft:item/enchanted_book"
  },
  "loader": "renderblender:cosmic",
  "cosmic": {
    "mask": "daedalus:item/daedalus_enchanted_book_mask"
  }
}
""")

print("\n下一步:")
print("  git add .")
print('  git commit -m "feat: use renderblender native loaders for cosmic effect"')
print("  git push")