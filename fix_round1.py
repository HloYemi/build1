#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SRC = P / "src" / "main" / "java" / "com" / "kzjy" / "daedalus"

# ============ 1. DaedalusConfig: ForgeConfigSpec → ModConfigSpec
cfg = SRC / "config" / "DaedalusConfig.java"
c = cfg.read_text(encoding="utf-8")
c = c.replace("ForgeConfigSpec", "ModConfigSpec")
cfg.write_text(c, encoding="utf-8")
print("[1] DaedalusConfig: ForgeConfigSpec → ModConfigSpec")

# ============ 2. @Mod.EventBusSubscriber → @EventBusSubscriber
for jf in SRC.rglob("*.java"):
    c = jf.read_text(encoding="utf-8")
    if "@Mod.EventBusSubscriber" in c:
        c = c.replace("@Mod.EventBusSubscriber", "@EventBusSubscriber")
        if "import net.neoforged.fml.common.EventBusSubscriber;" not in c:
            c = c.replace(
                "import net.neoforged.fml.common.Mod;",
                "import net.neoforged.fml.common.Mod;\nimport net.neoforged.fml.common.EventBusSubscriber;"
            )
        jf.write_text(c, encoding="utf-8")
        print(f"[2] {jf.name}")

# ============ 3. ClientSetup 重写
(SRC / "ClientSetup.java").write_text('''package com.kzjy.daedalus;

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
        event.register("cosmic", new DaedalusModelLoader());
    }
}
''', encoding="utf-8")
print("[3] ClientSetup.java 重写")

# ============ 4. DaedalusEvents.java 修复
ev = SRC / "event" / "DaedalusEvents.java"
c = ev.read_text(encoding="utf-8")

c = c.replace("import net.minecraft.world.entity.MobType;",
              "import net.minecraft.tags.EntityTypeTags;")
c = c.replace("import net.neoforged.neoforge.event.TickEvent;",
              "import net.neoforged.neoforge.event.tick.PlayerTickEvent;")

# 方法签名
for old, new in [
    ("onLivingHurtPre(LivingHurtEvent event)", "onLivingHurtPre(LivingDamageEvent.Pre event)"),
    ("onLivingHurtLogic(LivingHurtEvent event)", "onLivingHurtLogic(LivingDamageEvent.Pre event)"),
    ("onLivingDamageInit(LivingDamageEvent event)", "onLivingDamageInit(LivingDamageEvent.Pre event)"),
    ("onLivingDamageEnforce(LivingDamageEvent event)", "onLivingDamageEnforce(LivingDamageEvent.Pre event)"),
    ("onOutputDamage(LivingHurtEvent event)", "onOutputDamage(LivingDamageEvent.Pre event)"),
    ("onDefend(LivingHurtEvent event)", "onDefend(LivingDamageEvent.Pre event)"),
    ("onPlayerTick(TickEvent.PlayerTickEvent event)", "onPlayerTick(PlayerTickEvent.Post event)"),
]:
    c = c.replace(old, new)

# 方法体内的 getAmount/setAmount → getNewDamage/setNewDamage
def replace_in_method(content, sig, replacements):
    pat = re.compile(rf'({re.escape(sig)}.*?\{{)(.*?)(\n    \}})', re.DOTALL)
    def repl(m):
        body = m.group(2)
        for old, new in replacements:
            body = body.replace(old, new)
        return m.group(1) + body + m.group(3)
    return pat.sub(repl, content)

for sig in [
    "onLivingHurtLogic(LivingDamageEvent.Pre event)",
    "onLivingDamageEnforce(LivingDamageEvent.Pre event)",
    "onOutputDamage(LivingDamageEvent.Pre event)",
]:
    c = replace_in_method(c, sig, [
        ("event.getAmount()", "event.getNewDamage()"),
        ("event.setAmount(", "event.setNewDamage("),
    ])

# MobType.UNDEAD → EntityTypeTags
c = c.replace("event.getEntity().getMobType() == MobType.UNDEAD",
              "event.getEntity().getType().is(EntityTypeTags.UNDEAD)")
c = c.replace("a.getMobType() == MobType.UNDEAD",
              "a.getType().is(EntityTypeTags.UNDEAD)")

# onPlayerTick 里的 event.player → event.getEntity()
c = c.replace("event.phase != TickEvent.Phase.END || event.player.level().isClientSide",
              "event.getEntity().level().isClientSide")
c = c.replace("event.player", "event.getEntity()")

# calculateBaseDamage 简化（去掉 getDamageBonus）
old_cbd = '''private static float calculateBaseDamage(LivingEntity attacker, LivingEntity target) {
        double base = attacker.getAttributeValue(Attributes.ATTACK_DAMAGE);
        float ench = EnchantmentHelper.getDamageBonus(attacker.getMainHandItem(), target.getMobType());
        if (attacker instanceof Player p) {
            float s = p.getAttackStrengthScale(0.5f);
            base *= (0.2f + s * s * 0.8f);
            ench *= s;
        }
        return (float) base + ench;
    }'''
new_cbd = '''private static float calculateBaseDamage(LivingEntity attacker, LivingEntity target) {
        double base = attacker.getAttributeValue(Attributes.ATTACK_DAMAGE);
        if (attacker instanceof Player p) {
            float s = p.getAttackStrengthScale(0.5f);
            base *= (0.2f + s * s * 0.8f);
        }
        return (float) base;
    }'''
c = c.replace(old_cbd, new_cbd)

ev.write_text(c, encoding="utf-8")
print("[4] DaedalusEvents.java 修复")

# ============ 5. DaedalusForgeClientEvents.java
ce = SRC / "client" / "DaedalusForgeClientEvents.java"
c = ce.read_text(encoding="utf-8")
c = c.replace("import net.neoforged.neoforge.event.TickEvent;",
              "import net.neoforged.neoforge.client.event.ClientTickEvent;")
c = c.replace("public static void clientTick(TickEvent.ClientTickEvent event) {",
              "public static void clientTick(ClientTickEvent.Post event) {")
c = c.replace("if (event.phase != TickEvent.Phase.START) return;", "")
ce.write_text(c, encoding="utf-8")
print("[5] DaedalusForgeClientEvents.java 修复")

# ============ 6. 删除 MixinLivingHurtEvent
mlh = SRC / "mixin" / "MixinLivingHurtEvent.java"
if mlh.exists():
    mlh.unlink()
    print("[6] 删除 MixinLivingHurtEvent.java")

mj = P / "src" / "main" / "resources" / "daedalus.mixins.json"
if mj.exists():
    s = mj.read_text(encoding="utf-8")
    s = re.sub(r'\s*"MixinLivingHurtEvent",?', '', s)
    mj.write_text(s, encoding="utf-8")
    print("[6] 从 mixins.json 移除 MixinLivingHurtEvent")

# ============ 7. MixinLivingDamageEvent 更新
mld = SRC / "mixin" / "MixinLivingDamageEvent.java"
mld.write_text('''package com.kzjy.daedalus.mixin;

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
        if (((IDaedalusLivingEvent) (Object) this).daedalus$isAmountOnlyUp()) {
            if (newDamage < this.getNewDamage()) {
                ci.cancel();
            }
        }
    }
}
''', encoding="utf-8")
print("[7] MixinLivingDamageEvent.java 更新")

print("\n===== Round 1 修复完成 =====")