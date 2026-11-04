package com.kzjy.daedalus.effect;

import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;

/**
 * @author Kzjy<br>
 * 深渊诅咒效果<br>
 * 削减目标的护甲与韧性，并降低其输出伤害
 */
public class AbyssalCurseEffect extends MobEffect {
    public AbyssalCurseEffect() {
        super(MobEffectCategory.HARMFUL, 0x100010);
        // 每级 -10% 护甲
        this.addAttributeModifier(Attributes.ARMOR, "5D6F0BA2-1186-46AC-B896-C61C5CEE99CC", -0.1, AttributeModifier.Operation.MULTIPLY_TOTAL);
        // 每级 -5% 韧性
        this.addAttributeModifier(Attributes.ARMOR_TOUGHNESS, "D053F825-7977-444F-9689-7B7E14083873", -0.05, AttributeModifier.Operation.MULTIPLY_TOTAL);
    }
}
