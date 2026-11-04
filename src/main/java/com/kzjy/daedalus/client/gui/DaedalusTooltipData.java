package com.kzjy.daedalus.client.gui;

import com.kzjy.daedalus.enchantment.util.EnchantmentTheme;
import net.minecraft.network.chat.Component;
import net.minecraft.world.inventory.tooltip.TooltipComponent;
import org.jetbrains.annotations.Nullable;

/**
 * @author Kzjy<br>
 * 自定义 Tooltip 数据载体<br>
 * 渲染实现见: {@link DaedalusTextRenderer}<br>
 * <p>
 * 参数:<br>
 * - text: 主体文本<br>
 * - theme: 渲染主题 (颜色/特效)<br>
 * - maxWidth: 居中宽度控制<br>
 * - shouldShake: 是否启用抖动<br>
 * - suffix: 无特效后缀 (如属性名)<br>
 */
public record DaedalusTooltipData(Component text, EnchantmentTheme theme, int maxWidth, boolean shouldShake, @Nullable Component suffix) implements TooltipComponent {
    public DaedalusTooltipData(Component text, EnchantmentTheme theme, int maxWidth, boolean shouldShake) {
        this(text, theme, maxWidth, shouldShake, null);
    }

    public DaedalusTooltipData(Component text, EnchantmentTheme theme) {
        this(text, theme, -1, true, null);
    }
}
