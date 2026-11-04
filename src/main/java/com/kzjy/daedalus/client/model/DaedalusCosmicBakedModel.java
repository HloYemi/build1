package com.kzjy.daedalus.client.model;

import com.kzjy.daedalus.client.DaedalusRenderTypes;
import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import committee.nova.mods.renderblender.api.client.model.bakedmodels.WrappedItemModel;
import committee.nova.mods.renderblender.client.shader.RBShaders;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.ShaderInstance;
import net.minecraft.client.renderer.block.model.BakedQuad;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.core.Direction;
import net.minecraft.core.Vec3i;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.RandomSource;
import net.minecraft.world.inventory.InventoryMenu;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import org.jetbrains.annotations.Nullable;
import org.joml.Vector3f;
import org.lwjgl.opengl.GL11;

import java.util.ArrayList;
import java.util.List;

public class DaedalusCosmicBakedModel extends WrappedItemModel {
    public static final float[] COSMIC_UVS = new float[40];
    private final List<ResourceLocation> maskSprite;

    private final int glowColor;
    private final float glowWidth;
    private final float glowOffset;
    private final boolean isNeo;
    private final int neoType;

    private ItemDisplayContext currentTransformType;

    public DaedalusCosmicBakedModel(BakedModel wrapped, List<ResourceLocation> maskSprite, int glowColor, float glowWidth, float glowOffset, boolean isNeo, int neoType) {
        super(wrapped);
        this.maskSprite = maskSprite;
        this.glowColor = glowColor;
        this.glowWidth = glowWidth;
        this.glowOffset = glowOffset;
        this.isNeo = isNeo;
        this.neoType = neoType;
    }

    public DaedalusCosmicBakedModel(BakedModel wrapped, List<ResourceLocation> maskSprite) {
        this(wrapped, maskSprite, 0, 0, 0, false, 0);
    }

    @Override
    public void renderItem(ItemStack stack, ItemDisplayContext transformType, PoseStack pStack, MultiBufferSource source, int light, int overlay) {
        this.currentTransformType = transformType;

        if (this.glowWidth > 0) {
            float offset = this.glowWidth * 0.008F;
            if (transformType == ItemDisplayContext.FIXED || transformType == ItemDisplayContext.GUI) {
                offset += 0.005F;
            }
            renderGlowEdge(stack, pStack, source, light, overlay, offset);
        }

        this.renderWrapped(stack, pStack, source, light, overlay, true);
        if (source instanceof MultiBufferSource.BufferSource bs) {
            bs.endBatch();
        }

        renderCosmicEffect(stack, pStack, source, light, overlay);
    }

    private void renderCosmicEffect(ItemStack stack, PoseStack pStack, MultiBufferSource source, int light, int overlay) {
        final Minecraft mc = Minecraft.getInstance();
        float yaw = 0.0f;
        float pitch = 0.0f;
        float scale = 1f;

        if (RBShaders.inventoryRender || currentTransformType == ItemDisplayContext.GUI) {
            scale = 100.0F;
        } else {
            if (mc.player != null) {
                yaw = (float) (mc.player.getYRot() * 2.0f * Math.PI / 360.0);
                pitch = -(float) (mc.player.getXRot() * 2.0f * Math.PI / 360.0);
            }
        }

        ShaderInstance shaderInstance = isNeo ? DaedalusRenderTypes.cosmicNeoShader : DaedalusRenderTypes.cosmicShader;
        RenderType renderType = isNeo ? DaedalusRenderTypes.COSMIC_NEO : DaedalusRenderTypes.DAEDALUS_COSMIC;

        if (shaderInstance != null) {
            safeSetFloat(shaderInstance, "time", (System.currentTimeMillis() % 200000L) / 2000.0F);
            safeSetFloat(shaderInstance, "yaw", yaw);
            safeSetFloat(shaderInstance, "pitch", pitch);
            safeSetFloat(shaderInstance, "externalScale", scale);
            safeSetFloat(shaderInstance, "opacity", 1.0F);

            int colorInt = 0xFFFFFF; // 可自行从主题获取
            float r = ((colorInt >> 16) & 0xFF) / 255.0f;
            float g = ((colorInt >> 8) & 0xFF) / 255.0f;
            float b = (colorInt & 0xFF) / 255.0f;

            if (shaderInstance.getUniform("baseColor") != null) {
                shaderInstance.getUniform("baseColor").set(r, g, b);
            }
            if (shaderInstance.getUniform("cosmicColor0") != null) {
                shaderInstance.getUniform("cosmicColor0").set(r, g, b, 1.0f);
            }
            if (shaderInstance.getUniform("useCosmicType") != null) {
                shaderInstance.getUniform("useCosmicType").set(neoType);
            }
            if (shaderInstance.getUniform("screenSize") != null) {
                shaderInstance.getUniform("screenSize").set((float)mc.getWindow().getWidth(), (float)mc.getWindow().getHeight());
            }

            for (int i = 0; i < 10; ++i) {
                TextureAtlasSprite sprite = Minecraft.getInstance().getTextureAtlas(InventoryMenu.BLOCK_ATLAS)
                        .apply(ResourceLocation.fromNamespaceAndPath("renderblender", "misc/cosmic_" + i));
                COSMIC_UVS[i * 4] = sprite.getU0();
                COSMIC_UVS[i * 4 + 1] = sprite.getV0();
                COSMIC_UVS[i * 4 + 2] = sprite.getU1();
                COSMIC_UVS[i * 4 + 3] = sprite.getV1();
            }
            if (shaderInstance.getUniform("cosmicuvs") != null) {
                shaderInstance.getUniform("cosmicuvs").set(COSMIC_UVS);
            }
        }

        final VertexConsumer cons = source.getBuffer(renderType);
        List<TextureAtlasSprite> atlasSprite = new ArrayList<>();
        for (ResourceLocation res : maskSprite) {
            atlasSprite.add(Minecraft.getInstance().getTextureAtlas(InventoryMenu.BLOCK_ATLAS).apply(res));
        }

        pStack.pushPose();
        pStack.translate(0.5, 0.5, 0.5);
        pStack.scale(1.002f, 1.002f, 1.002f);
        pStack.translate(-0.5, -0.5, -0.5);
        Minecraft.getInstance().getItemRenderer().renderQuadList(pStack, cons, bakeItem(atlasSprite), stack, light, overlay);
        pStack.popPose();
    }

    private void renderGlowEdge(ItemStack stack, PoseStack pStack, MultiBufferSource source, int light, int overlay, float offset) {
        float r = ((glowColor >> 16) & 0xFF) / 255.0f;
        float g = ((glowColor >> 8) & 0xFF) / 255.0f;
        float b = (glowColor & 0xFF) / 255.0f;
        float a = ((glowColor >> 24) & 0xFF) / 255.0f;
        if (a == 0) a = 1.0f;

        ShaderInstance glowShader = DaedalusRenderTypes.glowEdgeShader;
        if (glowShader != null) {
            if (glowShader.getUniform("uColor") != null) glowShader.getUniform("uColor").set(r, g, b, a);
            if (glowShader.getUniform("uType") != null) glowShader.getUniform("uType").set(1);
            if (glowShader.getUniform("time") != null) glowShader.getUniform("time").set((System.currentTimeMillis() % 200000L) / 1000.0F);
            if (glowShader.getUniform("screenSize") != null) {
                Minecraft mc = Minecraft.getInstance();
                glowShader.getUniform("screenSize").set((float)mc.getWindow().getWidth(), (float)mc.getWindow().getHeight());
            }
        }

        VertexConsumer consumer = source.getBuffer(DaedalusRenderTypes.GLOWING_OUTLINE);
        List<BakedQuad> quads = this.wrapped.getQuads(null, null, RandomSource.create());

        pStack.pushPose();
        for (Vector3f direction : new Vector3f[]{
                new Vector3f(offset, offset, offset),
                new Vector3f(-offset, offset, offset),
                new Vector3f(offset, -offset, offset),
                new Vector3f(offset, offset, -offset),
                new Vector3f(-offset, -offset, offset),
                new Vector3f(-offset, offset, -offset),
                new Vector3f(offset, -offset, -offset),
                new Vector3f(-offset, -offset, -offset)
        }) {
            pStack.pushPose();
            pStack.translate(direction.x(), direction.y(), direction.z());
            PoseStack.Pose pose = pStack.last();
            for (BakedQuad quad : quads) {
                consumer.putBulkData(pose, quad, r, g, b, a, light, overlay, true);
            }
            pStack.popPose();
        }
        pStack.popPose();
    }

    private void safeSetFloat(ShaderInstance shader, String name, float val) {
        if (shader.getUniform(name) != null) {
            shader.getUniform(name).set(val);
        }
    }
}
