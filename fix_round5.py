#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 24: 优化“神圣”主题的渐变色，拉开对比度
"""
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
theme_file = P / "src/main/java/com/kzjy/daedalus/enchantment/util/EnchantmentTheme.java"

if not theme_file.exists():
    print("[错误] 找不到 EnchantmentTheme.java")
    exit(1)

c = theme_file.read_text(encoding="utf-8")

# 原来的：DIVINE("神圣", 0xFFD700, 0xFFEA00, ChatFormatting.YELLOW),
# 修改为：金色 -> 纯白色，增强圣光感
old_divine = 'DIVINE("神圣", 0xFFD700, 0xFFEA00, ChatFormatting.YELLOW),'
new_divine = 'DIVINE("神圣", 0xFFD700, 0xFFFFFF, ChatFormatting.YELLOW),'

if old_divine in c:
    c = c.replace(old_divine, new_divine)
    print("[修改] DIVINE 主题：0xFFEA00 (亮黄) -> 0xFFFFFF (纯白)")
elif new_divine in c:
    print("[跳过] DIVINE 主题已是最新")
else:
    print("[警告] 未找到 DIVINE 主题的原始定义，请检查文件")

theme_file.write_text(c, encoding="utf-8")

print("\n下一步:")
print("  git add .")
print('  git commit -m "style: improve DIVINE theme gradient to gold-white"')
print("  git push")