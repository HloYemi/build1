package com.kzjy.daedalus.effect;

import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.entity.LivingEntity;

public class MarkOfSinEffect extends MobEffect {
    public MarkOfSinEffect() {
        super(MobEffectCategory.HARMFUL, 0x8B0000);
    }

    @Override
    public boolean applyEffectTick(LivingEntity entity, int amplifier) {
        if (entity.level().isClientSide) return false;
        float maxHealth = entity.getMaxHealth();
        float basePercent = 0.05f;
        float damageAmount = maxHealth * (basePercent + (amplifier * 0.01f));
        entity.hurt(entity.damageSources().magic(), damageAmount);
        return true;
    }

    @Override
    public boolean shouldApplyEffectTickThisTick(int duration, int amplifier) {
        return duration % 20 == 0;
    }
}
