package com.kzjy.daedalus.effect;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;

public class AbyssalCurseEffect extends MobEffect {
    public AbyssalCurseEffect() {
        super(MobEffectCategory.HARMFUL, 0x100010);
        this.addAttributeModifier(Attributes.ARMOR,
                ResourceLocation.fromNamespaceAndPath("daedalus", "abyssal_curse_armor"),
                -0.1, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL);
        this.addAttributeModifier(Attributes.ARMOR_TOUGHNESS,
                ResourceLocation.fromNamespaceAndPath("daedalus", "abyssal_curse_toughness"),
                -0.05, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL);
    }
}
