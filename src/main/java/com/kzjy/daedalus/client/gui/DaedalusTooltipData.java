package com.kzjy.daedalus.client.gui;

import com.kzjy.daedalus.enchantment.util.EnchantmentTheme;
import net.minecraft.network.chat.Component;
import net.minecraft.world.inventory.tooltip.TooltipComponent;
import org.jetbrains.annotations.Nullable;

public record DaedalusTooltipData(Component text, EnchantmentTheme theme, int maxWidth, boolean shouldShake, boolean isTitle, @Nullable Component suffix) implements TooltipComponent {
    public DaedalusTooltipData(Component text, EnchantmentTheme theme, int maxWidth, boolean shouldShake, boolean isTitle) {
        this(text, theme, maxWidth, shouldShake, isTitle, null);
    }

    public DaedalusTooltipData(Component text, EnchantmentTheme theme, int maxWidth, boolean shouldShake) {
        this(text, theme, maxWidth, shouldShake, false, null);
    }

    public DaedalusTooltipData(Component text, EnchantmentTheme theme) {
        this(text, theme, -1, true, false, null);
    }
}
