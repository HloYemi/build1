package com.kzjy.daedalus.enchantment.util;

import net.minecraft.ChatFormatting;
import net.minecraft.client.Minecraft;
import net.minecraft.util.Mth;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.fml.loading.FMLEnvironment;
import java.awt.Color;

public enum EnchantmentTheme {
    ABYSS("深渊", 0x1E3A8A, 0x3B82F6, ChatFormatting.DARK_BLUE),
    CURSE("诅咒", 0x7E22CE, 0xC084FC, ChatFormatting.DARK_PURPLE),
    SIN("罪孽", 0x991B1B, 0xEF4444, ChatFormatting.DARK_RED),
    DIVINE("神圣", 0xFFD700, 0xFFEA00, ChatFormatting.YELLOW),
    NATURE("自然", 0x166534, 0x22C55E, ChatFormatting.DARK_GREEN),
    VOID("虚空", 0x333333, 0x888888, ChatFormatting.DARK_GRAY),
    DAEDALUS("代达罗斯", 0x78350F, 0xD97706, ChatFormatting.GOLD),
    MIRACLE("奇迹", 0xFFFFFF, 0xFFFFFF, ChatFormatting.LIGHT_PURPLE),
    LOVE_BLUE("爱之诗-蓝", 0x00BFFF, 0x1E90FF, ChatFormatting.BLUE),
    LAVENDER("爱之诗-幻", 0xB0C4DE, 0x9370DB, ChatFormatting.LIGHT_PURPLE);

    private final String chineseName;
    private final int primaryColor;
    private final int secondaryColor;
    private final ChatFormatting chatColor;

    EnchantmentTheme(String chineseName, int primaryColor, int secondaryColor, ChatFormatting chatColor) {
        this.chineseName = chineseName;
        this.primaryColor = primaryColor;
        this.secondaryColor = secondaryColor;
        this.chatColor = chatColor;
    }

    public String getChineseName() { return chineseName; }
    public int getPrimaryColor() { return primaryColor; }
    public int getSecondaryColor() { return secondaryColor; }
    public ChatFormatting getChatColor() { return chatColor; }

    public static int createGradientColor(int color1, int color2, int cycleLength) {
        return createGradientColor(color1, color2, cycleLength, null);
    }

    public static int createGradientColor(int color1, int color2, int cycleLength, EnchantmentTheme overrideTheme) {
        if (FMLEnvironment.dist == Dist.CLIENT) {
            long time = 0;
            if (Minecraft.getInstance().level != null) {
                time = Minecraft.getInstance().level.getGameTime();
            } else {
                time = System.currentTimeMillis() / 50;
            }

            if (overrideTheme == MIRACLE) {
                float hue = (time % cycleLength) / (float) cycleLength;
                return Color.HSBtoRGB(hue, 0.8f, 1.0f);
            }

            double radians = ((double) (time % cycleLength) / cycleLength) * 2 * Math.PI;
            double t = (Math.sin(radians) + 1.0) / 2.0;
            return lerpColor(color1, color2, t);
        }
        return lerpColor(color1, color2, 0.5);
    }

    private static int lerpColor(int color1, int color2, double t) {
        int r1 = (color1 >> 16) & 0xFF;
        int g1 = (color1 >> 8) & 0xFF;
        int b1 = color1 & 0xFF;
        int r2 = (color2 >> 16) & 0xFF;
        int g2 = (color2 >> 8) & 0xFF;
        int b2 = color2 & 0xFF;
        int r = (int) (r1 + (r2 - r1) * t);
        int g = (int) (g1 + (g2 - g1) * t);
        int b = (int) (b1 + (b2 - b1) * t);
        r = Mth.clamp(r, 0, 255);
        g = Mth.clamp(g, 0, 255);
        b = Mth.clamp(b, 0, 255);
        return (r << 16) | (g << 8) | b;
    }

    public int createThemeGradient(int cycleLength) {
        return createGradientColor(primaryColor, secondaryColor, cycleLength, this);
    }
}
