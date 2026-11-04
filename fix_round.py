#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daedalus NeoForge 1.21.1 - fix_round.py
当前轮次: Round 8
修复: 创造物品栏悬停 Daedalus 附魔书时 tooltip 崩溃 (IndexOutOfBoundsException)
机制: CreativeModeInventoryScreen 依赖 tooltip 中至少 1 个 Either.left(FormattedText)，
      我们替换成 Either.right(DaedalusTooltipData) 后会破坏这个假设。
      修复: 在创造物品栏场景下降级为静态样式 (Either.left + withStyle)，保留原版结构；
           其它场景仍用动态组件 (Either.right) 保留渐变效果。
"""
import re
from pathlib import Path

P = Path(r"D:\AAA.Download\Daedalus_Enchantment-main")
SRC = P / "src" / "main" / "java" / "com" / "kzjy" / "daedalus"
TARGET = SRC / "client" / "DaedalusForgeClientEvents.java"

if not TARGET.exists():
    print(f"[错误] 找不到: {TARGET}")
    raise SystemExit(1)

c = TARGET.read_text(encoding="utf-8")

# 1. 添加 import
if "import net.minecraft.client.gui.screens.inventory.CreativeModeInventoryScreen;" not in c:
    c = c.replace(
        "import net.minecraft.client.gui.screens.Screen;",
        "import net.minecraft.client.gui.screens.Screen;\nimport net.minecraft.client.gui.screens.inventory.CreativeModeInventoryScreen;"
    )
if "import net.minecraft.network.chat.Style;" not in c:
    c = c.replace(
        "import net.minecraft.network.chat.MutableComponent;",
        "import net.minecraft.network.chat.MutableComponent;\nimport net.minecraft.network.chat.Style;"
    )

# 2. 替换附魔书的 tooltip 逻辑：条件降级
old_block = '''            for (int i = 0; i < event.getTooltipElements().size(); i++) {
                var el = event.getTooltipElements().get(i);
                if (el.left().isEmpty()) continue;
                String line = el.left().get().getString();
                boolean isTitle = line.contains(base);
                boolean isDesc = !full.isEmpty() && !isTitle && full.contains(line.trim()) && line.trim().length() > 4;
                if (isTitle || isDesc)
                    event.getTooltipElements().set(i, Either.right(new DaedalusTooltipData(
                            Component.literal(line), theme, -1, true)));
            }'''

new_block = '''            boolean inCreativeInventory = Minecraft.getInstance().screen instanceof CreativeModeInventoryScreen;
            int primaryColor = theme.getPrimaryColor();
            for (int i = 0; i < event.getTooltipElements().size(); i++) {
                var el = event.getTooltipElements().get(i);
                if (el.left().isEmpty()) continue;
                String line = el.left().get().getString();
                boolean isTitle = line.contains(base);
                boolean isDesc = !full.isEmpty() && !isTitle && full.contains(line.trim()) && line.trim().length() > 4;
                if (isTitle || isDesc) {
                    if (inCreativeInventory) {
                        // 创造物品栏: 必须保留 Either.left(FormattedText) 结构，
                        // 否则 CreativeModeInventoryScreen 在 index 1 处 add 附魔名列表会越界
                        FormattedText styled = Component.literal(line)
                                .withStyle(Style.EMPTY.withColor(primaryColor));
                        event.getTooltipElements().set(i, Either.left(styled));
                    } else {
                        // 普通背包/容器: 动态渐变组件
                        event.getTooltipElements().set(i, Either.right(new DaedalusTooltipData(
                                Component.literal(line), theme, -1, true)));
                    }
                }
            }'''

if old_block not in c:
    print("[警告] 未找到预期的附魔书 tooltip 代码块，请手工检查")
    # 尝试打印当前文件里含 'isTitle || isDesc' 的上下文
    for i, line in enumerate(c.splitlines(), 1):
        if "isTitle" in line and "isDesc" in line:
            print(f"  第 {i} 行: {line.strip()}")
    raise SystemExit(1)

c = c.replace(old_block, new_block)
TARGET.write_text(c, encoding="utf-8")
print("[修改] DaedalusForgeClientEvents.java (创造物品栏 tooltip 降级为静态)")

print("\n" + "=" * 60)
print("Round 8 修复完成")
print("=" * 60)
print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: downgrade enchantment book tooltip to static in CreativeModeInventoryScreen"')
print("  git push")