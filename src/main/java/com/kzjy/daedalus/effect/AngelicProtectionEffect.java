package com.kzjy.daedalus.effect;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;

/**
 * @author Kzjy<br>
 * 天使庇佑效果<br>
 * 提供创造模式飞行能力与针对亡灵生物的伤害减免
 */
public class AngelicProtectionEffect extends MobEffect {
    public AngelicProtectionEffect() { super(MobEffectCategory.BENEFICIAL, 0xFFFFE0); }
}
