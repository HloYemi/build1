#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daedalus NeoForge 1.21.1 - fix_round.py
当前轮次: Round 9
修复: Style import 缺失 (Round 8 用了 MutableComponent 做锚点但文件里没有那行)
方案: 改用 UnaryOperator 版本的 withStyle，不依赖 Style 类型
"""
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
TARGET = P / "src/main/java/com/kzjy/daedalus/client/DaedalusForgeClientEvents.java"

if not TARGET.exists():
    print(f"[错误] 找不到: {TARGET}")
    raise SystemExit(1)

c = TARGET.read_text(encoding="utf-8")

# 1. 清理可能残留的 Style import（如果 Round 8 加了但加错位置）
c = c.replace("import net.minecraft.network.chat.Style;\n", "")

# 2. 替换 Style.EMPTY 用法为 UnaryOperator<Style> 版本
old = '''                        FormattedText styled = Component.literal(line)
                                .withStyle(Style.EMPTY.withColor(primaryColor));
                        event.getTooltipElements().set(i, Either.left(styled));'''

new = '''                        FormattedText styled = Component.literal(line)
                                .withStyle(s -> s.withColor(primaryColor));
                        event.getTooltipElements().set(i, Either.left(styled));'''

if old not in c:
    print("[警告] 未找到预期代码块，打印当前含 primaryColor 的行:")
    for i, line in enumerate(c.splitlines(), 1):
        if "primaryColor" in line:
            print(f"  第 {i} 行: {line}")
    raise SystemExit(1)

c = c.replace(old, new)
TARGET.write_text(c, encoding="utf-8")
print("[修改] DaedalusForgeClientEvents.java: Style.EMPTY → lambda")

print("\n" + "=" * 60)
print("Round 9 修复完成")
print("=" * 60)
print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: use UnaryOperator lambda instead of Style.EMPTY"')
print("  git push")