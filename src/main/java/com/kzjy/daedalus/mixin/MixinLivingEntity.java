package com.kzjy.daedalus.mixin;

import com.kzjy.daedalus.duck.IDaedalusDamageSource;
import com.kzjy.daedalus.registry.DaedalusRegistries;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(LivingEntity.class)
public abstract class MixinLivingEntity extends Entity {

    public MixinLivingEntity(EntityType<?> t, Level l) { super(t, l); }

    @Shadow public abstract boolean hasEffect(net.minecraft.core.Holder<MobEffect> h);
    @Shadow public abstract MobEffectInstance getEffect(net.minecraft.core.Holder<MobEffect> h);

    @Inject(method = "getHealth", at = @At("HEAD"), cancellable = true)
    private void daedalus$getHealth(CallbackInfoReturnable<Float> cir) {
        if (this.getPersistentData().getBoolean("DaedalusDeathMark")) cir.setReturnValue(0.0f);
    }

    @Inject(method = "checkTotemDeathProtection", at = @At("HEAD"), cancellable = true)
    private void daedalus$blockTotems(DamageSource source, CallbackInfoReturnable<Boolean> cir) {
        if (source instanceof IDaedalusDamageSource ds && ds.daedalus$isBypassAll()) cir.setReturnValue(false);
    }

    @Inject(method = "tick", at = @At("HEAD"))
    private void daedalus$angelFlight(CallbackInfo ci) {
        if ((Object)this instanceof Player player) {
            var inst = player.getEffect(DaedalusRegistries.ANGELIC_PROTECTION);
            if (inst != null && inst.getAmplifier() + 1 >= 4 && !player.getAbilities().mayfly) {
                player.getAbilities().mayfly = true;
                player.onUpdateAbilities();
            }
        }
    }
}
