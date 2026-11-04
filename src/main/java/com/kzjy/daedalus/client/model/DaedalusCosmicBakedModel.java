package com.kzjy.daedalus.client.model;

import com.kzjy.daedalus.client.DaedalusRenderTypes;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.ShaderInstance;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.inventory.InventoryMenu;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.client.model.BakedModelWrapper;

import java.util.ArrayList;
import java.util.List;

public class DaedalusCosmicBakedModel extends BakedModelWrapper<BakedModel> {
    public static final float[] COSMIC_UVS = new float[40];
    private final List<ResourceLocation> maskSprite;
    private final boolean isNeo;
    private final int neoType;

    public DaedalusCosmicBakedModel(BakedModel wrapped, List<ResourceLocation> maskSprite, boolean isNeo, int neoType) {
        super(wrapped);
        this.maskSprite = maskSprite;
        this.isNeo = isNeo;
        this.neoType = neoType;
    }

    public void renderCosmicEffect(ItemStack stack, PoseStack pStack, MultiBufferSource source, int light, int overlay, float yaw, float pitch, float scale) {
        ShaderInstance shaderInstance = isNeo ? DaedalusRenderTypes.cosmicNeoShader : DaedalusRenderTypes.cosmicShader;
        RenderType renderType = isNeo ? DaedalusRenderTypes.COSMIC_NEO : DaedalusRenderTypes.DAEDALUS_COSMIC;

        if (shaderInstance != null) {
            safeSetFloat(shaderInstance, "time", (System.currentTimeMillis() % 200000L) / 2000.0F);
            safeSetFloat(shaderInstance, "yaw", yaw);
            safeSetFloat(shaderInstance, "pitch", pitch);
            safeSetFloat(shaderInstance, "externalScale", scale);
            safeSetFloat(shaderInstance, "opacity", 1.0F);

            if (shaderInstance.getUniform("useCosmicType") != null) {
                shaderInstance.getUniform("useCosmicType").set(neoType);
            }
            if (shaderInstance.getUniform("screenSize") != null) {
                Minecraft mc = Minecraft.getInstance();
                shaderInstance.getUniform("screenSize").set((float)mc.getWindow().getWidth(), (float)mc.getWindow().getHeight());
            }

            for (int i = 0; i < 10; ++i) {
                TextureAtlasSprite sprite = Minecraft.getInstance().getTextureAtlas(InventoryMenu.BLOCK_ATLAS)
                        .apply(ResourceLocation.fromNamespaceAndPath("minecraft", "misc/cosmic_" + i));
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

    private void safeSetFloat(ShaderInstance shader, String name, float val) {
        if (shader.getUniform(name) != null) {
            shader.getUniform(name).set(val);
        }
    }
}
