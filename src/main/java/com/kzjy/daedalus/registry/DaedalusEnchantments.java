package com.kzjy.daedalus.registry;

import com.kzjy.daedalus.Daedalus;
import com.kzjy.daedalus.enchantment.util.EnchantmentTheme;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.enchantment.Enchantment;

import java.util.HashMap;
import java.util.Map;

public final class DaedalusEnchantments {
    private DaedalusEnchantments() {}

    private static ResourceKey<Enchantment> k(String n) {
        return ResourceKey.create(Registries.ENCHANTMENT, ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, n));
    }

    public static final ResourceKey<Enchantment> DAEDALUS_BOW = k("daedalus_bow");
    public static final ResourceKey<Enchantment> ABYSSAL_GAZE = k("abyssal_gaze");
    public static final ResourceKey<Enchantment> CURSED_CHAIN = k("cursed_chain");
    public static final ResourceKey<Enchantment> MARK_OF_SIN = k("mark_of_sin");
    public static final ResourceKey<Enchantment> VOID_REND = k("void_rend");
    public static final ResourceKey<Enchantment> SOUL_THIRST = k("soul_thirst");
    public static final ResourceKey<Enchantment> ABYSSAL_PROTECTION = k("abyssal_protection");
    public static final ResourceKey<Enchantment> VOID_BREACH = k("void_breach");
    public static final ResourceKey<Enchantment> DIVINE_JUDGMENT = k("divine_judgment");
    public static final ResourceKey<Enchantment> ANGELIC_PROTECTION = k("angelic_protection");
    public static final ResourceKey<Enchantment> LIFE_SIPHON = k("life_siphon");
    public static final ResourceKey<Enchantment> STELLAR_EATER = k("stellar_eater");
    public static final ResourceKey<Enchantment> IMMORTAL = k("immortal");

    private static final Map<ResourceKey<Enchantment>, EnchantmentTheme> THEMES = new HashMap<>();
    static {
        THEMES.put(DAEDALUS_BOW, EnchantmentTheme.DAEDALUS);
        THEMES.put(ABYSSAL_GAZE, EnchantmentTheme.ABYSS);
        THEMES.put(CURSED_CHAIN, EnchantmentTheme.CURSE);
        THEMES.put(MARK_OF_SIN, EnchantmentTheme.SIN);
        THEMES.put(VOID_REND, EnchantmentTheme.VOID);
        THEMES.put(SOUL_THIRST, EnchantmentTheme.SIN);
        THEMES.put(ABYSSAL_PROTECTION, EnchantmentTheme.ABYSS);
        THEMES.put(VOID_BREACH, EnchantmentTheme.VOID);
        THEMES.put(DIVINE_JUDGMENT, EnchantmentTheme.DIVINE);
        THEMES.put(ANGELIC_PROTECTION, EnchantmentTheme.DIVINE);
        THEMES.put(LIFE_SIPHON, EnchantmentTheme.NATURE);
        THEMES.put(STELLAR_EATER, EnchantmentTheme.MIRACLE);
        THEMES.put(IMMORTAL, EnchantmentTheme.MIRACLE);
    }

    public static EnchantmentTheme getTheme(ResourceKey<Enchantment> key) { return THEMES.get(key); }

    public static int getLevel(ItemStack stack, ResourceKey<Enchantment> key) {
        for (var e : stack.getEnchantments().entrySet())
            if (e.getKey().is(key)) return e.getValue();
        return 0;
    }
}
