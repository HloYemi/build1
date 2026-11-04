package com.kzjy.daedalus.client.renderer;

import com.kzjy.daedalus.Daedalus;
import com.kzjy.daedalus.client.DaedalusRenderTypes;
import com.mojang.blaze3d.platform.GlStateManager;
import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.mojang.math.Axis;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemDisplayContext;
import org.joml.Matrix3f;
import org.joml.Matrix4f;

import java.awt.Color;
import java.util.Random;

public class DaedalusGlowRenderer {
    private static final ResourceLocation GR_GLOW = new ResourceLocation(Daedalus.MODID, "textures/misc/gr.png");
    private static final ResourceLocation MAP_GLOW = new ResourceLocation(Daedalus.MODID, "textures/misc/gr_m.png");
    private static final Random RANDOM = new Random(432L);

    public static void render(PoseStack poseStack, MultiBufferSource bufferSource, ItemDisplayContext displayContext) {
        poseStack.pushPose();
        poseStack.translate(0.5F, 0.5F, 0.5F);

        if (displayContext == ItemDisplayContext.GROUND) {
            poseStack.scale(1.5F, 1.5F, 1.5F);
        }

        RenderSystem.enableBlend();
        RenderSystem.blendFunc(GlStateManager.SourceFactor.SRC_ALPHA, GlStateManager.DestFactor.ONE);
        RenderSystem.disableDepthTest();
        RenderSystem.disableCull();

        VertexConsumer vertexConsumer;
        if (displayContext == ItemDisplayContext.GUI) {
            vertexConsumer = bufferSource.getBuffer(DaedalusRenderTypes.GR_GLOW_NO_DEPTH);
        } else {
            vertexConsumer = bufferSource.getBuffer(DaedalusRenderTypes.GR_GLOW_DEPTH);
        }

        float time = (System.currentTimeMillis() % 200000L) / 1000.0F;

        int layers = 5;
        for (int i = 0; i < layers; i++) {
            poseStack.pushPose();

            float rotX = (i * 72F) + (time * 2F);
            float rotY = (i * 45F) + (time * 1.5F);
            float rotZ = (i * 30F);

            poseStack.mulPose(Axis.XP.rotationDegrees(rotX));
            poseStack.mulPose(Axis.YP.rotationDegrees(rotY));
            poseStack.mulPose(Axis.ZP.rotationDegrees(rotZ));

            renderRays(poseStack, vertexConsumer, time, i);

            poseStack.popPose();
        }

        poseStack.pushPose();
        poseStack.mulPose(Axis.YP.rotationDegrees(time * 20.0F));
        poseStack.mulPose(Axis.XP.rotationDegrees(time * 15.0F));

        VertexConsumer ringConsumer = bufferSource.getBuffer(DaedalusRenderTypes.GR_GLOW_DEPTH_2);
        renderRingWave(poseStack, ringConsumer, time);
        poseStack.popPose();

        RenderSystem.enableCull();
        RenderSystem.enableDepthTest();
        RenderSystem.disableBlend();
        RenderSystem.defaultBlendFunc();

        poseStack.popPose();
    }

    private static void renderRays(PoseStack poseStack, VertexConsumer vertexConsumer, float time, int layerIndex) {
        int rayCount = 6 + (layerIndex % 3);
        float rayLength = 1.1F;
        float minWidth = 0.05F;
        float maxWidth = 0.35F;

        for (int i = 0; i < rayCount; ++i) {
            float angle = time * (1.0F + layerIndex * 0.2F) + (float) ((i * 2) * Math.PI / rayCount);
            poseStack.pushPose();
            poseStack.mulPose(Axis.ZP.rotation(angle));

            ColorInfo colorInfo = generateTimeBasedColor(time, i + layerIndex * 10, 20);
            renderGlowRay(poseStack, vertexConsumer, rayLength, minWidth, maxWidth, colorInfo);

            poseStack.popPose();
        }
    }

    private static void renderRingWave(PoseStack poseStack, VertexConsumer vertexConsumer, float time) {
        Matrix4f matrix = poseStack.last().pose();
        Matrix3f normal = poseStack.last().normal();

        int alpha = 150;
        int segments = 32;

        for (int i = 0; i < segments; ++i) {
            ColorInfo colorInfo = generateTimeBasedColor(time, i, segments);
            int nextI = (i + 1) % segments;

            float angle1 = (float) ((Math.PI * 2D) * i / segments);
            float angle2 = (float) ((Math.PI * 2D) * nextI / segments);

            float offset1 = calculateWaveOffset(time * 5.0F, i);
            float offset2 = calculateWaveOffset(time * 5.0F, nextI);

            float innerRadius = 0.25F + offset1 * 0.5F;
            float outerRadius = 0.55F + offset1 * 0.5F;
            float innerRadiusNext = 0.25F + offset2 * 0.5F;
            float outerRadiusNext = 0.55F + offset2 * 0.5F;

            float innerX1 = (float) (innerRadius * Math.cos(angle1));
            float innerY1 = (float) (innerRadius * Math.sin(angle1));
            float outerX1 = (float) (outerRadius * Math.cos(angle1));
            float outerY1 = (float) (outerRadius * Math.sin(angle1));

            float innerX2 = (float) (innerRadiusNext * Math.cos(angle2));
            float innerY2 = (float) (innerRadiusNext * Math.sin(angle2));
            float outerX2 = (float) (outerRadiusNext * Math.cos(angle2));
            float outerY2 = (float) (outerRadiusNext * Math.sin(angle2));

            addVertexWithColor(vertexConsumer, matrix, normal, innerX1, innerY1, 0.0F, 0.0F, 0.0F, colorInfo.r1, colorInfo.g1, colorInfo.b1, alpha);
            addVertexWithColor(vertexConsumer, matrix, normal, outerX1, outerY1, 0.0F, 1.0F, 0.0F, colorInfo.r1, colorInfo.g1, colorInfo.b1, alpha);
            addVertexWithColor(vertexConsumer, matrix, normal, innerX2, innerY2, 0.0F, 0.0F, 1.0F, colorInfo.r1, colorInfo.g1, colorInfo.b1, alpha);
            addVertexWithColor(vertexConsumer, matrix, normal, outerX1, outerY1, 0.0F, 1.0F, 0.0F, colorInfo.r1, colorInfo.g1, colorInfo.b1, alpha);
            addVertexWithColor(vertexConsumer, matrix, normal, outerX2, outerY2, 0.0F, 1.0F, 1.0F, colorInfo.r1, colorInfo.g1, colorInfo.b1, alpha);
            addVertexWithColor(vertexConsumer, matrix, normal, innerX2, innerY2, 0.0F, 0.0F, 1.0F, colorInfo.r1, colorInfo.g1, colorInfo.b1, alpha);
        }
    }

    private static float calculateWaveOffset(float time, int index) {
        return (float) (Math.sin(time * 3.5F + index * 1.0F) * 0.17F +
                Math.sin(time * 3.0F + index * 0.5F) * 0.13F);
    }

    private static ColorInfo generateTimeBasedColor(float time, int index, int count) {
        float colorPhaseOffset = (float) (index * 360.0 / count);
        float hue1 = (time * 50.0F + colorPhaseOffset) % 360.0F;
        float hue2 = (time * 50.0F + colorPhaseOffset + 60.0F) % 360.0F;

        int color1 = Color.HSBtoRGB(hue1 / 360.0F, 1.0F, 1.0F);
        int color2 = Color.HSBtoRGB(hue2 / 360.0F, 1.0F, 1.0F);

        return new ColorInfo(
                (color1 >> 16) & 255, (color1 >> 8) & 255, color1 & 255,
                (color2 >> 16) & 255, (color2 >> 8) & 255, color2 & 255
        );
    }

    private static void renderGlowRay(PoseStack poseStack, VertexConsumer vertexConsumer, float length, float minWidth, float maxWidth, ColorInfo color) {
        Matrix4f matrix = poseStack.last().pose();
        Matrix3f normal = poseStack.last().normal();

        float x1 = -minWidth / 2.0F;
        float x2 = minWidth / 2.0F;
        float x3 = maxWidth / 2.0F;
        float x4 = -maxWidth / 2.0F;

        int alpha = 60;

        addVertexWithColor(vertexConsumer, matrix, normal, x1, 0.0F, 0.0F, 0.0F, 1.0F, color.r1, color.g1, color.b1, alpha);
        addVertexWithColor(vertexConsumer, matrix, normal, x2, 0.0F, 0.0F, 1.0F, 1.0F, color.r1, color.g1, color.b1, alpha);
        addVertexWithColor(vertexConsumer, matrix, normal, x3, length, 0.0F, 1.0F, 0.0F, color.r2, color.g2, color.b2, 0);

        addVertexWithColor(vertexConsumer, matrix, normal, x1, 0.0F, 0.0F, 0.0F, 1.0F, color.r1, color.g1, color.b1, alpha);
        addVertexWithColor(vertexConsumer, matrix, normal, x3, length, 0.0F, 1.0F, 0.0F, color.r2, color.g2, color.b2, 0);
        addVertexWithColor(vertexConsumer, matrix, normal, x4, length, 0.0F, 0.0F, 0.0F, color.r2, color.g2, color.b2, 0);
    }

    private static void addVertexWithColor(VertexConsumer vertexConsumer, Matrix4f matrix, Matrix3f normal, float x, float y, float z, float u, float v, int r, int g, int b, int alpha) {
        vertexConsumer.vertex(matrix, x, y, z)
                .color(r, g, b, alpha)
                .uv(u, v)
                .overlayCoords(240, 240)
                .uv2(240, 240)
                .normal(normal, 0.0F, 1.0F, 0.0F)
                .endVertex();
    }

    private record ColorInfo(int r1, int g1, int b1, int r2, int g2, int b2) {}
}
