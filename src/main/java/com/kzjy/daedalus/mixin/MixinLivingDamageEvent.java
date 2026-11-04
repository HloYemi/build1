package com.kzjy.daedalus.mixin;

import com.kzjy.daedalus.duck.IDaedalusLivingEvent;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(value = LivingDamageEvent.Pre.class, remap = false)
public abstract class MixinLivingDamageEvent {
    @Shadow(remap = false) public abstract float getNewDamage();

    @Inject(method = "setNewDamage", at = @At("HEAD"), cancellable = true, remap = false)
    private void daedalus$interceptSetNewDamage(float newDamage, CallbackInfo ci) {
        if (((IDaedalusLivingEvent) (Object) this).daedalus$isOnlyAmountUp()) {
            if (newDamage < this.getNewDamage()) {
                ci.cancel();
            }
        }
    }
}
