#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 14: 采用 RenderBlender 标准格式完全替换 Daedalus 模型
"""
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
RES = P / "src/main/resources"

print("=" * 60)
print("Round 14: 使用 RenderBlender 标准格式")
print("=" * 60)

def write(rel, content):
    p = RES / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[写入] {rel}")

# 1. 爱之诗剑：使用 handheld，且使用前置库的 halo_cosmic
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

# 2. 附魔书：使用 generated，且使用前置库的 cosmic
write("assets/minecraft/models/item/enchanted_book.json", """{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "daedalus:item/daedalus_enchanted_book",
    "halo_tex": "daedalus:item/daedalus_enchanted_book_mask"
  },
  "loader": "renderblender:cosmic",
  "cosmic": {
    "mask": "daedalus:item/daedalus_enchanted_book_mask"
  }
}
""")

print("\n下一步:")
print("  git add .")
print('  git commit -m "feat: use official RenderBlender JSON format for effects"')
print("  git push")