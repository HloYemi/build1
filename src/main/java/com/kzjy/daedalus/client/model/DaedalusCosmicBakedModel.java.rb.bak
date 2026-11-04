package com.kzjy.daedalus.client.model;

import com.kzjy.daedalus.client.DaedalusRenderTypes;
import com.kzjy.daedalus.client.renderer.DaedalusGlowRenderer;
import com.kzjy.daedalus.enchantment.DaedalusBaseEnchantment;
import com.kzjy.daedalus.enchantment.util.EnchantmentTheme;
import com.kzjy.daedalus.registry.DaedalusRegistries;
import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import committee.nova.mods.renderblender.RenderBlenderLib;
import committee.nova.mods.renderblender.api.client.model.PerspectiveModelState;
import committee.nova.mods.renderblender.api.client.model.bakedmodels.WrappedItemModel;
import committee.nova.mods.renderblender.api.client.util.TransformUtils;
import committee.nova.mods.renderblender.api.iface.IBowTransform;
import committee.nova.mods.renderblender.api.iface.IToolTransform;
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
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.EnchantmentHelper;
import org.jetbrains.annotations.Nullable;
import org.joml.Vector3f;
import org.lwjgl.opengl.GL11;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class DaedalusCosmicBakedModel extends WrappedItemModel {
    public static final float[] COSMIC_UVS = new float[40];
    private final List<ResourceLocation> maskSprite;

    private final int glowColor;
    private final float glowWidth;
    private final float glowOffset;

    private final boolean isNeo;
    private final int neoType;

    private ItemDisplayContext currentTransformType;

    public DaedalusCosmicBakedModel(final BakedModel wrapped, final List<ResourceLocation> maskSprite, int glowColor, float glowWidth, float glowOffset, boolean isNeo, int neoType) {
        super(wrapped);
        this.maskSprite = maskSprite;
        this.glowColor = glowColor;
        this.glowWidth = glowWidth;
        this.glowOffset = glowOffset;
        this.isNeo = isNeo;
        this.neoType = neoType;
    }

    public DaedalusCosmicBakedModel(final BakedModel wrapped, final List<ResourceLocation> maskSprite) {
        this(wrapped, maskSprite, 0, 0, 0, false, 0);
    }

    @Override
    public void renderItem(ItemStack stack, ItemDisplayContext transformType, PoseStack pStack, MultiBufferSource source, int light, int overlay) {
        this.currentTransformType = transformType;

        if (stack.getItem() instanceof IToolTransform) {
            this.parentState = TransformUtils.DEFAULT_TOOL;
        } else if (stack.getItem() instanceof IBowTransform) {
            this.parentState = TransformUtils.DEFAULT_BOW;
        } else{
            this.parentState = TransformUtils.DEFAULT_ITEM;
        }

        // 1. 渲染 Glow Edge Shader 描边
        if (this.glowWidth > 0) {
            float offset = this.glowWidth * 0.008F;
            if (transformType == ItemDisplayContext.FIXED || transformType == ItemDisplayContext.GUI) {
                offset += 0.005F;
            }
            renderGlowEdge(stack, pStack, source, light, overlay, offset);
        }

        // 2. 渲染基础模型
        this.renderWrapped(stack, pStack, source, light, overlay, true);
        if (source instanceof MultiBufferSource.BufferSource bs) {
            bs.endBatch();
        }

        // 3. 渲染星空特效 Mask
        renderCosmicEffect(stack, pStack, source, light, overlay);

        // 4. 渲染程序化彩虹光晕 (Love Poem Sword)
        boolean shouldRenderProceduralGlow = transformType == ItemDisplayContext.GUI ||
                transformType == ItemDisplayContext.FIXED ||
                transformType == ItemDisplayContext.GROUND;

        if (stack.getItem() == DaedalusRegistries.LOVE_POEM_SWORD.get() && shouldRenderProceduralGlow) {
            DaedalusGlowRenderer.render(pStack, source, transformType);
        }
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

        EnchantmentTheme theme = EnchantmentTheme.VOID;
        boolean isMiracle = false;
        boolean hasEnchantment = false;

        Map<Enchantment, Integer> enchantments = EnchantmentHelper.getEnchantments(stack);
        for (Enchantment ench : enchantments.keySet()) {
            if (ench instanceof DaedalusBaseEnchantment daedalusEnch) {
                theme = daedalusEnch.getTheme();
                hasEnchantment = true;
                if (theme == EnchantmentTheme.MIRACLE) {
                    isMiracle = true;
                }
                break;
            }
        }

        if (!hasEnchantment && stack.getItem() == DaedalusRegistries.LOVE_POEM_SWORD.get()) {
            theme = EnchantmentTheme.MIRACLE;
            isMiracle = true;
        }

        ShaderInstance shaderInstance = isNeo ? DaedalusRenderTypes.cosmicNeoShader : DaedalusRenderTypes.cosmicShader;
        RenderType renderType = isNeo ? DaedalusRenderTypes.COSMIC_NEO : DaedalusRenderTypes.DAEDALUS_COSMIC;

        if (shaderInstance != null) {
            safeSetFloat(shaderInstance, "time", (System.currentTimeMillis() % 200000L) / 2000.0F);
            safeSetFloat(shaderInstance, "yaw", yaw);
            safeSetFloat(shaderInstance, "pitch", pitch);
            safeSetFloat(shaderInstance, "externalScale", scale);
            safeSetFloat(shaderInstance, "opacity", 1.0F);

            int colorInt;
            if (isMiracle) {
                colorInt = EnchantmentTheme.createGradientColor(0, 0, 120, EnchantmentTheme.MIRACLE);
            } else {
                colorInt = theme.getSecondaryColor();
            }
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
                        .apply(RenderBlenderLib.rl("misc/cosmic_" + i));
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

            Minecraft mc = Minecraft.getInstance();
            float yaw = 0.0f;
            float pitch = 0.0f;
            if (mc.player != null) {
                yaw = (float) (mc.player.getYRot() * Math.PI / 180.0);
                pitch = (float) (mc.player.getXRot() * Math.PI / 180.0);
            }
            if (glowShader.getUniform("yaw") != null) glowShader.getUniform("yaw").set(yaw);
            if (glowShader.getUniform("pitch") != null) glowShader.getUniform("pitch").set(pitch);
        }

        VertexConsumer consumer = source.getBuffer(DaedalusRenderTypes.GLOWING_OUTLINE);

        RenderSystem.assertOnRenderThread();
        boolean depthTestEnabled = GL11.glIsEnabled(GL11.GL_DEPTH_TEST);
        int depthFunc = GL11.glGetInteger(GL11.GL_DEPTH_FUNC);

        try {
            GL11.glEnable(GL11.GL_DEPTH_TEST);
            GL11.glDepthFunc(GL11.GL_LEQUAL);
            RenderSystem.enableBlend();
            RenderSystem.defaultBlendFunc();
            RenderSystem.colorMask(true, true, true, true);

            Vector3f[] directions = new Vector3f[]{
                    new Vector3f(offset, offset, offset),
                    new Vector3f(-offset, offset, offset),
                    new Vector3f(offset, -offset, offset),
                    new Vector3f(offset, offset, -offset),
                    new Vector3f(-offset, -offset, offset),
                    new Vector3f(-offset, offset, -offset),
                    new Vector3f(offset, -offset, -offset),
                    new Vector3f(-offset, -offset, -offset)
            };

            List<BakedQuad> quads = this.wrapped.getQuads(null, null, RandomSource.create());

            pStack.pushPose();
            if (currentTransformType == ItemDisplayContext.FIXED) {
                pStack.translate(0, 0, 0.05F);
            }

            for (Vector3f direction : directions) {
                pStack.pushPose();
                pStack.translate(direction.x(), direction.y(), direction.z());
                PoseStack.Pose pose = pStack.last();
                for (BakedQuad quad : quads) {
                    if (shouldRenderQuad(quad, direction)) {
                        consumer.putBulkData(pose, quad, r, g, b, a, light, overlay, true);
                    }
                }
                pStack.popPose();
            }
            pStack.popPose();

        } finally {
            if (depthTestEnabled) {
                GL11.glEnable(GL11.GL_DEPTH_TEST);
            } else {
                GL11.glDisable(GL11.GL_DEPTH_TEST);
            }
            GL11.glDepthFunc(depthFunc);
        }
    }

    private boolean shouldRenderQuad(BakedQuad quad, Vector3f offsetDirection) {
        Direction quadDirection = quad.getDirection();
        Vec3i quadNormal = quadDirection.getNormal();
        float dotProduct = offsetDirection.x() * (float)quadNormal.getX() +
                offsetDirection.y() * (float)quadNormal.getY() +
                offsetDirection.z() * (float)quadNormal.getZ();
        return dotProduct > 0.0F;
    }

    private void safeSetFloat(ShaderInstance shader, String name, float val) {
        if (shader.getUniform(name) != null) {
            shader.getUniform(name).set(val);
        }
    }

    @Override
    public @Nullable PerspectiveModelState getModelState() {
        return (PerspectiveModelState) this.parentState;
    }

    @Override
    public boolean isCosmic() {
        return true;
    }
}
