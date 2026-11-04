package com.kzjy.daedalus.mixin;

import com.kzjy.daedalus.duck.IDaedalusLivingEvent;
import net.minecraft.world.entity.Entity;
import net.neoforged.neoforge.event.entity.EntityEvent;
import net.neoforged.neoforge.event.entity.living.LivingEvent;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;

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
}
