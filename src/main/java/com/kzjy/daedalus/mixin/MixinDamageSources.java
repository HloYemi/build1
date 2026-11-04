package com.kzjy.daedalus.mixin;

import com.kzjy.daedalus.config.DaedalusConfig;
import com.kzjy.daedalus.duck.IDaedalusDamageSource;
import com.kzjy.daedalus.registry.DaedalusEnchantments;
import com.kzjy.daedalus.registry.DaedalusRegistries;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageSources;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(DamageSources.class)
public class MixinDamageSources {

    private static boolean isBypass(ItemStack s) {
        return (DaedalusConfig.COMMON.stellarEaterEnabled.get()
                && DaedalusEnchantments.getLevel(s, DaedalusEnchantments.STELLAR_EATER) > 0)
                || s.is(DaedalusRegistries.LOVE_POEM_SWORD.get());
    }

    private static void apply(DamageSource source, ItemStack s) {
        if (source instanceof IDaedalusDamageSource ds) {
            if (isBypass(s)) ds.daedalus$setBypassAll(true);
            if (DaedalusConfig.COMMON.voidBreachEnabled.get()
                    && DaedalusEnchantments.getLevel(s, DaedalusEnchantments.VOID_BREACH) > 0)
                ds.daedalus$setVoidBreach(true);
        }
    }

    @Inject(method = "playerAttack", at = @At("RETURN"))
    private void daedalus$playerAttack(Player player, CallbackInfoReturnable<DamageSource> cir) {
        apply(cir.getReturnValue(), player.getMainHandItem());
    }

    @Inject(method = "mobAttack", at = @At("RETURN"))
    private void daedalus$mobAttack(LivingEntity attacker, CallbackInfoReturnable<DamageSource> cir) {
        apply(cir.getReturnValue(), attacker.getMainHandItem());
    }
}
