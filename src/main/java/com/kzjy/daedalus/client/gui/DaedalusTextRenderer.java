package com.kzjy.daedalus.client.gui;

import com.kzjy.daedalus.enchantment.util.EnchantmentTheme;
import net.minecraft.Util;
import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.screens.inventory.tooltip.ClientTooltipComponent;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.network.chat.Component;
import net.minecraft.util.FormattedCharSequence;
import net.minecraft.util.Mth;
import org.joml.Matrix4f;

import java.awt.Color;

public class DaedalusTextRenderer implements ClientTooltipComponent {
    private final FormattedCharSequence text;
    private final String rawString;
    private final EnchantmentTheme theme;
    private final int maxWidth;
    private final boolean shouldShake;
    private final Component suffix;

    public DaedalusTextRenderer(DaedalusTooltipData data) {
        this.text = data.text().getVisualOrderText();
        this.rawString = data.text().getString();
        this.theme = data.theme();
        this.maxWidth = data.maxWidth();
        this.shouldShake = data.shouldShake();
        this.suffix = data.suffix();
    }

    @Override
    public int getHeight() {
        return 10;
    }

    @Override
    public int getWidth(Font font) {
        int w = font.width(text);
        if (suffix != null) {
            w += font.width(suffix);
        }
        return maxWidth > 0 ? maxWidth : w;
    }

    @Override
    public void renderText(Font font, int x, int y, Matrix4f matrix, MultiBufferSource.BufferSource bufferSource) {
        long milliTime = Util.getMillis();
        double timeSeconds = milliTime / 1000.0;

        float currentX = x;

        if (maxWidth > 0) {
            int totalWidth = font.width(text);
            if (suffix != null) totalWidth += font.width(suffix);
            currentX += (maxWidth - totalWidth) / 2.0f;
        }

        if (theme == EnchantmentTheme.LAVENDER) {
            renderEdenStyle(font, currentX, y, matrix, bufferSource, milliTime);
            currentX += font.width(text);
        } else {
            renderNormalStyle(font, currentX, y, matrix, bufferSource, timeSeconds);
            currentX += font.width(text);
        }

        if (suffix != null) {
            font.drawInBatch(suffix.getVisualOrderText(), currentX, y, 0xFFFFFFFF, true, matrix, bufferSource, Font.DisplayMode.NORMAL, 0, 15728880);
        }
    }

    /**
     * 效果: 全局飘荡 + 局部波浪 + 呼吸透明度
     */
    private void renderEdenStyle(Font font, float startX, float startY, Matrix4f matrix, MultiBufferSource bufferSource, long milliTime) {
        float posX = startX;

        float globalXOffset = Mth.cos((float) milliTime * 0.000833F);

        int baseColor = theme.getPrimaryColor();
        baseColor = baseColor | 0xFF000000;

        for (int i = 0; i < rawString.length(); i++) {
            char c = rawString.charAt(i);
            String s = String.valueOf(c);
            int charWidth = font.width(s);

            if (c == ' ') {
                posX += charWidth;
                continue;
            }

            float yOffset = Mth.sin((i * 0.5F + (float) milliTime * 0.00166F));

            int alpha = (int) (Mth.clamp((Mth.abs(Mth.cos(i * 0.2F + (float) milliTime / 720F)) * 255), 100, 255));
            int colorWithAlpha = (baseColor & 0x00FFFFFF) | (alpha << 24);

            font.drawInBatch(s,
                    posX + globalXOffset,
                    startY + yOffset,
                    colorWithAlpha,
                    true,
                    matrix,
                    bufferSource,
                    Font.DisplayMode.NORMAL,
                    0,
                    15728880);

            posX += charWidth;
        }
    }

    /**
     * 普通风格渲染<br>
     * 效果: 抖动 + 彩虹色/渐变
     */
    private void renderNormalStyle(Font font, float startX, float startY, Matrix4f matrix, MultiBufferSource bufferSource, double timeSeconds) {
        float currentX = startX;

        for (int i = 0; i < rawString.length(); i++) {
            char c = rawString.charAt(i);
            String s = String.valueOf(c);
            int charWidth = font.width(s);

            if (c == ' ') {
                currentX += charWidth;
                continue;
            }

            float offsetX = 0;
            float offsetY = 0;
            if (shouldShake) {
                float angle = (float) ((timeSeconds * 3.0 + i * 0.3) % (Math.PI * 2));
                offsetX = Mth.sin(angle) * 0.65f;
                offsetY = Mth.cos(angle) * 0.65f;
            }

            int color;
            if (theme == EnchantmentTheme.MIRACLE) {
                float hue = (float) ((timeSeconds * 0.2 + i * 0.05) % 1.0);
                color = Color.HSBtoRGB(hue, 0.6f, 1.0f);
            } else if (theme == EnchantmentTheme.LOVE_BLUE) {
                double colorT = (Math.sin(timeSeconds * 5.0 - i * 0.1) + 1.0) / 2.0;
                color = lerpColor(theme.getPrimaryColor(), theme.getSecondaryColor(), (float) colorT);
            } else {
                double colorT = (Math.sin(timeSeconds * 2.0 - i * 0.1) + 1.0) / 2.0;
                color = lerpColor(theme.getPrimaryColor(), theme.getSecondaryColor(), (float) colorT);
            }

            if (theme == EnchantmentTheme.MIRACLE && shouldShake) {
                int ghostColor = (color & 0x00FFFFFF) | 0x44000000;
                font.drawInBatch(s, currentX + offsetX + 0.5f, startY + offsetY + 0.5f, ghostColor, false, matrix, bufferSource, Font.DisplayMode.NORMAL, 0, 15728880);
            }

            font.drawInBatch(s, currentX + offsetX, startY + offsetY, color, true, matrix, bufferSource, Font.DisplayMode.NORMAL, 0, 15728880);
            currentX += charWidth;
        }
    }

    private int lerpColor(int color1, int color2, float t) {
        int r1 = (color1 >> 16) & 0xFF;
        int g1 = (color1 >> 8) & 0xFF;
        int b1 = color1 & 0xFF;
        int r2 = (color2 >> 16) & 0xFF;
        int g2 = (color2 >> 8) & 0xFF;
        int b2 = color2 & 0xFF;
        int r = (int) (r1 + (r2 - r1) * t);
        int g = (int) (g1 + (g2 - g1) * t);
        int b = (int) (b1 + (b2 - b1) * t);
        return (r << 16) | (g << 8) | b;
    }
}
