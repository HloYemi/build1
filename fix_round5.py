#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 23: 使用 halo_cosmic 为物品栏叠加"光晕+星空"双层特效
"""
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
RES = P / "src/main/resources"

print("=" * 60)
print("Round 23: 为物品栏叠加 光晕 + 星空 双层")
print("=" * 60)

def write(rel, content):
    p = RES / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[写入] {rel}")

# 1. 爱之诗剑：光晕（蓝色，呼吸脉冲）+ 星空
write("assets/daedalus/models/item/love_poem_sword.json", """{
  "parent": "minecraft:item/handheld",
  "textures": {
    "layer0": "daedalus:item/love_poem_sword",
    "halo_tex": "daedalus:item/love_poem_sword"
  },
  "loader": "renderblender:halo_cosmic",
  "halo": {
    "texture": "halo_tex",
    "color": 2003199,
    "size": 1.0,
    "pulse": true
  },
  "cosmic": {
    "mask": "daedalus:item/love_poem_sword"
  }
}
""")

# 2. 附魔书：金色光晕（呼吸脉冲）+ 星空
write("assets/minecraft/models/item/enchanted_book.json", """{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "minecraft:item/enchanted_book",
    "halo_tex": "minecraft:item/enchanted_book"
  },
  "loader": "renderblender:halo_cosmic",
  "halo": {
    "texture": "halo_tex",
    "color": 16766720,
    "size": 1.0,
    "pulse": true
  },
  "cosmic": {
    "mask": "minecraft:item/enchanted_book"
  }
}
""")

# 3. 清理 Daedalus 自带的那份附魔书模型（如果存在），避免它被当作另一个物品渲染
book_alt = RES / "assets/daedalus/models/item/daedalus_enchanted_book.json"
if book_alt.exists():
    book_alt.write_text("""{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "daedalus:item/daedalus_enchanted_book",
    "halo_tex": "daedalus:item/daedalus_enchanted_book"
  },
  "loader": "renderblender:halo_cosmic",
  "halo": {
    "texture": "halo_tex",
    "color": 16766720,
    "size": 1.0,
    "pulse": true
  },
  "cosmic": {
    "mask": "daedalus:item/daedalus_enchanted_book"
  }
}
""", encoding="utf-8")
    print("[写入] daedalus_enchanted_book.json（同步为 halo_cosmic）")

print("\n下一步:")
print("  git add .")
print('  git commit -m "feat: use halo_cosmic for GUI double-layer effect"')
print("  git push")