package com.kzjy.daedalus.event;

import com.kzjy.daedalus.Daedalus;
import com.kzjy.daedalus.config.DaedalusConfig;
import com.kzjy.daedalus.duck.IDaedalusDamageSource;
import com.kzjy.daedalus.duck.IDaedalusLivingEvent;
import com.kzjy.daedalus.registry.DaedalusEnchantments;
import com.kzjy.daedalus.registry.DaedalusRegistries;
import com.kzjy.daedalus.mixin.ZombieVillagerInvoker;
import com.kzjy.daedalus.util.DaedalusDeathManager;
import net.minecraft.ChatFormatting;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.MobType;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.boss.wither.WitherBoss;
import net.minecraft.world.entity.monster.ZombieVillager;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.BowItem;
import net.minecraft.world.item.CrossbowItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TridentItem;
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.EnchantmentHelper;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.TickEvent;
import net.neoforged.neoforge.event.entity.living.*;
import net.neoforged.neoforge.event.entity.player.AttackEntityEvent;
import net.neoforged.neoforge.event.entity.player.ItemTooltipEvent;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@EventBusSubscriber(modid = Daedalus.MODID)
public class DaedalusEvents {
    private static final Random RANDOM = new Random();

    private static float calculateBaseDamage(LivingEntity attacker, LivingEntity target) {
        double base = attacker.getAttributeValue(Attributes.ATTACK_DAMAGE);
        float ench = EnchantmentHelper.getDamageBonus(attacker.getMainHandItem(), target.getMobType());
        if (attacker instanceof Player p) {
            float s = p.getAttackStrengthScale(0.5f);
            base *= (0.2f + s * s * 0.8f);
            ench *= s;
        }
        return (float) base + ench;
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
        var player = event.getEntity();
        ItemStack stack = player.getMainHandItem();
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
    public static void onLivingAttackInit(LivingAttackEvent event) {
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
    public static void onLivingAttackEnforce(LivingAttackEvent event) {
        if (event.isCanceled() && event.getSource() instanceof IDaedalusDamageSource ds && ds.daedalus$isBypassAll())
            event.setCanceled(false);
    }

    @SubscribeEvent(priority = EventPriority.HIGHEST)
    public static void onLivingHurtPre(LivingHurtEvent event) {
        if (event.getSource().getEntity() instanceof LivingEntity a) {
            ItemStack w = a.getMainHandItem();
            if (DaedalusConfig.COMMON.voidBreachEnabled.get()
                    && DaedalusEnchantments.getLevel(w, DaedalusEnchantments.VOID_BREACH) > 0) {
                event.getEntity().invulnerableTime = 0;
            }
            if (isAbsoluteTrueDamage(w)) {
                event.getEntity().invulnerableTime = 0;
                if (event.getSource() instanceof IDaedalusDamageSource ds) ds.daedalus$setBypassAll(true);
                if (event instanceof IDaedalusLivingEvent dle) {
                    dle.daedalus$setUncancelable(true);
                    dle.daedalus$setOnlyAmountUp(true);
                }
            }
        }
    }

    @SubscribeEvent(priority = EventPriority.HIGH)
    public static void onLivingHurtLogic(LivingHurtEvent event) {
        if (!(event.getSource().getEntity() instanceof LivingEntity a)) return;
        ItemStack w = a.getMainHandItem();

        if (DaedalusConfig.COMMON.cursedChainEnabled.get()) {
            int lvl = DaedalusEnchantments.getLevel(w, DaedalusEnchantments.CURSED_CHAIN);
            if (lvl > 0) {
                float reduction = 0.5f - (lvl * 0.05f);
                event.setAmount(event.getAmount() * (1.0f - reduction));
                float bonus = event.getAmount() * (lvl * 0.1f);
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
            if (lvl > 0 && event.getEntity().getMobType() == MobType.UNDEAD) {
                float b = 1.0f + lvl * DaedalusConfig.COMMON.divineJudgmentUndeadBonusPerLevel.get().floatValue();
                event.setAmount(event.getAmount() * b);
                if (event.getEntity() instanceof ZombieVillager zv
                        && RANDOM.nextFloat() < lvl * DaedalusConfig.COMMON.divineJudgmentCureChance.get()
                        && !zv.level().isClientSide)
                    ((ZombieVillagerInvoker) zv).invokeStartConverting(a.getUUID(), 1);
            }
        }
        if (DaedalusConfig.COMMON.soulThirstEnabled.get()) {
            int lvl = DaedalusEnchantments.getLevel(w, DaedalusEnchantments.SOUL_THIRST);
            if (lvl > 0) {
                CompoundTag tag = w.getOrCreateTag();
                int souls = tag.getInt("DaedalusSouls");
                int max = DaedalusConfig.COMMON.soulThirstMaxThreshold.get();
                if (souls >= max) {
                    float base = DaedalusConfig.COMMON.soulThirstBaseBonus.get().floatValue();
                    float lb = lvl > 1 ? (lvl - 1) * DaedalusConfig.COMMON.soulThirstBonusPerLevel.get().floatValue() : 0;
                    var t = event.getEntity();
                    int inv = t.invulnerableTime; t.invulnerableTime = 0;
                    t.hurt(a.damageSources().magic(), event.getAmount() * (base + lb));
                    t.invulnerableTime = inv;
                    tag.putInt("DaedalusSouls", 0);
                }
            }
        }
        if (DaedalusConfig.COMMON.lifeSiphonEnabled.get()) {
            int lvl = DaedalusEnchantments.getLevel(w, DaedalusEnchantments.LIFE_SIPHON);
            if (lvl > 0) {
                float base = DaedalusConfig.COMMON.lifeSiphonBaseHeal.get().floatValue();
                float lb = lvl > 1 ? (lvl - 1) * DaedalusConfig.COMMON.lifeSiphonHealPerLevel.get().floatValue() : 0;
                a.heal(event.getAmount() * (base + lb));
            }
        }
    }

    @SubscribeEvent(priority = EventPriority.HIGHEST)
    public static void onLivingDamageInit(LivingDamageEvent event) {
        if (!(event.getSource().getEntity() instanceof LivingEntity a)) return;
        ItemStack w = a.getMainHandItem();
        if (isAbsoluteTrueDamage(w)) {
            if (event.isCanceled()) event.setCanceled(false);
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

    @SubscribeEvent(priority = EventPriority.LOWEST, receiveCanceled = true)
    public static void onLivingDamageEnforce(LivingDamageEvent event) {
        if (event.getSource().getEntity() instanceof LivingEntity a) {
            ItemStack w = a.getMainHandItem();
            LivingEntity t = event.getEntity();
            if (isAbsoluteTrueDamage(w)) {
                if (event.isCanceled()) event.setCanceled(false);
                if (event instanceof IDaedalusLivingEvent dle) {
                    dle.daedalus$setUncancelable(true);
                    dle.daedalus$setOnlyAmountUp(true);
                }
                float raw = calculateBaseDamage(a, t);
                if (event.getAmount() < raw) event.setAmount(raw);
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
                    if (event.getAmount() < attr * pct) event.setAmount(attr * pct);
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
                if (cap != Float.MAX_VALUE && event.getAmount() > cap) event.setAmount(cap);
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
                event.setAmount(event.getAmount() * cur);
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
                CompoundTag tag = w.getOrCreateTag();
                int cur = tag.getInt("DaedalusSouls");
                int gain = (int)(lvl * DaedalusConfig.COMMON.soulThirstGainPerLevel.get());
                int max = DaedalusConfig.COMMON.soulThirstMaxThreshold.get();
                tag.putInt("DaedalusSouls", Math.min(max, cur + gain));
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
    public static void onLivingTick(LivingEvent.LivingTickEvent event) {
        if (event.getEntity().level().isClientSide) return;
        LivingEntity e = event.getEntity();
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
            event.setResult(net.neoforged.bus.api.Event.Result.DENY);
        }
    }

    @SubscribeEvent
    public static void onPlayerTick(TickEvent.PlayerTickEvent event) {
        if (event.phase != TickEvent.Phase.END || event.player.level().isClientSide || event.player.tickCount % 5 != 0) return;
        if (!DaedalusConfig.COMMON.abyssalGazeEnabled.get()) return;
        Player p = event.player;
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
            int souls = s.getOrCreateTag().getInt("DaedalusSouls");
            int max = DaedalusConfig.COMMON.soulThirstMaxThreshold.get();
            event.getToolTip().add(Component.literal("Souls: " + souls + "/" + max).withStyle(ChatFormatting.DARK_RED));
        }
    }

    @SubscribeEvent
    public static void onOutputDamage(LivingHurtEvent event) {
        if (event.getSource().getEntity() instanceof LivingEntity a) {
            var inst = a.getEffect(DaedalusRegistries.ABYSSAL_CURSE);
            if (inst != null) {
                int lvl = inst.getAmplifier() + 1;
                event.setAmount(event.getAmount() * (1.0f - Math.min(0.8f, lvl * 0.1f)));
            }
        }
    }

    @SubscribeEvent
    public static void onDefend(LivingHurtEvent event) {
        LivingEntity v = event.getEntity();
        var aInst = v.getEffect(DaedalusRegistries.ABYSSAL_PROTECTION);
        if (aInst != null) {
            boolean breach = event.getSource() instanceof IDaedalusDamageSource ds
                    && (ds.daedalus$isVoidBreach() || ds.daedalus$isBypassAll());
            int lvl = aInst.getAmplifier() + 1;
            if (!breach && RANDOM.nextFloat() < lvl * 0.05) { event.setCanceled(true); return; }
            event.setAmount(event.getAmount() * (1.0f - lvl * 0.1f));
        }
        var gInst = v.getEffect(DaedalusRegistries.ANGELIC_PROTECTION);
        if (gInst != null && event.getSource().getEntity() instanceof LivingEntity a && a.getMobType() == MobType.UNDEAD) {
            int lvl = gInst.getAmplifier() + 1;
            event.setAmount(event.getAmount() * (1.0f - Math.min(0.99f, lvl * 0.25f)));
        }
    }

    private static int getArmorEnchantmentLevel(LivingEntity e, ResourceKey<Enchantment> key) {
        int max = 0;
        for (ItemStack s : e.getArmorSlots()) max = Math.max(max, DaedalusEnchantments.getLevel(s, key));
        return max;
    }
}
