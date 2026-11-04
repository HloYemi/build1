#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 19: 彻底清理旧 Loader 引用，强制重写所有模型 JSON
"""
from pathlib import Path
import shutil

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
RES = P / "src/main/resources"

print("=" * 60)
print("Round 19: 修复模型加载失败与黑面问题")
print("=" * 60)

def write(rel, content):
    p = RES / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[写入] {rel}")

# 1. 强制重写附魔书的模型（修复日志中报错的 daedalus_enchanted_book）
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

# 2. 如果模组自己还留了一个特定书本模型，一并重写
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

# 3. 强制重写爱之诗剑的模型
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

# 4. 扫描并清理任何仍然残留旧 loader 的 JSON 文件
for json_file in RES.rglob("*.json"):
    try:
        content = json_file.read_text(encoding="utf-8")
        if "daedalus:cosmic" in content:
            print(f"[警告] 发现残留旧 Loader 的文件: {json_file.relative_to(RES)}")
    except Exception:
        pass

print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: force rewrite models and remove legacy daedalus:cosmic loader"')
print("  git push")