#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daedalus NeoForge 1.21.1 - fix_round.py
当前轮次: Round 12
修复: CreativeModeInventoryScreen.getTooltipFromContainerItem 内部 list.add(1, ...) 越界
机制: 在 ItemTooltipEvent 的 LOWEST 优先级监听器里，对创造物品栏场景确保 tooltip 非空。
      原版 CreativeModeInventoryScreen.java:753 会对空列表执行 add(1, ...)，抛 IndexOutOfBoundsException。
"""
from pathlib import Path

P = Path(r"D:\AAA.Download\Daedalus_Enchantment-main")
TARGET = P / "src/main/java/com/kzjy/daedalus/client/DaedalusForgeClientEvents.java"

if not TARGET.exists():
    print(f"[错误] 找不到: {TARGET}")
    raise SystemExit(1)

c = TARGET.read_text(encoding="utf-8")

if "ensureNonEmptyTooltip" in c:
    print("[跳过] 已有 ensureNonEmptyTooltip")
    raise SystemExit(0)

old = '''    @SubscribeEvent
    public static void onItemTooltip(ItemTooltipEvent event) {'''

new = '''    @SubscribeEvent(priority = net.neoforged.bus.api.EventPriority.LOWEST)
    public static void ensureNonEmptyTooltip(ItemTooltipEvent event) {
        // 1.21.1 的 CreativeModeInventoryScreen.getTooltipFromContainerItem 内部会对 tooltip 列表
        // 执行 list.add(1, ...)，如果列表为空则抛 IndexOutOfBoundsException。
        // 在所有 tooltip 监听器之后，确保创造物品栏场景下列表至少有一个元素。
        if (Minecraft.getInstance().screen instanceof CreativeModeInventoryScreen
                && event.getToolTip().isEmpty()) {
            event.getToolTip().add(CommonComponents.EMPTY);
        }
    }

    @SubscribeEvent
    public static void onItemTooltip(ItemTooltipEvent event) {'''

if old not in c:
    print("[错误] 未找到 onItemTooltip 方法头")
    raise SystemExit(1)

c = c.replace(old, new)
TARGET.write_text(c, encoding="utf-8")
print("[修改] DaedalusForgeClientEvents.java: 添加 ensureNonEmptyTooltip")

print("\n" + "=" * 60)
print("Round 12 修复完成")
print("=" * 60)
print("下一步:")
print("  git add .")
print('  git commit -m "fix: ensure non-empty tooltip in CreativeModeInventoryScreen"')
print("  git push")