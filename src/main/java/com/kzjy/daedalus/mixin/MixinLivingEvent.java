package com.kzjy.daedalus.mixin;

import com.kzjy.daedalus.duck.IDaedalusLivingEvent;
import net.minecraft.world.entity.Entity;
import net.neoforged.neoforge.event.entity.EntityEvent;
import net.neoforged.neoforge.event.entity.living.LivingEvent;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;

/**
 * @author Kzjy<br>
 * LivingEvent 混入<br>
 * 实现事件状态的强制控制 (不可取消/仅增伤)<br>
 */
@Mixin(LivingEvent.class)
public abstract class MixinLivingEvent extends EntityEvent implements IDaedalusLivingEvent {
    @Unique private boolean daedalus$uncancelable = false;
    @Unique private boolean daedalus$onlyAmountUp = false;

    public MixinLivingEvent(Entity entity) {
        super(entity);
    }

    @Override
    public void daedalus$setUncancelable(boolean uncancelable) {
        this.daedalus$uncancelable = uncancelable;
    }

    @Override
    public boolean daedalus$isUncancelable() {
        return this.daedalus$uncancelable;
    }

    @Override
    public void daedalus$setOnlyAmountUp(boolean onlyUp) {
        this.daedalus$onlyAmountUp = onlyUp;
    }

    @Override
    public boolean daedalus$isOnlyAmountUp() {
        return this.daedalus$onlyAmountUp;
    }

    /**
     * 拒绝取消操作<br>
     * 当 daedalus$uncancelable 为 true 时生效
     */
    @Override
    public void setCanceled(boolean cancel) {
        if (this.daedalus$uncancelable && cancel) {
            return;
        }
        super.setCanceled(cancel);
    }

    /**
     * 伪造未取消状态<br>
     * 当 daedalus$uncancelable 为 true 时强制返回 false
     */
    @Override
    public boolean isCanceled() {
        if (this.daedalus$uncancelable) {
            return false;
        }
        return super.isCanceled();
    }
}
