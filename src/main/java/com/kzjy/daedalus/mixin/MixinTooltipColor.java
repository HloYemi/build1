package com.kzjy.daedalus.mixin;

import com.kzjy.daedalus.registry.DaedalusRegistries;
import net.minecraft.util.Mth;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.client.event.RenderTooltipEvent;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

import java.awt.Color;

@Mixin(RenderTooltipEvent.Color.class)
public abstract class MixinTooltipColor {

    // 渐变周期（毫秒）：延长至 5000ms，更加舒缓
    @Unique
    private static final long COLOR_CYCLE_TIME = 5000;

    /**
     * 获取当前动态渐变颜色 (HSB 模式)
     * 在 薰衣草紫 (Hue ~0.75) 和 皇家蓝 (Hue ~0.6) 之间平滑摆动
     */
    @Unique
    private int getCurrentGradientColor(long offset) {
        long time = System.currentTimeMillis() + offset;
        // 进度 0.0 ~ 1.0
        float progress = (time % COLOR_CYCLE_TIME) / (float) COLOR_CYCLE_TIME;

        // 使用正弦波将线性进度转换为 -1.0 ~ 1.0 的波形
        // 这样颜色会往复运动：蓝 -> 紫 -> 蓝，而不是突变
        float wave = Mth.sin(progress * (float) Math.PI * 2); // -1.0 ~ 1.0

        // 映射到 0.0 ~ 1.0
        float factor = (wave + 1.0f) / 2.0f;

        // 定义两个颜色的 HSB 值
        // 皇家蓝 (Royal Blue): H=225(0.625), S=0.71, B=0.88
        // 薰衣草 (Lavender):   H=260(0.722), S=0.45, B=1.00

        float h1 = 0.625f; float s1 = 0.75f; float b1 = 0.9f;
        float h2 = 0.740f; float s2 = 0.55f; float b2 = 1.0f;

        // 对 HSB 分别进行线性插值
        float h = h1 + (h2 - h1) * factor;
        float s = s1 + (s2 - s1) * factor;
        float b = b1 + (b2 - b1) * factor;

        // 转回 RGB
        return Color.HSBtoRGB(h, s, b);
    }

    @Inject(method = "getBorderStart", at = @At("HEAD"), cancellable = true, remap = false)
    private void overrideBorderStart(CallbackInfoReturnable<Integer> cir) {
        if (isTargetItem()) {
            cir.setReturnValue(getCurrentGradientColor(0));
        }
    }

    @Inject(method = "getBorderEnd", at = @At("HEAD"), cancellable = true, remap = false)
    private void overrideBorderEnd(CallbackInfoReturnable<Integer> cir) {
        if (isTargetItem()) {
            // 稍微错开一点时间，让边框有流动感，但不要错开太多以免显得杂乱
            cir.setReturnValue(getCurrentGradientColor(1000));
        }
    }

    @Inject(method = "getBackgroundStart", at = @At("HEAD"), cancellable = true, remap = false)
    private void overrideBackgroundStart(CallbackInfoReturnable<Integer> cir) {
        if (isTargetItem()) {
            // 背景色：取当前颜色的极深版本 (亮度降低)，保持色调一致
            int color = getCurrentGradientColor(0);
            int r = (color >> 16) & 0xFF;
            int g = (color >> 8) & 0xFF;
            int b = color & 0xFF;

            // 变暗处理：RGB * 0.2
            r = (int)(r * 0.2f);
            g = (int)(g * 0.2f);
            b = (int)(b * 0.2f);

            // 0xF0 (240) = 约94% 不透明度，深色背景衬托文字
            int finalColor = (0xF0 << 24) | (r << 16) | (g << 8) | b;
            cir.setReturnValue(finalColor);
        }
    }

    @Inject(method = "getBackgroundEnd", at = @At("HEAD"), cancellable = true, remap = false)
    private void overrideBackgroundEnd(CallbackInfoReturnable<Integer> cir) {
        if (isTargetItem()) {
            // 底部背景同理，稍微错开时间
            int color = getCurrentGradientColor(1000);
            int r = (color >> 16) & 0xFF;
            int g = (color >> 8) & 0xFF;
            int b = color & 0xFF;

            r = (int)(r * 0.2f);
            g = (int)(g * 0.2f);
            b = (int)(b * 0.2f);

            int finalColor = (0xF0 << 24) | (r << 16) | (g << 8) | b;
            cir.setReturnValue(finalColor);
        }
    }

    @Unique
    private boolean isTargetItem() {
        RenderTooltipEvent.Color event = (RenderTooltipEvent.Color)(Object)this;
        ItemStack stack = event.getItemStack();
        return stack != null && stack.getItem() == DaedalusRegistries.LOVE_POEM_SWORD.get();
    }
}
