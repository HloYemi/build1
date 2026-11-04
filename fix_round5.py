#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 25 (修正版): 正确注册图集，修复 mask 缺失导致的正面黑块
"""
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
RES = P / "src/main/resources"

print("=" * 60)
print("Round 25 (修正版): 注册图集并修复 mask 黑块")
print("=" * 60)

def write(rel, content):
    p = RES / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[写入] {rel}")

# 1. 补上缺失的图集声明 blocks.json
# 将 daedalus:item/ 目录下的所有贴图（包括原版没有引用的 mask）加载进 BLOCK_ATLAS
write("assets/daedalus/atlases/blocks.json", """{
  "sources": [
    {
      "type": "minecraft:directory",
      "prefix": "item/",
      "source": "item"
    }
  ]
}
""")

# 2. 剑的模型：保持不变，引用专属 mask
write("assets/daedalus/models/item/love_poem_sword.json", """{
  "parent": "minecraft:item/handheld",
  "textures": {
    "layer0": "daedalus:item/love_poem_sword"
  },
  "loader": "renderblender:cosmic",
  "cosmic": {
    "mask": "daedalus:item/love_poem_sword_mask"
  }
}
""")

# 3. 附魔书的模型：保留原版底图，引用专属 mask（绝对不破坏原版书皮）
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
print('  git commit -m "fix: register atlases/blocks.json for mask texture, keep vanilla book layer0"')
print("  git push")