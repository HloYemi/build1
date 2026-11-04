#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 22: 恢复创造模式 Tooltip 渲染，修复剑的字体，优化附魔书模型
"""
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SRC = P / "src/main/java/com/kzjy/daedalus"
RES = P / "src/main/resources"

print("=" * 60)
print("Round 22: 恢复剑的 Tooltip，优化附魔书特效")
print("=" * 60)

# 1. 重写 DaedalusForgeClientEvents，移除拦截
fce = SRC / "client" / "DaedalusForgeClientEvents.java"
fce.write_text('''package com.kzjy.daedalus.client;

import com.kzjy.daedalus.Daedalus;
import com.kzjy.daedalus.client.gui.DaedalusTooltipData;
import com.kzjy.daedalus.enchantment.util.EnchantmentTheme;
import com.kzjy.daedalus.registry.DaedalusEnchantments;
import com.kzjy.daedalus.registry.DaedalusRegistries;
import com.mojang.datafixers.util.Either;
import net.minecraft.ChatFormatting;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.resources.language.I18n;
import net.minecraft.core.Holder;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.ItemEnchantments;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RenderTooltipEvent;

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

        processEnchantments(s, s.getEnchantments(), event);
        processEnchantments(s, s.getOrDefault(DataComponents.STORED_ENCHANTMENTS, ItemEnchantments.EMPTY), event);
    }

    private static void processEnchantments(ItemStack stack, ItemEnchantments enchantments, RenderTooltipEvent.GatherComponents event) {
        for (var entry : enchantments.entrySet()) {
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

            for (int i = 0; i < event.getTooltipElements().size(); i++) {
                var el = event.getTooltipElements().get(i);
                if (el.left().isEmpty()) continue;
                
                String line = el.left().get().getString();
                boolean isTitle = line.contains(base);
                boolean isDesc = !full.isEmpty() && !isTitle && full.contains(line.trim()) && line.trim().length() > 4;
                
                if (isTitle || isDesc) {
                    event.getTooltipElements().set(i, Either.right(new DaedalusTooltipData(
                            Component.literal(line), theme, -1, true)));
                }
            }
        }
    }
}
''', encoding="utf-8")
print("[重写] DaedalusForgeClientEvents.java (移除了创造模式拦截)")

# 2. 修复附魔书，使用 handheld 强制渲染 3D 特效，或者使用 Layer 叠加
# 由于附魔书是 2D 模型，在 1.21 中，如果不在手持时渲染，可能是因为没有 3D 深度。
# 我们给附魔书换成 "item/handheld" 确实会变形，所以保持 generated，但添加 halo 属性
book_path = RES / "assets/minecraft/models/item/enchanted_book.json"
book_path.write_text("""{
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
""", encoding="utf-8")
print("[写入] enchanted_book.json 增加了 halo_cosmic")

print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: restore creative mode tooltips for sword, use halo_cosmic for book"')
print("  git push")