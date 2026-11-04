package com.kzjy.daedalus.mixin;

import com.kzjy.daedalus.duck.IDaedalusLivingEvent;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * @author Kzjy<br>
 * LivingDamageEvent 混入<br>
 * 拦截 setAmount, 防止最终伤害被削减<br>
 */
@Mixin(value = LivingDamageEvent.class, remap = false)
public abstract class MixinLivingDamageEvent {
    @Shadow(remap = false) public abstract float getAmount();

    @Inject(method = "setAmount", at = @At("HEAD"), cancellable = true, remap = false)
    private void daedalus$interceptSetAmount(float amount, CallbackInfo ci) {
        if (((IDaedalusLivingEvent) (Object) this).daedalus$isOnlyAmountUp()) {
            if (amount < this.getAmount()) {
                ci.cancel();
            }
        }
    }
}
