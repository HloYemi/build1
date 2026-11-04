#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daedalus NeoForge 1.21.1 移植 - Round 3
策略：直接重写所有出错文件，不依赖字符串替换。
"""
import re
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SRC = P / "src" / "main" / "java" / "com" / "kzjy" / "daedalus"
RES = P / "src" / "main" / "resources"

def write_file(rel: str, content: str):
    path = SRC / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[写入] {rel}")

# =====================================================================
# 1. DaedalusEvents.java —— 完全重写
# =====================================================================
write_file("event/DaedalusEvents.java", '''package com.kzjy.daedalus.event;

import com.kzjy.daedalus.Daedalus;
import com.kzjy.daedalus.config.DaedalusConfig;
import com.kzjy.daedalus.duck.IDaedalusDamageSource;
import com.kzjy.daedalus.duck.IDaedalusLivingEvent;
import com.kzjy.daedalus.registry.DaedalusEnchantments;
import com.kzjy.daedalus.registry.DaedalusRegistries;
import com.kzjy.daedalus.mixin.ZombieVillagerInvoker;
import com.kzjy.daedalus.util.DaedalusDeathManager;
import net.minecraft.ChatFormatting;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.tags.EntityTypeTags;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.boss.wither.WitherBoss;
import net.minecraft.world.entity.monster.ZombieVillager;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.BowItem;
import net.minecraft.world.item.CrossbowItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TridentItem;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.EnchantmentHelper;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.common.util.TriState;
import net.neoforged.neoforge.event.entity.living.*;
import net.neoforged.neoforge.event.entity.player.AttackEntityEvent;
import net.neoforged.neoforge.event.entity.player.ItemTooltipEvent;
import net.neoforged.neoforge.event.tick.EntityTickEvent;
import net.neoforged.neoforge.event.tick.PlayerTickEvent;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@EventBusSubscriber(modid = Daedalus.MODID)
public class DaedalusEvents {
    private static final Random RANDOM = new Random();

    private static CompoundTag getCustomData(ItemStack stack) {
        return stack.getOrDefault(DataComponents.CUSTOM_DATA, CustomData.EMPTY).copyTag();
    }

    private static void setCustomData(ItemStack stack, CompoundTag tag) {
        stack.set(DataComponents.CUSTOM_DATA, CustomData.of(tag));
    }

    private static float calculateBaseDamage(LivingEntity attacker) {
        double base = attacker.getAttributeValue(Attributes.ATTACK_DAMAGE);
        if (attacker instanceof Player p) {
            float s = p.getAttackStrengthScale(0.5f);
            base *= (0.2f + s * s * 0.8f);
        }
        return (float) base;
    }

    private static float getCataclysmDamageCap(LivingEntity e) {
        try {
            Method m = e.getClass().getMethod("DamageCap");
            if (m.getReturnType() == float.class) return (float) m.invoke(e);
        } catch (Exception ignored) {}
        return Float.MAX_VALUE;
    }

    private static boolean isAbsoluteTrueDamage(ItemStack s) {
        if (s.is(DaedalusRegistries.LOVE_POEM_SWORD.get())) return true;
        return DaedalusConfig.COMMON.stellarEaterEnabled.get()
                && DaedalusEnchantments.getLevel(s, DaedalusEnchantments.STELLAR_EATER) > 0;
    }

    @SubscribeEvent(priority = EventPriority.HIGHEST)
    public static void onPlayerAttackOverride(AttackEntityEvent event) {
        if (event.getEntity().level().isClientSide) return;
        ItemStack stack = event.getEntity().getMainHandItem();
        if (DaedalusConfig.COMMON.voidBreachEnabled.get()
                && DaedalusEnchantments.getLevel(stack, DaedalusEnchantments.VOID_BREACH) > 0) {
            if (event.getTarget() instanceof LivingEntity t) {
                t.invulnerableTime = 0;
                if (t instanceof WitherBoss w && w.getInvulnerableTicks() > 0) w.setInvulnerableTicks(0);
                if (t instanceof Player tp && tp.getAbilities().invulnerable) tp.getAbilities().invulnerable = false;
            }
        }
    }

    @SubscribeEvent(priority = EventPriority.HIGHEST)
    public static void onLivingIncomingDamageInit(LivingIncomingDamageEvent event) {
        if (event.getEntity().level().isClientSide) return;
        if (event.getSource().getEntity() instanceof LivingEntity a) {
            ItemStack w = a.getMainHandItem();
            if (DaedalusConfig.COMMON.voidBreachEnabled.get()
                    && DaedalusEnchantments.getLevel(w, DaedalusEnchantments.VOID_BREACH) > 0) {
                if (event.getSource() instanceof IDaedalusDamageSource ds) ds.daedalus$setVoidBreach(true);
            }
            if (isAbsoluteTrueDamage(w)) {
                if (event.getSource() instanceof IDaedalusDamageSource ds) ds.daedalus$setBypassAll(true);
                if (event instanceof IDaedalusLivingEvent dle) {
                    dle.daedalus$setUncancelable(true);
                    dle.daedalus$setOnlyAmountUp(true);
                }
            }
        }
    }

    @SubscribeEvent(priority = EventPriority.LOWEST, receiveCanceled = true)
    public static void onLivingIncomingDamageEnforce(LivingIncomingDamageEvent event) {
        if (event.isCanceled() && event.getSource() instanceof IDaedalusDamageSource ds && ds.daedalus$isBypassAll())
            event.setCanceled(false);
    }

    @SubscribeEvent(priority = EventPriority.HIGH)
    public static void onLivingHurtLogic(LivingDamageEvent.Pre event) {
        if (!(event.getSource().getEntity() instanceof LivingEntity a)) return;
        ItemStack w = a.getMainHandItem();

        if (DaedalusConfig.COMMON.cursedChainEnabled.get()) {
            int lvl = DaedalusEnchantments.getLevel(w, DaedalusEnchantments.CURSED_CHAIN);
            if (lvl > 0) {
                float reduction = 0.5f - (lvl * 0.05f);
                event.setNewDamage(event.getNewDamage() * (1.0f - reduction));
                float bonus = event.getNewDamage() * (lvl * 0.1f);
                if (bonus > 0) {
                    var t = event.getEntity();
                    int inv = t.invulnerableTime; t.invulnerableTime = 0;
                    t.hurt(a.damageSources().magic(), bonus);
                    t.invulnerableTime = inv;
                }
            }
        }
        if (DaedalusConfig.COMMON.markOfSinEnabled.get()) {
            int lvl = DaedalusEnchantments.getLevel(w, DaedalusEnchantments.MARK_OF_SIN);
            if (lvl > 0) {
                int eff = lvl * DaedalusConfig.COMMON.markOfSinLevelPerLevel.get();
                event.getEntity().addEffect(new MobEffectInstance(DaedalusRegistries.MARK_OF_SIN, 100, eff - 1));
            }
        }
        if (DaedalusConfig.COMMON.divineJudgmentEnabled.get()) {
            int lvl = DaedalusEnchantments.getLevel(w, DaedalusEnchantments.DIVINE_JUDGMENT);
            if (lvl > 0 && event.getEntity().getType().is(EntityTypeTags.UNDEAD)) {
                float b = 1.0f + lvl * DaedalusConfig.COMMON.divineJudgmentUndeadBonusPerLevel.get().floatValue();
                event.setNewDamage(event.getNewDamage() * b);
                if (event.getEntity() instanceof ZombieVillager zv
                        && RANDOM.nextFloat() < lvl * DaedalusConfig.COMMON.divineJudgmentCureChance.get()
                        && !zv.level().isClientSide)
                    ((ZombieVillagerInvoker) zv).invokeStartConverting(a.getUUID(), 1);
            }
        }
        if (DaedalusConfig.COMMON.soulThirstEnabled.get()) {
            int lvl = DaedalusEnchantments.getLevel(w, DaedalusEnchantments.SOUL_THIRST);
            if (lvl > 0) {
                CompoundTag tag = getCustomData(w);
                int souls = tag.getInt("DaedalusSouls");
                int max = DaedalusConfig.COMMON.soulThirstMaxThreshold.get();
                if (souls >= max) {
                    float base = DaedalusConfig.COMMON.soulThirstBaseBonus.get().floatValue();
                    float lb = lvl > 1 ? (lvl - 1) * DaedalusConfig.COMMON.soulThirstBonusPerLevel.get().floatValue() : 0;
                    var t = event.getEntity();
                    int inv = t.invulnerableTime; t.invulnerableTime = 0;
                    t.hurt(a.damageSources().magic(), event.getNewDamage() * (base + lb));
                    t.invulnerableTime = inv;
                    tag.putInt("DaedalusSouls", 0);
                    setCustomData(w, tag);
                }
            }
        }
        if (DaedalusConfig.COMMON.lifeSiphonEnabled.get()) {
            int lvl = DaedalusEnchantments.getLevel(w, DaedalusEnchantments.LIFE_SIPHON);
            if (lvl > 0) {
                float base = DaedalusConfig.COMMON.lifeSiphonBaseHeal.get().floatValue();
                float lb = lvl > 1 ? (lvl - 1) * DaedalusConfig.COMMON.lifeSiphonHealPerLevel.get().floatValue() : 0;
                a.heal(event.getNewDamage() * (base + lb));
            }
        }
    }

    @SubscribeEvent(priority = EventPriority.HIGHEST)
    public static void onLivingDamageInit(LivingDamageEvent.Pre event) {
        if (!(event.getSource().getEntity() instanceof LivingEntity a)) return;
        ItemStack w = a.getMainHandItem();
        if (isAbsoluteTrueDamage(w)) {
            if (event instanceof IDaedalusLivingEvent dle) {
                dle.daedalus$setUncancelable(true);
                dle.daedalus$setOnlyAmountUp(true);
            }
        } else if (DaedalusConfig.COMMON.voidRendEnabled.get()
                && DaedalusEnchantments.getLevel(w, DaedalusEnchantments.VOID_REND) > 0
                && event instanceof IDaedalusLivingEvent dle) {
            dle.daedalus$setOnlyAmountUp(true);
        }
    }

    @SubscribeEvent(priority = EventPriority.LOWEST)
    public static void onLivingDamageEnforce(LivingDamageEvent.Pre event) {
        if (event.getSource().getEntity() instanceof LivingEntity a) {
            ItemStack w = a.getMainHandItem();
            LivingEntity t = event.getEntity();
            if (isAbsoluteTrueDamage(w)) {
                if (event instanceof IDaedalusLivingEvent dle) {
                    dle.daedalus$setUncancelable(true);
                    dle.daedalus$setOnlyAmountUp(true);
                }
                float raw = calculateBaseDamage(a);
                if (event.getNewDamage() < raw) event.setNewDamage(raw);
                t.invulnerableTime = 0;
                if (w.is(DaedalusRegistries.LOVE_POEM_SWORD.get())) {
                    DaedalusDeathManager.markForExecution(t);
                    DaedalusDeathManager.executeExecution(t, event.getSource());
                }
            }
            if (DaedalusConfig.COMMON.voidRendEnabled.get()) {
                int lvl = DaedalusEnchantments.getLevel(w, DaedalusEnchantments.VOID_REND);
                if (lvl > 0) {
                    if (event.getSource() instanceof IDaedalusDamageSource ds) ds.daedalus$setBypassAll(true);
                    float pct = lvl * DaedalusConfig.COMMON.voidRendTrueDamagePercentPerLevel.get().floatValue();
                    float attr = (float) a.getAttributeValue(Attributes.ATTACK_DAMAGE);
                    if (event.getNewDamage() < attr * pct) event.setNewDamage(attr * pct);
                    if (t.getHealth() / t.getMaxHealth() < DaedalusConfig.COMMON.voidRendRagnarokThreshold.get().floatValue()) {
                        float chance = lvl * DaedalusConfig.COMMON.voidRendRagnarokChancePerLevel.get().floatValue();
                        if (RANDOM.nextFloat() < chance) {
                            t.setHealth(0.0f);
                            t.die(a.damageSources().genericKill());
                        }
                    }
                }
            }
            if (DaedalusEnchantments.getLevel(w, DaedalusEnchantments.VOID_BREACH) > 0) {
                float cap = getCataclysmDamageCap(t);
                if (cap != Float.MAX_VALUE && event.getNewDamage() > cap) event.setNewDamage(cap);
            }
        }

        LivingEntity victim = event.getEntity();
        if (DaedalusConfig.COMMON.immortalEnabled.get()) {
            int lvl = getArmorEnchantmentLevel(victim, DaedalusEnchantments.IMMORTAL);
            if (lvl > 0) {
                CompoundTag d = victim.getPersistentData();
                int dur = DaedalusConfig.COMMON.immortalBaseDuration.get()
                        + lvl * DaedalusConfig.COMMON.immortalDurationPerLevel.get();
                double red = DaedalusConfig.COMMON.immortalBaseReduction.get()
                        + lvl * DaedalusConfig.COMMON.immortalReductionPerLevel.get();
                int timer = d.getInt("DaedalusImmortalTimer");
                float cur = d.contains("DaedalusImmortalMultiplier") ? d.getFloat("DaedalusImmortalMultiplier") : 1.0f;
                event.setNewDamage(event.getNewDamage() * cur);
                float next = (timer > 0 ? cur : 1.0f) * (float)(1.0 - red);
                if (next < 0.01f) next = 0.01f;
                d.putFloat("DaedalusImmortalMultiplier", next);
                d.putInt("DaedalusImmortalTimer", dur);
            }
        }
    }

    @SubscribeEvent(priority = EventPriority.HIGHEST)
    public static void onLivingDeathInit(LivingDeathEvent event) {
        if (event.getSource().getEntity() instanceof LivingEntity a) {
            if (isAbsoluteTrueDamage(a.getMainHandItem())
                    && event instanceof IDaedalusLivingEvent dle) dle.daedalus$setUncancelable(true);
        }
        if (event.getSource().getEntity() instanceof Player p && DaedalusConfig.COMMON.soulThirstEnabled.get()) {
            ItemStack w = p.getMainHandItem();
            int lvl = DaedalusEnchantments.getLevel(w, DaedalusEnchantments.SOUL_THIRST);
            if (lvl > 0) {
                CompoundTag tag = getCustomData(w);
                int cur = tag.getInt("DaedalusSouls");
                int gain = (int)(lvl * DaedalusConfig.COMMON.soulThirstGainPerLevel.get());
                int max = DaedalusConfig.COMMON.soulThirstMaxThreshold.get();
                tag.putInt("DaedalusSouls", Math.min(max, cur + gain));
                setCustomData(w, tag);
            }
        }
    }

    @SubscribeEvent(priority = EventPriority.LOWEST, receiveCanceled = true)
    public static void onLivingDeathEnforce(LivingDeathEvent event) {
        if (event.getSource().getEntity() instanceof LivingEntity a
                && isAbsoluteTrueDamage(a.getMainHandItem())) {
            if (event.isCanceled()) event.setCanceled(false);
            event.getEntity().setHealth(0.0f);
        }
    }

    @SubscribeEvent(priority = EventPriority.HIGHEST)
    public static void onLivingHealInit(LivingHealEvent event) {
        LivingEntity e = event.getEntity();
        var inst = e.getEffect(DaedalusRegistries.ANGELIC_PROTECTION);
        if (inst == null) return;
        int lvl = inst.getAmplifier() + 1;
        float boosted = event.getAmount() * (1.0f + lvl);
        if (lvl >= 4) {
            if (event.isCanceled()) event.setCanceled(false);
            if (event instanceof IDaedalusLivingEvent dle) {
                dle.daedalus$setUncancelable(true);
                dle.daedalus$setOnlyAmountUp(true);
            }
            if (boosted <= 0.01f) boosted = e.getMaxHealth() * 0.05f;
        }
        event.setAmount(boosted);
    }

    @SubscribeEvent
    public static void onEntityTick(EntityTickEvent.Post event) {
        if (!(event.getEntity() instanceof LivingEntity e)) return;
        if (e.level().isClientSide) return;
        DaedalusDeathManager.tickExecution(e);

        CompoundTag data = e.getPersistentData();
        int it = data.getInt("DaedalusImmortalTimer");
        if (it > 0) {
            data.putInt("DaedalusImmortalTimer", it - 1);
            if (it - 1 <= 0) data.putFloat("DaedalusImmortalMultiplier", 1.0f);
        }
        if (e.tickCount % 10 != 0) return;

        if (DaedalusConfig.COMMON.immortalEnabled.get()
                && getArmorEnchantmentLevel(e, DaedalusEnchantments.IMMORTAL) > 0) {
            for (var eff : new ArrayList<>(e.getActiveEffects()))
                if (eff.getEffect().value().getCategory() == MobEffectCategory.HARMFUL)
                    e.removeEffect(eff.getEffect());
        }
        if (DaedalusConfig.COMMON.abyssalProtectionEnabled.get()) {
            int lvl = DaedalusEnchantments.getLevel(e.getItemBySlot(EquipmentSlot.CHEST), DaedalusEnchantments.ABYSSAL_PROTECTION);
            if (lvl > 0) {
                int bl = lvl * DaedalusConfig.COMMON.abyssalProtectionLevelPerLevel.get();
                e.addEffect(new MobEffectInstance(DaedalusRegistries.ABYSSAL_PROTECTION, 100, bl - 1, false, false));
            }
        }
        if (e instanceof Player player) {
            boolean hasAngel = false;
            if (DaedalusConfig.COMMON.angelicProtectionEnabled.get()) {
                int c = DaedalusEnchantments.getLevel(player.getItemBySlot(EquipmentSlot.CHEST), DaedalusEnchantments.ANGELIC_PROTECTION);
                int l = DaedalusEnchantments.getLevel(player.getItemBySlot(EquipmentSlot.LEGS), DaedalusEnchantments.ANGELIC_PROTECTION);
                if (c > 0 || l > 0) {
                    int base = Math.max(c, l);
                    if (c > 0 && c == l) base += 1;
                    int total = base * DaedalusConfig.COMMON.angelicProtectionLevelPerLevel.get();
                    if (total >= 4) hasAngel = true;
                    player.addEffect(new MobEffectInstance(DaedalusRegistries.ANGELIC_PROTECTION, 100, total - 1, false, false));
                }
            }
            if (!hasAngel && !player.isCreative() && !player.isSpectator() && player.getAbilities().mayfly) {
                player.getAbilities().mayfly = false;
                player.getAbilities().flying = false;
                player.onUpdateAbilities();
            }
        }
    }

    @SubscribeEvent
    public static void onMobEffectApplicable(MobEffectEvent.Applicable event) {
        if (DaedalusConfig.COMMON.immortalEnabled.get()
                && event.getEffectInstance().getEffect().value().getCategory() == MobEffectCategory.HARMFUL
                && getArmorEnchantmentLevel(event.getEntity(), DaedalusEnchantments.IMMORTAL) > 0) {
            event.setResult(TriState.FALSE);
        }
    }

    @SubscribeEvent
    public static void onPlayerTick(PlayerTickEvent.Post event) {
        var p = event.getEntity();
        if (p.level().isClientSide || p.tickCount % 5 != 0) return;
        if (!DaedalusConfig.COMMON.abyssalGazeEnabled.get()) return;
        int lvl = DaedalusEnchantments.getLevel(p.getItemBySlot(EquipmentSlot.HEAD), DaedalusEnchantments.ABYSSAL_GAZE);
        if (lvl <= 0) return;
        Vec3 look = p.getLookAngle();
        Vec3 eye = p.getEyePosition();
        AABB box = p.getBoundingBox().expandTowards(look.scale(20)).inflate(2);
        for (LivingEntity t : p.level().getEntitiesOfClass(LivingEntity.class, box, x -> x != p)) {
            Vec3 tp = t.getBoundingBox().getCenter();
            if (look.dot(tp.subtract(eye).normalize()) > 0.95 && eye.distanceTo(tp) <= 20 && p.hasLineOfSight(t)) {
                int cl = lvl * DaedalusConfig.COMMON.abyssalGazeCurseLevelPerLevel.get();
                t.addEffect(new MobEffectInstance(DaedalusRegistries.ABYSSAL_CURSE, 100, cl - 1));
            }
        }
    }

    @SubscribeEvent
    public static void onItemUseTick(LivingEntityUseItemEvent.Tick event) {
        if (!DaedalusConfig.COMMON.daedalusBowEnabled.get()) return;
        ItemStack s = event.getItem();
        if (!(s.getItem() instanceof BowItem || s.getItem() instanceof CrossbowItem || s.getItem() instanceof TridentItem)) return;
        int lvl = DaedalusEnchantments.getLevel(s, DaedalusEnchantments.DAEDALUS_BOW);
        if (lvl <= 0) return;
        double bonus = lvl * DaedalusConfig.COMMON.daedalusBowSpeedPerLevel.get();
        CompoundTag d = event.getEntity().getPersistentData();
        float acc = d.getFloat("DaedalusBowAccumulator") + (float) bonus;
        int red = (int) acc;
        if (red > 0) {
            event.setDuration(Math.max(0, event.getDuration() - red));
            acc -= red;
        }
        d.putFloat("DaedalusBowAccumulator", acc);
    }

    @SubscribeEvent
    public static void onItemTooltip(ItemTooltipEvent event) {
        ItemStack s = event.getItemStack();
        if (DaedalusEnchantments.getLevel(s, DaedalusEnchantments.SOUL_THIRST) > 0) {
            int souls = getCustomData(s).getInt("DaedalusSouls");
            int max = DaedalusConfig.COMMON.soulThirstMaxThreshold.get();
            event.getToolTip().add(Component.literal("Souls: " + souls + "/" + max).withStyle(ChatFormatting.DARK_RED));
        }
    }

    @SubscribeEvent
    public static void onOutputDamage(LivingDamageEvent.Pre event) {
        if (event.getSource().getEntity() instanceof LivingEntity a) {
            var inst = a.getEffect(DaedalusRegistries.ABYSSAL_CURSE);
            if (inst != null) {
                int lvl = inst.getAmplifier() + 1;
                event.setNewDamage(event.getNewDamage() * (1.0f - Math.min(0.8f, lvl * 0.1f)));
            }
        }
    }

    @SubscribeEvent
    public static void onDefend(LivingDamageEvent.Pre event) {
        LivingEntity v = event.getEntity();
        var aInst = v.getEffect(DaedalusRegistries.ABYSSAL_PROTECTION);
        if (aInst != null) {
            boolean breach = event.getSource() instanceof IDaedalusDamageSource ds
                    && (ds.daedalus$isVoidBreach() || ds.daedalus$isBypassAll());
            int lvl = aInst.getAmplifier() + 1;
            if (!breach && RANDOM.nextFloat() < lvl * 0.05) { event.setNewDamage(0); return; }
            event.setNewDamage(event.getNewDamage() * (1.0f - lvl * 0.1f));
        }
        var gInst = v.getEffect(DaedalusRegistries.ANGELIC_PROTECTION);
        if (gInst != null && event.getSource().getEntity() instanceof LivingEntity a
                && a.getType().is(EntityTypeTags.UNDEAD)) {
            int lvl = gInst.getAmplifier() + 1;
            event.setNewDamage(event.getNewDamage() * (1.0f - Math.min(0.99f, lvl * 0.25f)));
        }
    }

    private static int getArmorEnchantmentLevel(LivingEntity e, ResourceKey<Enchantment> key) {
        int max = 0;
        for (ItemStack s : e.getArmorSlots()) max = Math.max(max, DaedalusEnchantments.getLevel(s, key));
        return max;
    }
}
''')

# =====================================================================
# 2. ClientSetup.java
# =====================================================================
write_file("ClientSetup.java", '''package com.kzjy.daedalus;

import com.kzjy.daedalus.client.model.DaedalusModelLoader;
import net.minecraft.client.renderer.item.ItemProperties;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Items;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.neoforge.client.event.ModelEvent;

@EventBusSubscriber(modid = Daedalus.MODID, value = Dist.CLIENT, bus = EventBusSubscriber.Bus.MOD)
public class ClientSetup {
    @SubscribeEvent
    public static void clientSetup(FMLClientSetupEvent event) {
        event.enqueueWork(() -> {
            ItemProperties.register(Items.ENCHANTED_BOOK,
                    ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "enchanted_book"),
                    (stack, world, entity, seed) -> {
                        var enchants = stack.getEnchantments();
                        for (var e : enchants.entrySet()) {
                            var keyOpt = e.getKey().unwrapKey();
                            if (keyOpt.isPresent() && keyOpt.get().location().getNamespace().equals(Daedalus.MODID)) {
                                return 1.0f;
                            }
                        }
                        return 0.0f;
                    });
        });
    }

    @SubscribeEvent
    public static void registerGeometryLoaders(ModelEvent.RegisterGeometryLoaders event) {
        event.register(
            ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "cosmic"),
            new DaedalusModelLoader()
        );
    }
}
''')

# =====================================================================
# 3. DaedalusRenderTypes.java —— 修复 ResourceLocation
# =====================================================================
rt = SRC / "client" / "DaedalusRenderTypes.java"
if rt.exists():
    c = rt.read_text(encoding="utf-8")
    c = c.replace('new ResourceLocation(Daedalus.MODID, "textures/misc/gr.png")',
                  'ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "textures/misc/gr.png")')
    c = c.replace('new ResourceLocation(Daedalus.MODID, "textures/misc/gr_m.png")',
                  'ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "textures/misc/gr_m.png")')
    c = c.replace('new ResourceLocation(Daedalus.MODID, "daedalus_cosmic")',
                  'ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "daedalus_cosmic")')
    c = c.replace('new ResourceLocation(Daedalus.MODID, "cosmic_neo")',
                  'ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "cosmic_neo")')
    c = c.replace('new ResourceLocation(Daedalus.MODID, "glow_edge")',
                  'ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "glow_edge")')
    c = c.replace('new ResourceLocation("textures/atlas/blocks.png")',
                  'ResourceLocation.parse("textures/atlas/blocks.png")')
    # 修复 @Mod.EventBusSubscriber
    c = c.replace("@Mod.EventBusSubscriber", "@EventBusSubscriber")
    if "import net.neoforged.fml.common.EventBusSubscriber;" not in c:
        c = c.replace("import net.neoforged.bus.api.SubscribeEvent;",
                      "import net.neoforged.bus.api.SubscribeEvent;\nimport net.neoforged.fml.common.EventBusSubscriber;")
    rt.write_text(c, encoding="utf-8")
    print("[修改] DaedalusRenderTypes.java")

# =====================================================================
# 4. DaedalusGlowRenderer.java
# =====================================================================
gr = SRC / "client" / "renderer" / "DaedalusGlowRenderer.java"
if gr.exists():
    c = gr.read_text(encoding="utf-8")
    c = c.replace('new ResourceLocation(Daedalus.MODID, "textures/misc/gr.png")',
                  'ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "textures/misc/gr.png")')
    c = c.replace('new ResourceLocation(Daedalus.MODID, "textures/misc/gr_m.png")',
                  'ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "textures/misc/gr_m.png")')
    c = c.replace('vertexConsumer.vertex(matrix, x, y, z)',
                  'vertexConsumer.addVertex(matrix, x, y, z)')
    gr.write_text(c, encoding="utf-8")
    print("[修改] DaedalusGlowRenderer.java")

# =====================================================================
# 5. DaedalusModelLoader.java —— 重写
# =====================================================================
write_file("client/model/DaedalusModelLoader.java", '''package com.kzjy.daedalus.client.model;

import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import net.minecraft.client.renderer.block.model.BlockModel;
import net.minecraft.client.renderer.block.model.ItemOverrides;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.client.resources.model.Material;
import net.minecraft.client.resources.model.ModelBaker;
import net.minecraft.client.resources.model.ModelState;
import net.minecraft.client.resources.model.UnbakedModel;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.GsonHelper;
import net.neoforged.neoforge.client.model.geometry.IGeometryBakingContext;
import net.neoforged.neoforge.client.model.geometry.IGeometryLoader;
import net.neoforged.neoforge.client.model.geometry.IUnbakedGeometry;

import java.util.Collections;
import java.util.function.Function;

public class DaedalusModelLoader implements IGeometryLoader<DaedalusModelLoader.DaedalusCosmicGeometry> {

    @Override
    public DaedalusCosmicGeometry read(JsonObject jsonObject, JsonDeserializationContext context) throws JsonParseException {
        JsonObject cosmicObj = jsonObject.getAsJsonObject("daedalus_cosmic");
        boolean isNeo = false;
        int neoType = 0;

        if (cosmicObj == null) {
            cosmicObj = jsonObject.getAsJsonObject("cosmic_neo");
            if (cosmicObj != null) {
                isNeo = true;
                neoType = GsonHelper.getAsInt(cosmicObj, "type", 0);
            }
        }

        if (cosmicObj == null) throw new IllegalStateException("Missing 'daedalus_cosmic' or 'cosmic_neo' object.");

        String maskPath = cosmicObj.get("mask").getAsString();

        int glowColor = 0xFFFFFF;
        float glowWidth = 0.0f;
        float glowOffset = 0.0f;

        if (jsonObject.has("glow_edge")) {
            JsonObject glowObj = jsonObject.getAsJsonObject("glow_edge");
            glowColor = GsonHelper.getAsInt(glowObj, "color", 16777215);
            glowWidth = GsonHelper.getAsFloat(glowObj, "width", 1.0f);
            glowOffset = GsonHelper.getAsFloat(glowObj, "offset", 0.02f);
        }

        JsonObject clean = jsonObject.deepCopy();
        clean.remove("daedalus_cosmic");
        clean.remove("cosmic_neo");
        clean.remove("glow_edge");
        clean.remove("loader");

        BlockModel baseModel = context.deserialize(clean, BlockModel.class);

        return new DaedalusCosmicGeometry(baseModel,
                ResourceLocation.parse(maskPath),
                glowColor, glowWidth, glowOffset, isNeo, neoType);
    }

    public static class DaedalusCosmicGeometry implements IUnbakedGeometry<DaedalusCosmicGeometry> {
        private final BlockModel baseModel;
        private final ResourceLocation maskLocation;
        private final int glowColor;
        private final float glowWidth;
        private final float glowOffset;
        private final boolean isNeo;
        private final int neoType;

        public DaedalusCosmicGeometry(BlockModel baseModel, ResourceLocation maskLocation,
                                      int glowColor, float glowWidth, float glowOffset,
                                      boolean isNeo, int neoType) {
            this.baseModel = baseModel;
            this.maskLocation = maskLocation;
            this.glowColor = glowColor;
            this.glowWidth = glowWidth;
            this.glowOffset = glowOffset;
            this.isNeo = isNeo;
            this.neoType = neoType;
        }

        @Override
        public BakedModel bake(IGeometryBakingContext context, ModelBaker baker,
                               Function<Material, TextureAtlasSprite> spriteGetter,
                               ModelState modelState, ItemOverrides overrides) {
            BakedModel bakedBaseModel = this.baseModel.bake(
                    baker, this.baseModel, spriteGetter, modelState, true);
            return new DaedalusCosmicBakedModel(bakedBaseModel,
                    Collections.singletonList(maskLocation),
                    glowColor, glowWidth, glowOffset, isNeo, neoType);
        }

        @Override
        public void resolveParents(Function<ResourceLocation, UnbakedModel> modelGetter,
                                   IGeometryBakingContext context) {
            this.baseModel.resolveParents(modelGetter);
        }
    }
}
''')

# =====================================================================
# 6. LovePoemSwordItem.java —— 重写
# =====================================================================
write_file("item/LovePoemSwordItem.java", '''package com.kzjy.daedalus.item;

import com.kzjy.daedalus.enchantment.util.EnchantmentTheme;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.Style;
import net.minecraft.tags.BlockTags;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.Tiers;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.UseAnim;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.tags.TagKey;
import org.jetbrains.annotations.Nullable;

import java.util.List;

public class LovePoemSwordItem extends SwordItem {

    public LovePoemSwordItem() {
        super(new Tier() {
                  @Override public int getUses() { return 0; }
                  @Override public float getSpeed() { return 10.0F; }
                  @Override public float getAttackDamageBonus() { return 0.0F; }
                  @Override public TagKey<Block> getIncorrectBlocksForDrops() {
                      return BlockTags.INCORRECT_FOR_NETHERITE_TOOL;
                  }
                  @Override public int getEnchantmentValue() { return 25; }
                  @Override public Ingredient getRepairIngredient() { return Ingredient.EMPTY; }
              },
              new Properties().rarity(Rarity.EPIC).fireResistant()
                  .attributes(SwordItem.createAttributes(Tiers.NETHERITE, 1314 - 1, -2.4F + 2.3F)));
    }

    @Override
    public UseAnim getUseAnimation(ItemStack stack) {
        return UseAnim.BLOCK;
    }

    @Override
    public int getUseDuration(ItemStack stack) {
        return 72000;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        player.startUsingItem(hand);
        return InteractionResultHolder.consume(stack);
    }

    @Override
    public ItemStack getDefaultInstance() {
        ItemStack stack = new ItemStack(this);
        stack.set(DataComponents.HIDE_TOOLTIP, net.minecraft.util.Unit.INSTANCE);
        return stack;
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slotId, boolean isSelected) {
        super.inventoryTick(stack, level, entity, slotId, isSelected);
    }

    @Override
    public Component getName(ItemStack stack) {
        return Component.translatable(this.getDescriptionId(stack))
                .withStyle(Style.EMPTY.withColor(EnchantmentTheme.LOVE_BLUE.getPrimaryColor()));
    }

    @Override
    public void appendHoverText(ItemStack stack, @Nullable Level level, List<Component> tooltip, TooltipFlag flag) {
        if (Screen.hasAltDown()) {
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc0.line1"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc0.line2"));
        } else {
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc1.line1"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc1.line2"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc1.line3"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc1.line4"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc1.line5"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc1.line6"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc1.line7"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.hold_alt"));
        }
    }
}
''')

# =====================================================================
# 7. AbyssalCurseEffect.java
# =====================================================================
write_file("effect/AbyssalCurseEffect.java", '''package com.kzjy.daedalus.effect;

import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;

public class AbyssalCurseEffect extends MobEffect {
    public AbyssalCurseEffect() {
        super(MobEffectCategory.HARMFUL, 0x100010);
        this.addAttributeModifier(Attributes.ARMOR,
                ResourceLocation.fromNamespaceAndPath("daedalus", "abyssal_curse_armor"),
                -0.1, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL);
        this.addAttributeModifier(Attributes.ARMOR_TOUGHNESS,
                ResourceLocation.fromNamespaceAndPath("daedalus", "abyssal_curse_toughness"),
                -0.05, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL);
    }
}
''')

# =====================================================================
# 8. MarkOfSinEffect.java
# =====================================================================
write_file("effect/MarkOfSinEffect.java", '''package com.kzjy.daedalus.effect;

import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.entity.LivingEntity;

public class MarkOfSinEffect extends MobEffect {
    public MarkOfSinEffect() {
        super(MobEffectCategory.HARMFUL, 0x8B0000);
    }

    @Override
    public boolean applyEffectTick(LivingEntity entity, int amplifier) {
        if (entity.level().isClientSide) return false;
        float maxHealth = entity.getMaxHealth();
        float basePercent = 0.05f;
        float damageAmount = maxHealth * (basePercent + (amplifier * 0.01f));
        entity.hurt(entity.damageSources().magic(), damageAmount);
        return true;
    }

    @Override
    public boolean shouldApplyEffectTickThisTick(int duration, int amplifier) {
        return duration % 20 == 0;
    }
}
''')

# =====================================================================
# 9. MixinLivingEvent.java —— 简化，移除 setCanceled 覆写
# =====================================================================
write_file("mixin/MixinLivingEvent.java", '''package com.kzjy.daedalus.mixin;

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
''')

# =====================================================================
# 10. MixinLivingDamageEvent.java —— 修正方法名
# =====================================================================
write_file("mixin/MixinLivingDamageEvent.java", '''package com.kzjy.daedalus.mixin;

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
''')

# =====================================================================
# 11. MixinSynchedEntityData.java —— getSerializer → serializer
# =====================================================================
msd = SRC / "mixin" / "MixinSynchedEntityData.java"
if msd.exists():
    c = msd.read_text(encoding="utf-8")
    c = c.replace("key.getSerializer()", "key.serializer()")
    msd.write_text(c, encoding="utf-8")
    print("[修改] MixinSynchedEntityData.java")

# =====================================================================
# 12. DaedalusForgeClientEvents.java —— ClientTickEvent
# =====================================================================
ce = SRC / "client" / "DaedalusForgeClientEvents.java"
if ce.exists():
    c = ce.read_text(encoding="utf-8")
    c = c.replace("import net.neoforged.neoforge.event.TickEvent;",
                  "import net.neoforged.neoforge.client.event.ClientTickEvent;")
    c = c.replace("public static void clientTick(TickEvent.ClientTickEvent event) {",
                  "public static void clientTick(ClientTickEvent.Post event) {")
    c = c.replace("if (event.phase != TickEvent.Phase.START) return;", "")
    ce.write_text(c, encoding="utf-8")
    print("[修改] DaedalusForgeClientEvents.java")

# =====================================================================
# 13. DaedalusClientEvents.java —— @EventBusSubscriber
# =====================================================================
dce = SRC / "client" / "DaedalusClientEvents.java"
if dce.exists():
    c = dce.read_text(encoding="utf-8")
    c = c.replace("@Mod.EventBusSubscriber", "@EventBusSubscriber")
    if "import net.neoforged.fml.common.EventBusSubscriber;" not in c:
        c = c.replace("import net.neoforged.bus.api.SubscribeEvent;",
                      "import net.neoforged.bus.api.SubscribeEvent;\nimport net.neoforged.fml.common.EventBusSubscriber;")
    dce.write_text(c, encoding="utf-8")
    print("[修改] DaedalusClientEvents.java")

# =====================================================================
# 14. mixins.json 清理（移除 MixinLivingHurtEvent）
# =====================================================================
mj = RES / "daedalus.mixins.json"
if mj.exists():
    s = mj.read_text(encoding="utf-8")
    s = re.sub(r'\\s*"MixinLivingHurtEvent",?', '', s)
    mj.write_text(s, encoding="utf-8")
    print("[修改] daedalus.mixins.json")

print("\\n" + "=" * 60)
print("Round 3 修复完成")
print("=" * 60)
print("\\n下一步:")
print("  git add .")
print('  git commit -m "fix: NeoForge 1.21.1 API round 3"')
print("  git push")