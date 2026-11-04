package com.kzjy.daedalus.client;

import com.kzjy.daedalus.Daedalus;
import com.kzjy.daedalus.client.gui.DaedalusTooltipData;
import com.kzjy.daedalus.enchantment.util.EnchantmentTheme;
import com.kzjy.daedalus.registry.DaedalusEnchantments;
import com.mojang.datafixers.util.Either;
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
import net.neoforged.neoforge.client.event.RenderTooltipEvent;

@EventBusSubscriber(modid = Daedalus.MODID, value = Dist.CLIENT)
public class DaedalusForgeClientEvents {

    @SubscribeEvent
    public static void onGatherTooltipComponents(RenderTooltipEvent.GatherComponents event) {
        ItemStack s = event.getItemStack();
        
        // 1.21.1 中获取附魔要同时检查普通物品和附魔书
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
