package com.kzjy.daedalus.mixin;

import com.kzjy.daedalus.duck.IDaedalusDamageSource;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.tags.TagKey;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.damagesource.DamageType;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/**
 * @author Kzjy<br>
 * 伤害源混入<br>
 * 实现 IDaedalusDamageSource 接口, 强制注入伤害标签<br>
 * <p>
 * 逻辑:<br>
 * - VoidBreach: 穿透无敌/冷却<br>
 * - BypassAll: 穿透护甲/盾牌/无敌/抗性/冷却/药水及灾变模组防御<br>
 */
@Mixin(DamageSource.class)
public class MixinDamageSource implements IDaedalusDamageSource {
    @Unique private boolean daedalus$bypassAll = false;
    @Unique private boolean daedalus$voidBreach = false;
    @Unique private final boolean[] daedalus$tags = new boolean[128];

    @Override public void daedalus$setBypassAll(boolean bypass) { this.daedalus$bypassAll = bypass; }
    @Override public boolean daedalus$isBypassAll() { return this.daedalus$bypassAll; }
    @Override public void daedalus$setVoidBreach(boolean breach) { this.daedalus$voidBreach = breach; }
    @Override public boolean daedalus$isVoidBreach() { return this.daedalus$voidBreach; }
    @Override public void daedalus$giveSpecialTag(byte tag) { daedalus$tags[tag] = true; }
    @Override public void daedalus$cleanSpecialTag(byte tag) { daedalus$tags[tag] = false; }
    @Override public boolean daedalus$hasTag(byte tag) { return daedalus$tags[tag]; }

    /**
     * 强制 Tag 匹配<br>
     * 当开启特殊模式时, 欺骗系统认为该伤害源包含特定 Tag
     */
    @Inject(method = "is(Lnet/minecraft/tags/TagKey;)Z", at = @At("HEAD"), cancellable = true)
    private void daedalus$forceTags(TagKey<DamageType> tagKey, CallbackInfoReturnable<Boolean> cir) {
        if (this.daedalus$voidBreach) {
            if (tagKey == DamageTypeTags.BYPASSES_INVULNERABILITY || tagKey == DamageTypeTags.BYPASSES_COOLDOWN) {
                cir.setReturnValue(true);
            }
        }
        if (this.daedalus$bypassAll) {
            if (tagKey == DamageTypeTags.BYPASSES_ARMOR || tagKey == DamageTypeTags.BYPASSES_SHIELD ||
                    tagKey == DamageTypeTags.BYPASSES_INVULNERABILITY || tagKey == DamageTypeTags.BYPASSES_RESISTANCE ||
                    tagKey == DamageTypeTags.BYPASSES_COOLDOWN || tagKey == DamageTypeTags.BYPASSES_EFFECTS) {
                cir.setReturnValue(true);
            }
            if (tagKey.location().toString().equals("cataclysm:bypasses_hurt_time")) {
                cir.setReturnValue(true);
            }
        }
    }
}
