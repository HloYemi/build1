package com.kzjy.daedalus.duck;

/**
 * @author Kzjy<br>
 * 鸭子接口 - DamageSource 扩展<br>
 * 用于标记伤害源属性<br>
 * <p>
 * 实现见: {@link com.kzjy.daedalus.mixin.MixinDamageSource}<br>
 */
public interface IDaedalusDamageSource {
    void daedalus$setBypassAll(boolean bypass);
    boolean daedalus$isBypassAll();

    void daedalus$setVoidBreach(boolean breach);
    boolean daedalus$isVoidBreach();

    void daedalus$giveSpecialTag(byte tag);
    void daedalus$cleanSpecialTag(byte tag);
    boolean daedalus$hasTag(byte tag);
}
