#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 24: 照抄原版示例修复渲染 + 印象派字体重绘
"""
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SRC = P / "src/main/java/com/kzjy/daedalus"
RES = P / "src/main/resources"

print("=" * 60)
print("Round 24: 纯净渲染 + 字体印象变色")
print("=" * 60)

def write_java(rel, content):
    p = SRC / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[重写] {rel}")

def write_res(rel, content):
    p = RES / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[写入] {rel}")

# ================= 1. 修复模型渲染（照抄示例） =================

# 剑：纯 cosmic，不使用 halo
write_res("assets/daedalus/models/item/love_poem_sword.json", """{
  "parent": "minecraft:item/handheld",
  "textures": { "layer0": "daedalus:item/love_poem_sword" },
  "loader": "renderblender:cosmic",
  "cosmic": { "mask": "daedalus:item/love_poem_sword" }
}
""")

# 附魔书：纯 cosmic
write_res("assets/minecraft/models/item/enchanted_book.json", """{
  "parent": "minecraft:item/generated",
  "textures": { "layer0": "minecraft:item/enchanted_book" },
  "loader": "renderblender:cosmic",
  "cosmic": { "mask": "minecraft:item/enchanted_book" }
}
""")

write_res("assets/daedalus/models/item/daedalus_enchanted_book.json", """{
  "parent": "minecraft:item/generated",
  "textures": { "layer0": "daedalus:item/daedalus_enchanted_book" },
  "loader": "renderblender:cosmic",
  "cosmic": { "mask": "daedalus:item/daedalus_enchanted_book" }
}
""")

# ================= 2. 重绘字体颜色与特效 =================

# 1. 修改 DaedalusTooltipData 增加 isTitle 参数
write_java("client/gui/DaedalusTooltipData.java", '''package com.kzjy.daedalus.client.gui;

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
''')

# 2. 重写 DaedalusTextRenderer，实现印象变色
write_java("client/gui/DaedalusTextRenderer.java", '''package com.kzjy.daedalus.client.gui;

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
    private final boolean isTitle;
    private final Component suffix;

    public DaedalusTextRenderer(DaedalusTooltipData data) {
        this.text = data.text().getVisualOrderText();
        this.rawString = data.text().getString();
        this.theme = data.theme();
        this.maxWidth = data.maxWidth();
        this.shouldShake = data.shouldShake();
        this.isTitle = data.isTitle();
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
            renderImpressionStyle(font, currentX, y, matrix, bufferSource, timeSeconds);
            currentX += font.width(text);
        }

        if (suffix != null) {
            font.drawInBatch(suffix.getVisualOrderText(), currentX, y, 0xFFFFFFFF, true, matrix, bufferSource, Font.DisplayMode.NORMAL, 0, 15728880);
        }
    }

    private void renderEdenStyle(Font font, float startX, float startY, Matrix4f matrix, MultiBufferSource bufferSource, long milliTime) {
        float posX = startX;
        float globalXOffset = Mth.cos((float) milliTime * 0.000833F);
        int baseColor = theme.getPrimaryColor() | 0xFF000000;

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

            font.drawInBatch(s, posX + globalXOffset, startY + yOffset, colorWithAlpha, true, matrix, bufferSource, Font.DisplayMode.NORMAL, 0, 15728880);
            posX += charWidth;
        }
    }

    /**
     * 印象变色重绘：名字高亮闪烁，简介主题波浪
     */
    private void renderImpressionStyle(Font font, float startX, float startY, Matrix4f matrix, MultiBufferSource bufferSource, double timeSeconds) {
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
                // 名字抖动更剧烈，简介抖动更平缓
                float shakeSpeed = isTitle ? 5.0f : 2.0f;
                float shakeAmount = isTitle ? 0.8f : 0.4f;
                float angle = (float) ((timeSeconds * shakeSpeed + i * 0.3) % (Math.PI * 2));
                offsetX = Mth.sin(angle) * shakeAmount;
                offsetY = Mth.cos(angle) * shakeAmount;
            }

            int color;
            if (isTitle) {
                // 名字：高亮、高饱和度闪烁，贴合主题色系
                float hueBase = getHueFromColor(theme.getPrimaryColor());
                // 在主题色相附近小幅度波动，同时亮度极高
                float hue = (float) ((hueBase + Math.sin(timeSeconds * 3.0 + i * 0.1) * 0.05) % 1.0);
                if (hue < 0) hue += 1.0f;
                color = Color.HSBtoRGB(hue, 0.9f, 1.0f);
            } else {
                // 简介：主题色的波浪渐变（主色 -> 副色）
                double colorT = (Math.sin(timeSeconds * 2.0 - i * 0.15) + 1.0) / 2.0;
                color = lerpColor(theme.getPrimaryColor(), theme.getSecondaryColor(), (float) colorT);
                
                // 如果是奇迹（彩虹）主题，则让简介也有一点彩虹感
                if (theme == EnchantmentTheme.MIRACLE) {
                    float hue = (float) ((timeSeconds * 0.2 + i * 0.05) % 1.0);
                    color = Color.HSBtoRGB(hue, 0.6f, 1.0f);
                }
            }

            // 标题加一点光晕残影
            if (isTitle && shouldShake) {
                int ghostColor = (color & 0x00FFFFFF) | 0x66000000;
                font.drawInBatch(s, currentX + offsetX + 0.5f, startY + offsetY + 0.5f, ghostColor, false, matrix, bufferSource, Font.DisplayMode.NORMAL, 0, 15728880);
            }

            font.drawInBatch(s, currentX + offsetX, startY + offsetY, color, true, matrix, bufferSource, Font.DisplayMode.NORMAL, 0, 15728880);
            currentX += charWidth;
        }
    }

    private float getHueFromColor(int rgb) {
        float[] hsb = Color.RGBtoHSB((rgb >> 16) & 0xFF, (rgb >> 8) & 0xFF, rgb & 0xFF, null);
        return hsb[0];
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
''')

# 3. 修改 DaedalusForgeClientEvents 传入 isTitle 标志
fce = SRC / "client" / "DaedalusForgeClientEvents.java"
c = fce.read_text(encoding="utf-8")
c = c.replace(
    'new DaedalusTooltipData(Component.literal(line), theme, -1, true)));',
    'new DaedalusTooltipData(Component.literal(line), theme, -1, true, isTitle)));'
)
fce.write_text(c, encoding="utf-8")
print("[修改] DaedalusForgeClientEvents.java (传入 isTitle 标志)")

print("\n下一步:")
print("  git add .")
print('  git commit -m "feat: fix cosmic rendering and implement impression tooltips"')
print("  git push")