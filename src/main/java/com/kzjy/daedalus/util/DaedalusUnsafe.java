package com.kzjy.daedalus.util;

import com.kzjy.daedalus.Daedalus;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.neoforged.fml.util.ObfuscationReflectionHelper;
import sun.misc.Unsafe;

import java.lang.invoke.MethodHandle;
import java.lang.invoke.MethodHandles;
import java.lang.invoke.MethodType;
import java.lang.reflect.Field;

/**
 * @author Kzjy<br>
 * Unsafe 工具类<br>
 * 利用 JVM 底层机制在 Tick 末尾强制执行状态修正<br>
 * <p>
 * 逻辑:<br>
 * - 直接内存修改 invulnerableTime<br>
 * - 强制调用父类 die() 方法<br>
 */
public class DaedalusUnsafe {

    private static Unsafe UNSAFE;
    private static long INVULNERABLE_TIME_OFFSET;
    private static MethodHandle SUPER_DIE;
    private static boolean initialized = false;

    private static void init() {
        if (initialized) return;
        try {
            Field f = Unsafe.class.getDeclaredField("theUnsafe");
            f.setAccessible(true);
            UNSAFE = (Unsafe) f.get(null);

            Field invulField = null;
            try {
                invulField = Entity.class.getDeclaredField("f_19802_");
            } catch (NoSuchFieldException e) {
                invulField = Entity.class.getDeclaredField("invulnerableTime");
            }
            INVULNERABLE_TIME_OFFSET = UNSAFE.objectFieldOffset(invulField);

            Field implLookupField = MethodHandles.Lookup.class.getDeclaredField("IMPL_LOOKUP");
            long offset = UNSAFE.staticFieldOffset(implLookupField);
            MethodHandles.Lookup trustedLookup = (MethodHandles.Lookup) UNSAFE.getObject(MethodHandles.Lookup.class, offset);

            String dieName = "m_6667_";
            try {
                LivingEntity.class.getDeclaredMethod(dieName, DamageSource.class);
            } catch (NoSuchMethodException e) {
                dieName = "die";
            }
            SUPER_DIE = trustedLookup.findSpecial(
                    LivingEntity.class,
                    dieName,
                    MethodType.methodType(void.class, DamageSource.class),
                    LivingEntity.class
            );

            initialized = true;
        } catch (Throwable t) {
            Daedalus.LOGGER.error("DaedalusUnsafe initialization failed: ", t);
        }
    }

    /**
     * 强制修正状态<br>
     * 1. 清空无敌帧 (直接写内存)<br>
     * 2. 强制锁血<br>
     * 3. 强制死亡调用<br>
     */
    public static void enforceEndTick(LivingEntity target) {
        if (!initialized) init();
        if (target.level().isClientSide) return;

        try {
            if (INVULNERABLE_TIME_OFFSET != 0) {
                UNSAFE.putInt(target, INVULNERABLE_TIME_OFFSET, 0);
            }

            if (target.getHealth() > 0) {
                target.setHealth(0.0f);
            }

            if (target.isAlive() || target.getHealth() <= 0) {
                target.setHealth(0.0f);

                if (SUPER_DIE != null) {
                    SUPER_DIE.invoke(target, target.damageSources().genericKill());
                }
            }
        } catch (Throwable t) {
        }
    }
}
