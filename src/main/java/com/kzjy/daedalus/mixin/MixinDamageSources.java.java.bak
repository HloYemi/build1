package com.kzjy.daedalus.mixin;

import com.kzjy.daedalus.config.DaedalusConfig;
import com.kzjy.daedalus.duck.IDaedalusDamageSource;
import com.kzjy.daedalus.registry.DaedalusRegistries;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageSources;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.enchantment.EnchantmentHelper;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * @author Kzjy<br>
 * 伤害源工厂混入<br>
 * 在伤害源创建阶段注入特殊Tag (BypassAll/VoidBreach)<br>
 * <p>
 * 逻辑:<br>
 * 1. 玩家攻击注入: {@link #daedalus$modifyPlayerAttack}<br>
 * 2. 生物攻击注入: {@link #daedalus$modifyMobAttack}<br>
 */
@Mixin(DamageSources.class)
public class MixinDamageSources {

    /**
     * 拦截玩家攻击源<br>
     * 判定: 耀星之噬/爱之诗 -> BypassAll<br>
     * 判定: 虚空破壁 -> VoidBreach
     */
    @Inject(method = "playerAttack", at = @At("RETURN"))
    private void daedalus$modifyPlayerAttack(Player player, CallbackInfoReturnable<DamageSource> cir) {
        DamageSource source = cir.getReturnValue();
        if (source instanceof IDaedalusDamageSource ds) {
            ItemStack stack = player.getMainHandItem();

            boolean isStellarOrLove = (DaedalusConfig.COMMON.stellarEaterEnabled.get() &&
                    EnchantmentHelper.getItemEnchantmentLevel(DaedalusRegistries.STELLAR_EATER.get(), stack) > 0)
                    || stack.getItem() == DaedalusRegistries.LOVE_POEM_SWORD.get();

            if (isStellarOrLove) {
                ds.daedalus$setBypassAll(true);
            }

            if (DaedalusConfig.COMMON.voidBreachEnabled.get() &&
                    EnchantmentHelper.getItemEnchantmentLevel(DaedalusRegistries.VOID_BREACH.get(), stack) > 0) {
                ds.daedalus$setVoidBreach(true);
            }
        }
    }

    /**
     * 拦截生物攻击源<br>
     * 逻辑同上, 兼容非玩家实体
     */
    @Inject(method = "mobAttack", at = @At("RETURN"))
    private void daedalus$modifyMobAttack(LivingEntity attacker, CallbackInfoReturnable<DamageSource> cir) {
        DamageSource source = cir.getReturnValue();
        if (source instanceof IDaedalusDamageSource ds) {
            ItemStack stack = attacker.getMainHandItem();

            boolean isStellarOrLove = (DaedalusConfig.COMMON.stellarEaterEnabled.get() &&
                    EnchantmentHelper.getItemEnchantmentLevel(DaedalusRegistries.STELLAR_EATER.get(), stack) > 0)
                    || stack.getItem() == DaedalusRegistries.LOVE_POEM_SWORD.get();

            if (isStellarOrLove) {
                ds.daedalus$setBypassAll(true);
            }

            if (DaedalusConfig.COMMON.voidBreachEnabled.get() &&
                    EnchantmentHelper.getItemEnchantmentLevel(DaedalusRegistries.VOID_BREACH.get(), stack) > 0) {
                ds.daedalus$setVoidBreach(true);
            }
        }
    }
}
