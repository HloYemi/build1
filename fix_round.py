#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daedalus NeoForge 1.21.1 - fix_round.py
当前轮次: Round 10
修复: 完整重写 DaedalusForgeClientEvents.java
  - 去掉 Style 依赖 (用 lambda s -> s.withColor(primaryColor))
  - 创造物品栏降级为静态样式，避免 CreativeModeInventoryScreen 越界崩溃
  - 普通容器保持动态渐变 tooltip
"""
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
TARGET = P / "src/main/java/com/kzjy/daedalus/client/DaedalusForgeClientEvents.java"

if not TARGET.exists():
    print(f"[错误] 找不到: {TARGET}")
    raise SystemExit(1)

CONTENT = '''package com.kzjy.daedalus.client;

import com.kzjy.daedalus.Daedalus;
import com.kzjy.daedalus.client.gui.DaedalusTooltipData;
import com.kzjy.daedalus.enchantment.util.EnchantmentTheme;
import com.kzjy.daedalus.registry.DaedalusEnchantments;
import com.kzjy.daedalus.registry.DaedalusRegistries;
import com.mojang.datafixers.util.Either;
import net.minecraft.ChatFormatting;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.inventory.CreativeModeInventoryScreen;
import net.minecraft.client.resources.language.I18n;
import net.minecraft.core.Holder;
import net.minecraft.network.chat.CommonComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.FormattedText;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.inventory.tooltip.TooltipComponent;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.enchantment.Enchantment;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RenderTooltipEvent;
import net.neoforged.neoforge.event.entity.player.ItemTooltipEvent;

import java.util.ArrayList;
import java.util.List;

@EventBusSubscriber(modid = Daedalus.MODID, value = Dist.CLIENT)
public class DaedalusForgeClientEvents {

    private static int typewriterTick = 0;
    private static boolean wasAltDown = false;
    private static final int TICKS_PER_CHAR = 2;

    @SubscribeEvent
    public static void clientTick(ClientTickEvent.Post event) {
        boolean alt = Screen.hasAltDown();
        if (alt) {
            if (!wasAltDown) typewriterTick = 0;
            typewriterTick++;
        } else {
            typewriterTick = 0;
        }
        wasAltDown = alt;
    }

    @SubscribeEvent
    public static void onItemTooltip(ItemTooltipEvent event) {
        ItemStack s = event.getItemStack();
        if (s.is(DaedalusRegistries.LOVE_POEM_SWORD.get())) {
            List<Component> tip = event.getToolTip();
            tip.add(CommonComponents.EMPTY);
            tip.add(Component.translatable("item.modifiers.mainhand").withStyle(ChatFormatting.GRAY));
            tip.add(Component.literal(" Love ").append(Component.translatable("attribute.name.generic.attack_damage")));
            tip.add(Component.literal(" ")
                    .append(Component.translatable("item.daedalus.love_poem_sword.speed_value"))
                    .append(Component.literal(" "))
                    .append(Component.translatable("attribute.name.generic.attack_speed")));
        }
    }

    @SubscribeEvent
    public static void onGatherTooltipComponents(RenderTooltipEvent.GatherComponents event) {
        ItemStack s = event.getItemStack();
        var font = Minecraft.getInstance().font;

        if (s.is(DaedalusRegistries.LOVE_POEM_SWORD.get())) {
            String name = I18n.get("item.daedalus.love_poem_sword");
            String holdAlt = I18n.get("item.daedalus.love_poem_sword.hold_alt");
            String speedVal = I18n.get("item.daedalus.love_poem_sword.speed_value");
            String atkName = I18n.get("attribute.name.generic.attack_damage");
            String spdName = I18n.get("attribute.name.generic.attack_speed");
            List<String> d0 = List.of(
                    I18n.get("item.daedalus.love_poem_sword.desc0.line1"),
                    I18n.get("item.daedalus.love_poem_sword.desc0.line2"));
            List<String> d1 = new ArrayList<>();
            for (int i = 1; i <= 7; i++) d1.add(I18n.get("item.daedalus.love_poem_sword.desc1.line" + i));

            int w = 0;
            if (Screen.hasAltDown()) for (String x : d0) w = Math.max(w, font.width(x));
            else {
                for (String x : d1) w = Math.max(w, font.width(x));
                w = Math.max(w, font.width(holdAlt));
            }
            int show = typewriterTick / TICKS_PER_CHAR;
            int done = 0;

            for (int i = 0; i < event.getTooltipElements().size(); i++) {
                var el = event.getTooltipElements().get(i);
                if (el.left().isEmpty()) continue;
                String line = el.left().get().getString();
                if (line.contains(name)) {
                    event.getTooltipElements().set(i, Either.right(new DaedalusTooltipData(
                            Component.literal(line), EnchantmentTheme.LOVE_BLUE, -1, false)));
                } else if (d0.contains(line)) {
                    int len = line.length();
                    if (done >= show) {
                        event.getTooltipElements().set(i, Either.right(new DaedalusTooltipData(
                                Component.literal(""), EnchantmentTheme.LAVENDER, w, true)));
                    } else if (done + len > show) {
                        event.getTooltipElements().set(i, Either.right(new DaedalusTooltipData(
                                Component.literal(line.substring(0, show - done)), EnchantmentTheme.LAVENDER, w, true)));
                    } else {
                        event.getTooltipElements().set(i, Either.right(new DaedalusTooltipData(
                                Component.literal(line), EnchantmentTheme.LAVENDER, w, true)));
                    }
                    done += len;
                } else if (d1.contains(line) || line.contains(holdAlt)) {
                    event.getTooltipElements().set(i, Either.right(new DaedalusTooltipData(
                            Component.literal(line), EnchantmentTheme.MIRACLE, w, true)));
                } else if (line.contains("Love") && line.contains(atkName)) {
                    event.getTooltipElements().set(i, Either.right(new DaedalusTooltipData(
                            Component.literal(" Love "), EnchantmentTheme.MIRACLE, -1, true,
                            Component.literal(" " + atkName).withStyle(ChatFormatting.DARK_GREEN))));
                } else if (line.contains(speedVal) && line.contains(spdName)) {
                    event.getTooltipElements().set(i, Either.right(new DaedalusTooltipData(
                            Component.literal(" " + speedVal + " "), EnchantmentTheme.LAVENDER, -1, true,
                            Component.literal(" " + spdName).withStyle(ChatFormatting.DARK_GREEN))));
                }
            }
        }

        boolean inCreativeInventory =
                Minecraft.getInstance().screen instanceof CreativeModeInventoryScreen;

        for (var entry : s.getEnchantments().entrySet()) {
            Holder<Enchantment> holder = entry.getKey();
            var keyOpt = holder.unwrapKey();
            if (keyOpt.isEmpty()) continue;
            ResourceKey<Enchantment> key = keyOpt.get();
            if (!key.location().getNamespace().equals(Daedalus.MODID)) continue;
            EnchantmentTheme theme = DaedalusEnchantments.getTheme(key);
            if (theme == null) continue;

            String base = holder.value().description().getString();
            String dk = key.location().toLanguageKey("enchantment") + ".desc";
            String full = I18n.exists(dk) ? I18n.get(dk) : "";
            int primaryColor = theme.getPrimaryColor();

            for (int i = 0; i < event.getTooltipElements().size(); i++) {
                var el = event.getTooltipElements().get(i);
                if (el.left().isEmpty()) continue;
                String line = el.left().get().getString();
                boolean isTitle = line.contains(base);
                boolean isDesc = !full.isEmpty() && !isTitle && full.contains(line.trim()) && line.trim().length() > 4;
                if (isTitle || isDesc) {
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
                }
            }
        }
    }
}
'''

TARGET.write_text(CONTENT, encoding="utf-8")
print(f"[重写] {TARGET.name}")

print("\n" + "=" * 60)
print("Round 10 修复完成")
print("=" * 60)
print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: rewrite DaedalusForgeClientEvents (drop Style dep, creative tooltip fallback)"')
print("  git push")