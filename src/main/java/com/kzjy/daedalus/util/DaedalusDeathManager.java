package com.kzjy.daedalus.util;

import com.kzjy.daedalus.Daedalus;
import com.kzjy.daedalus.mixin.LivingEntityAccessor;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.LivingEntity;
import net.neoforged.fml.util.ObfuscationReflectionHelper;
import sun.misc.Unsafe;

import java.lang.invoke.MethodHandle;
import java.lang.invoke.MethodHandles;
import java.lang.invoke.MethodType;
import java.lang.reflect.Field;

/**
 * @author Kzjy<br>
 * 处决管理器 - 核心致死逻辑<br>
 * 实现多层级降维打击, 绕过目标实体的锁血/不死机制<br>
 * <p>
 * 机制索引:<br>
 * 1. JVM层句柄初始化: {@link #initHandles()}<br>
 * 2. 必死标记与Tick追杀: {@link #markForExecution}, {@link #tickExecution}<br>
 * 3. 5层处决逻辑: {@link #executeExecution}<br>
 *    - Layer 1: 满血伤害<br>
 *    - Layer 3: SynchedEntityData 强制写0 (见 {@link com.kzjy.daedalus.mixin.MixinSynchedEntityData})<br>
 *    - Layer 5: MethodHandle 调用父类 die() 绕过 Override<br>
 */
public class DaedalusDeathManager {

    private static MethodHandle SUPER_DIE;
    private static MethodHandle SUPER_TICK_DEATH;
    private static boolean initialized = false;

    // 初始化 MethodHandles, 获取 Unsafe 及受信任 Lookup
    private static void initHandles() {
        if (initialized) return;
        try {
            Field f = Unsafe.class.getDeclaredField("theUnsafe");
            f.setAccessible(true);
            Unsafe unsafe = (Unsafe) f.get(null);

            Field implLookupField = MethodHandles.Lookup.class.getDeclaredField("IMPL_LOOKUP");
            long offset = unsafe.staticFieldOffset(implLookupField);
            MethodHandles.Lookup trustedLookup = (MethodHandles.Lookup) unsafe.getObject(MethodHandles.Lookup.class, offset);

            String dieName = "m_6667_";
            String tickDeathName = "m_6153_";

            try {
                LivingEntity.class.getDeclaredMethod(dieName, DamageSource.class);
            } catch (NoSuchMethodException e) {
                dieName = "die";
                tickDeathName = "tickDeath";
            }

            SUPER_DIE = trustedLookup.findSpecial(
                    LivingEntity.class,
                    dieName,
                    MethodType.methodType(void.class, DamageSource.class),
                    LivingEntity.class
            );

            SUPER_TICK_DEATH = trustedLookup.findSpecial(
                    LivingEntity.class,
                    tickDeathName,
                    MethodType.methodType(void.class),
                    LivingEntity.class
            );

            initialized = true;
        } catch (Throwable t) {
            Daedalus.LOGGER.error("Failed to initialize Daedalus Execution Handles: ", t);
        }
    }

    public static void markForExecution(LivingEntity target) {
        if (target.level().isClientSide) return;
        target.getPersistentData().putBoolean("DaedalusDeathMark", true);
        target.getPersistentData().putInt("DaedalusExecutionTimer", 20);
    }

    public static void tickExecution(LivingEntity target) {
        if (target.level().isClientSide) return;

        if (target.getPersistentData().getBoolean("DaedalusDeathMark")) {
            int timer = target.getPersistentData().getInt("DaedalusExecutionTimer");
            if (timer > 0) {
                target.getPersistentData().putInt("DaedalusExecutionTimer", timer - 1);
                executeExecution(target, target.damageSources().genericKill());
            } else {
                target.getPersistentData().remove("DaedalusDeathMark");
            }
        }
    }

    public static void executeExecution(LivingEntity target, DamageSource source) {
        if (!initialized) initHandles();

        try {
            target.invulnerableTime = 0;
            // 触发 MixinSynchedEntityData 拦截
            target.setHealth(0.0f);
        } catch (Exception ignored) {}

        // Layer 5: 绕过子类重写, 强制执行父类死亡逻辑
        try {
            if (SUPER_DIE != null) {
                SUPER_DIE.invoke(target, source);
            }
        } catch (Throwable t) {
            Daedalus.LOGGER.error("Layer 5 Execution Failed: ", t);
        }

        try {
            target.setHealth(0.0f);

            // 强制推进死亡动画, 防止僵尸实体残留
            if (target.isAlive() && SUPER_TICK_DEATH != null) {
                target.deathTime = 19;
                SUPER_TICK_DEATH.invoke(target);
            } else {
                target.die(source);
            }
        } catch (Throwable ignored) {}
    }
}
