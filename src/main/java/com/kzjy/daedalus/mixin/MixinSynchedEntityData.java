package com.kzjy.daedalus.mixin;

import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import org.spongepowered.asm.mixin.Final;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.ModifyVariable;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * @author Kzjy<br>
 * 数据同步拦截器<br>
 * 配合 {@link com.kzjy.daedalus.util.DaedalusDeathManager} 实现绝对锁血<br>
 * <p>
 * 机制:<br>
 * - GET拦截: 强制返回 0.0f 欺骗外部模组的回滚检查<br>
 * - SET拦截: 拒绝任何 > 0 的血量写入, 无论来源 (治疗/重置/属性修改)<br>
 */
@Mixin(SynchedEntityData.class)
public class MixinSynchedEntityData {

    @Shadow @Final private Entity entity;

    /**
     * 拦截 GET 操作<br>
     * 针对必死实体, 读取 Float 类型数据 (血量/护盾) 时强制返回 0.0f
     */
    @SuppressWarnings("unchecked")
    @Inject(method = "get", at = @At("HEAD"), cancellable = true)
    private <T> void daedalus$interceptGet(EntityDataAccessor<T> key, CallbackInfoReturnable<T> cir) {
        if (this.entity instanceof LivingEntity living) {
            if (living.getPersistentData().getBoolean("DaedalusDeathMark")) {
                if (key.getSerializer() == EntityDataSerializers.FLOAT) {
                    cir.setReturnValue((T) Float.valueOf(0.0f));
                }
            }
        }
    }

    /**
     * 拦截 SET 操作<br>
     * 针对必死实体, 写入 Float 类型数据时若 > 0 则强制改为 0.0f
     */
    @SuppressWarnings("unchecked")
    @ModifyVariable(method = "set", at = @At("HEAD"), argsOnly = true)
    private <T> T daedalus$interceptSet(T value, EntityDataAccessor<T> key) {
        if (this.entity instanceof LivingEntity living) {
            if (living.getPersistentData().getBoolean("DaedalusDeathMark")) {
                if (key.getSerializer() == EntityDataSerializers.FLOAT) {
                    float floatVal = (Float) value;
                    if (floatVal > 0.0f) {
                        return (T) Float.valueOf(0.0f);
                    }
                }
            }
        }
        return value;
    }
}
