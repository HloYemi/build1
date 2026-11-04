#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daedalus NeoForge 1.21.1 - fix_round.py
当前轮次: Round 11
修复: 创造物品栏悬停任何带自定义 tooltip 的物品时越界崩溃
根因: CreativeModeInventoryScreen.getTooltipFromContainerItem 会在 tooltip 的 index 1
      处插入附魔名列表，前提是 tooltip 中存在 Either.left(FormattedText) 元素。
      如果我们的自定义渲染把所有 FormattedText 都换成了 Either.right(TooltipComponent)，
      ArrayList.add(1, ...) 就会越界。
方案: 创造物品栏场景下直接 return，让原版 tooltip 逻辑正常运行。
      普通背包/容器仍保留完整特效。
"""
from pathlib import Path

P = Path(r"D:\AAA.Download\Daedalus_Enchantment-main")
TARGET = P / "src/main/java/com/kzjy/daedalus/client/DaedalusForgeClientEvents.java"

if not TARGET.exists():
    print(f"[错误] 找不到: {TARGET}")
    raise SystemExit(1)

c = TARGET.read_text(encoding="utf-8")

# 1. 在 onGatherTooltipComponents 开头插入创造物品栏早退
old_head = '''    @SubscribeEvent
    public static void onGatherTooltipComponents(RenderTooltipEvent.GatherComponents event) {
        ItemStack s = event.getItemStack();'''

new_head = '''    @SubscribeEvent
    public static void onGatherTooltipComponents(RenderTooltipEvent.GatherComponents event) {
        // CreativeModeInventoryScreen.getTooltipFromContainerItem 会在 tooltip 的
        // index 1 处插入附魔名列表，前提是 tooltip 中存在 Either.left(FormattedText) 元素。
        // 我们的自定义渲染会把这些元素全部替换成 Either.right(TooltipComponent)，
        // 导致 ArrayList.add(1, ...) 越界崩溃。创造物品栏场景下直接早退，走原版 tooltip。
        if (Minecraft.getInstance().screen instanceof CreativeModeInventoryScreen) {
            return;
        }
        ItemStack s = event.getItemStack();'''

if old_head not in c:
    print("[警告] 未找到 onGatherTooltipComponents 开头，打印前 20 行含方法的上下文:")
    for i, line in enumerate(c.splitlines(), 1):
        if "onGatherTooltipComponents" in line:
            print(f"  第 {i} 行: {line}")
    raise SystemExit(1)

c = c.replace(old_head, new_head)
print("[修改] onGatherTooltipComponents 开头插入创造物品栏早退")

# 2. 清理 Round 10 留下的 inCreativeInventory 分支（现在是死代码）
old_branch = '''            boolean inCreativeInventory =
                    Minecraft.getInstance().screen instanceof CreativeModeInventoryScreen;

            for (var entry : s.getEnchantments().entrySet()) {'''

new_branch = '''            for (var entry : s.getEnchantments().entrySet()) {'''

if old_branch in c:
    c = c.replace(old_branch, new_branch)
    print("[修改] 移除附魔书分支里的 inCreativeInventory 变量")

old_inner = '''                if (isTitle || isDesc) {
                    if (inCreativeInventory) {
                        // 创造物品栏会往 tooltip 的 index 1 处插入附魔名列表，
                        // 必须保留至少一个 Either.left，否则 ArrayList 越界崩溃。
                        FormattedText styled = Component.literal(line)
                                .withStyle(st -> st.withColor(primaryColor));
                        event.getTooltipElements().set(i, Either.left(styled));
                    } else {
                        event.getTooltipElements().set(i, Either.right(new DaedalusTooltipData(
                                Component.literal(line), theme, -1, true)));
                    }
                }'''

new_inner = '''                if (isTitle || isDesc) {
                    event.getTooltipElements().set(i, Either.right(new DaedalusTooltipData(
                            Component.literal(line), theme, -1, true)));
                }'''

if old_inner in c:
    c = c.replace(old_inner, new_inner)
    print("[修改] 简化为直接替换（创造物品栏已早退，此处不会执行到）")

# 3. primaryColor 变量不再使用，删掉
c = c.replace("            int primaryColor = theme.getPrimaryColor();\n", "")

TARGET.write_text(c, encoding="utf-8")
print(f"[写入] {TARGET.name}")

print("\n" + "=" * 60)
print("Round 11 修复完成")
print("=" * 60)
print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: skip custom tooltip entirely in CreativeModeInventoryScreen"')
print("  git push")