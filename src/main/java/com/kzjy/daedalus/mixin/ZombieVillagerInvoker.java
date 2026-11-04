package com.kzjy.daedalus.mixin;

import net.minecraft.world.entity.monster.ZombieVillager;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.gen.Invoker;

import javax.annotation.Nullable;
import java.util.UUID;

/**
 * @author Kzjy<br>
 * 僵尸村民转换调用器<br>
 * 用于访问 ZombieVillager 类的受保护方法 startConverting
 */
@Mixin(ZombieVillager.class)
public interface ZombieVillagerInvoker {
    @Invoker("startConverting")
    void invokeStartConverting(@Nullable UUID conversionStarter, int villagerConversionTime);
}
