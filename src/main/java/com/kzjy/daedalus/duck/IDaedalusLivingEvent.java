package com.kzjy.daedalus.duck;

/**
 * @author Kzjy<br>
 * 鸭子接口 - LivingEvent 扩展<br>
 * 用于在事件总线中传递强制控制信号<br>
 * <p>
 * 实现见: {@link com.kzjy.daedalus.mixin.MixinLivingEvent}<br>
 * 调用见: {@link com.kzjy.daedalus.event.DaedalusEvents}<br>
 */
public interface IDaedalusLivingEvent {
    void daedalus$setUncancelable(boolean uncancelable);
    boolean daedalus$isUncancelable();

    void daedalus$setOnlyAmountUp(boolean onlyUp);
    boolean daedalus$isOnlyAmountUp();
}
