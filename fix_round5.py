#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 21: 配合已修复的 RenderBlender，彻底覆写 Daedalus 模型
"""
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
RES = P / "src/main/resources"

print("=" * 60)
print("Round 21: 强制重写模型，解决残存的 daedalus:cosmic 报错")
print("=" * 60)

def write(rel, content):
    p = RES / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[写入] {rel}")

# 1. 修复日志报错的 daedalus_enchanted_book.json
write("assets/daedalus/models/item/daedalus_enchanted_book.json", """{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "daedalus:item/daedalus_enchanted_book",
    "mask": "daedalus:item/daedalus_enchanted_book"
  },
  "loader": "renderblender:cosmic",
  "cosmic": { "mask": "mask" }
}
""")

# 2. 修复覆盖原版附魔书的模型
write("assets/minecraft/models/item/enchanted_book.json", """{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "minecraft:item/enchanted_book",
    "mask": "minecraft:item/enchanted_book"
  },
  "loader": "renderblender:cosmic",
  "cosmic": { "mask": "mask" }
}
""")

# 3. 修复爱之诗剑的模型
write("assets/daedalus/models/item/love_poem_sword.json", """{
  "parent": "minecraft:item/handheld",
  "textures": {
    "layer0": "daedalus:item/love_poem_sword",
    "mask": "daedalus:item/love_poem_sword"
  },
  "loader": "renderblender:cosmic",
  "cosmic": { "mask": "mask" }
}
""")

# 4. 扫描清理残留
print("\n[扫描] 检查是否还有残留的 daedalus:cosmic...")
found = False
for json_file in RES.rglob("*.json"):
    c = json_file.read_text(encoding="utf-8")
    if "daedalus:cosmic" in c:
        print(f"[警告] 发现残留: {json_file.relative_to(RES)}")
        c = c.replace('"daedalus:cosmic"', '"renderblender:cosmic"')
        json_file.write_text(c, encoding="utf-8")
        found = True
if not found:
    print("[OK] 没有发现残留。")

print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: force replace legacy loader in models"')
print("  git push")