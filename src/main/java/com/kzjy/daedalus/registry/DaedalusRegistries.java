package com.kzjy.daedalus.registry;

import com.kzjy.daedalus.Daedalus;
import com.kzjy.daedalus.effect.*;
import com.kzjy.daedalus.item.LovePoemSwordItem;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.item.*;
import net.minecraft.world.item.enchantment.EnchantmentInstance;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class DaedalusRegistries {
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(Daedalus.MODID);
    public static final DeferredRegister<MobEffect> MOB_EFFECTS = DeferredRegister.create(Registries.MOB_EFFECT, Daedalus.MODID);
    public static final DeferredRegister<CreativeModeTab> CREATIVE_MODE_TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, Daedalus.MODID);

    public static final DeferredHolder<Item, Item> LOVE_POEM_SWORD = ITEMS.register("love_poem_sword", LovePoemSwordItem::new);

    public static final DeferredHolder<MobEffect, MobEffect> ABYSSAL_CURSE = MOB_EFFECTS.register("abyssal_curse", AbyssalCurseEffect::new);
    public static final DeferredHolder<MobEffect, MobEffect> MARK_OF_SIN = MOB_EFFECTS.register("mark_of_sin", MarkOfSinEffect::new);
    public static final DeferredHolder<MobEffect, MobEffect> ABYSSAL_PROTECTION = MOB_EFFECTS.register("abyssal_protection", AbyssalProtectionEffect::new);
    public static final DeferredHolder<MobEffect, MobEffect> ANGELIC_PROTECTION = MOB_EFFECTS.register("angelic_protection", AngelicProtectionEffect::new);

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> DAEDALUS_TAB = CREATIVE_MODE_TABS.register("daedalus_tab", () ->
        CreativeModeTab.builder()
            .icon(() -> new ItemStack(Items.ENCHANTED_BOOK))
            .title(Component.translatable("itemGroup.daedalus"))
            .displayItems((params, output) -> {
                output.accept(LOVE_POEM_SWORD.get().getDefaultInstance());
                var lookup = params.holders().lookupOrThrow(Registries.ENCHANTMENT);
                lookup.listElements().forEach(h -> {
                    if (Daedalus.MODID.equals(h.key().location().getNamespace())) {
                        int min = Math.max(1, h.value().getMinLevel());
                        int max = h.value().getMaxLevel();
                        for (int i = min; i <= max; ++i)
                            output.accept(EnchantedBookItem.createForEnchantment(new EnchantmentInstance(h, i)));
                    }
                });
            })
            .build());
}
