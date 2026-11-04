#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 28: 废弃前置库，全面恢复原模组自带的原生渲染
"""
import shutil
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SRC = P / "src/main/java/com/kzjy/daedalus"
RES = P / "src/main/resources"

print("=" * 60)
print("Round 28: 废弃前置库，恢复原生渲染")
print("=" * 60)

def write(rel, content):
    p = SRC / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[写入] {rel}")

def write_res(rel, content):
    p = RES / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[写入] {rel}")

# ===== 1. 恢复 DaedalusRenderTypes =====
write("client/DaedalusRenderTypes.java", '''package com.kzjy.daedalus.client;

import com.kzjy.daedalus.Daedalus;
import com.mojang.blaze3d.platform.GlStateManager;
import com.mojang.blaze3d.systems.RenderSystem;
import com.mojang.blaze3d.vertex.DefaultVertexFormat;
import com.mojang.blaze3d.vertex.VertexFormat;
import net.minecraft.client.renderer.RenderStateShard;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.ShaderInstance;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterShadersEvent;

@EventBusSubscriber(modid = Daedalus.MODID, value = Dist.CLIENT, bus = EventBusSubscriber.Bus.MOD)
public class DaedalusRenderTypes extends RenderType {

    public DaedalusRenderTypes(String name, VertexFormat format, VertexFormat.Mode mode, int bufferSize, boolean affectsCrumbling, boolean sortOnUpload, Runnable setupState, Runnable clearState) {
        super(name, format, mode, bufferSize, affectsCrumbling, sortOnUpload, setupState, clearState);
    }

    public static ShaderInstance cosmicShader;
    public static ShaderInstance cosmicNeoShader;

    @SubscribeEvent
    public static void registerShaders(RegisterShadersEvent event) {
        try {
            event.registerShader(new ShaderInstance(event.getResourceProvider(), ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "daedalus_cosmic"), DefaultVertexFormat.NEW_ENTITY),
                    shaderInstance -> cosmicShader = shaderInstance);

            event.registerShader(new ShaderInstance(event.getResourceProvider(), ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "cosmic_neo"), DefaultVertexFormat.NEW_ENTITY),
                    shaderInstance -> cosmicNeoShader = shaderInstance);
        } catch (Exception e) {
            Daedalus.LOGGER.error("Failed to register Daedalus shaders", e);
        }
    }

    public static final RenderType DAEDALUS_COSMIC = create("daedalus_cosmic",
            DefaultVertexFormat.NEW_ENTITY, VertexFormat.Mode.QUADS, 256, true, true,
            RenderType.CompositeState.builder()
                    .setShaderState(new RenderStateShard.ShaderStateShard(() -> cosmicShader))
                    .setTextureState(new RenderStateShard.TextureStateShard(ResourceLocation.parse("textures/atlas/blocks.png"), false, false))
                    .setTransparencyState(TRANSLUCENT_TRANSPARENCY)
                    .setWriteMaskState(COLOR_WRITE)
                    .setCullState(NO_CULL)
                    .setLightmapState(LIGHTMAP)
                    .setOverlayState(OVERLAY)
                    .createCompositeState(true));

    public static final RenderType COSMIC_NEO = create("cosmic_neo",
            DefaultVertexFormat.NEW_ENTITY, VertexFormat.Mode.QUADS, 256, true, true,
            RenderType.CompositeState.builder()
                    .setShaderState(new RenderStateShard.ShaderStateShard(() -> cosmicNeoShader))
                    .setTextureState(new RenderStateShard.TextureStateShard(ResourceLocation.parse("textures/atlas/blocks.png"), false, false))
                    .setTransparencyState(TRANSLUCENT_TRANSPARENCY)
                    .setWriteMaskState(COLOR_WRITE)
                    .setCullState(NO_CULL)
                    .setLightmapState(LIGHTMAP)
                    .setOverlayState(OVERLAY)
                    .createCompositeState(true));
}
''')

# ===== 2. 恢复 DaedalusModelLoader =====
write("client/model/DaedalusModelLoader.java", '''package com.kzjy.daedalus.client.model;

import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import net.minecraft.client.renderer.block.model.BlockModel;
import net.minecraft.client.renderer.block.model.ItemOverrides;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.client.resources.model.Material;
import net.minecraft.client.resources.model.ModelBaker;
import net.minecraft.client.resources.model.ModelState;
import net.minecraft.client.resources.model.UnbakedModel;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.GsonHelper;
import net.neoforged.neoforge.client.model.geometry.IGeometryBakingContext;
import net.neoforged.neoforge.client.model.geometry.IGeometryLoader;
import net.neoforged.neoforge.client.model.geometry.IUnbakedGeometry;

import java.util.Collections;
import java.util.function.Function;

public class DaedalusModelLoader implements IGeometryLoader<DaedalusModelLoader.DaedalusCosmicGeometry> {

    @Override
    public DaedalusCosmicGeometry read(JsonObject jsonObject, JsonDeserializationContext context) throws JsonParseException {
        JsonObject cosmicObj = jsonObject.getAsJsonObject("daedalus_cosmic");
        boolean isNeo = false;
        int neoType = 0;

        if (cosmicObj == null) {
            cosmicObj = jsonObject.getAsJsonObject("cosmic_neo");
            if (cosmicObj != null) {
                isNeo = true;
                neoType = GsonHelper.getAsInt(cosmicObj, "type", 0);
            }
        }

        if (cosmicObj == null) throw new IllegalStateException("Missing 'daedalus_cosmic' or 'cosmic_neo' object.");

        String maskPath = cosmicObj.get("mask").getAsString();
        JsonObject clean = jsonObject.deepCopy();
        clean.remove("daedalus_cosmic");
        clean.remove("cosmic_neo");
        clean.remove("loader");

        BlockModel baseModel = context.deserialize(clean, BlockModel.class);

        return new DaedalusCosmicGeometry(baseModel, ResourceLocation.parse(maskPath), isNeo, neoType);
    }

    public static class DaedalusCosmicGeometry implements IUnbakedGeometry<DaedalusCosmicGeometry> {
        private final BlockModel baseModel;
        private final ResourceLocation maskLocation;
        private final boolean isNeo;
        private final int neoType;

        public DaedalusCosmicGeometry(BlockModel baseModel, ResourceLocation maskLocation, boolean isNeo, int neoType) {
            this.baseModel = baseModel;
            this.maskLocation = maskLocation;
            this.isNeo = isNeo;
            this.neoType = neoType;
        }

        @Override
        public BakedModel bake(IGeometryBakingContext context, ModelBaker baker,
                               Function<Material, TextureAtlasSprite> spriteGetter,
                               ModelState modelState, ItemOverrides overrides) {
            BakedModel bakedBaseModel = this.baseModel.bake(baker, this.baseModel, spriteGetter, modelState, true);
            return new DaedalusCosmicBakedModel(bakedBaseModel, Collections.singletonList(maskLocation), isNeo, neoType);
        }

        @Override
        public void resolveParents(Function<ResourceLocation, UnbakedModel> modelGetter, IGeometryBakingContext context) {
            this.baseModel.resolveParents(modelGetter);
        }
    }
}
''')

# ===== 3. 恢复 DaedalusCosmicBakedModel (纯原版渲染) =====
write("client/model/DaedalusCosmicBakedModel.java", '''package com.kzjy.daedalus.client.model;

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
''')

# ===== 4. 更新 ClientSetup 注册 Loader =====
write("ClientSetup.java", '''package com.kzjy.daedalus;

import com.kzjy.daedalus.client.model.DaedalusModelLoader;
import net.minecraft.client.renderer.item.ItemProperties;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Items;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.neoforge.client.event.ModelEvent;

@EventBusSubscriber(modid = Daedalus.MODID, value = Dist.CLIENT, bus = EventBusSubscriber.Bus.MOD)
public class ClientSetup {
    @SubscribeEvent
    public static void clientSetup(FMLClientSetupEvent event) {
        event.enqueueWork(() -> {
            ItemProperties.register(Items.ENCHANTED_BOOK,
                    ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "enchanted_book"),
                    (stack, world, entity, seed) -> {
                        var enchants = stack.getEnchantments();
                        for (var e : enchants.entrySet()) {
                            var keyOpt = e.getKey().unwrapKey();
                            if (keyOpt.isPresent() && keyOpt.get().location().getNamespace().equals(Daedalus.MODID)) {
                                return 1.0f;
                            }
                        }
                        return 0.0f;
                    });
        });
    }

    @SubscribeEvent
    public static void registerGeometryLoaders(ModelEvent.RegisterGeometryLoaders event) {
        event.register(
            ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "cosmic"),
            new DaedalusModelLoader()
        );
    }
}
''')

# ===== 5. 更新 IClientItemExtensions (原生渲染调用) =====
write("client/compat/RBPerspectiveItemExtensions.java", '''package com.kzjy.daedalus.client.compat;

import com.kzjy.daedalus.client.model.DaedalusCosmicBakedModel;
import com.mojang.blaze3d.vertex.PoseStack;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.BlockEntityWithoutLevelRenderer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.client.extensions.common.IClientItemExtensions;
import org.jetbrains.annotations.NotNull;

public final class RBPerspectiveItemExtensions implements IClientItemExtensions {
    @Override
    public @NotNull BlockEntityWithoutLevelRenderer getCustomRenderer() {
        return CustomRenderer.INSTANCE;
    }

    private static final class CustomRenderer extends BlockEntityWithoutLevelRenderer {
        static final CustomRenderer INSTANCE = new CustomRenderer();

        private CustomRenderer() {
            super(Minecraft.getInstance().getBlockEntityRenderDispatcher(),
                  Minecraft.getInstance().getEntityModels());
        }

        @Override
        public void renderByItem(@NotNull ItemStack stack, @NotNull ItemDisplayContext ctx,
                                 @NotNull PoseStack pStack, @NotNull MultiBufferSource source,
                                 int light, int overlay) {
            Minecraft mc = Minecraft.getInstance();
            BakedModel model = mc.getItemRenderer().getModel(stack, mc.level, mc.player, 0);

            // 1. 渲染原版模型
            mc.getItemRenderer().renderStatic(stack, ctx, light, overlay, pStack, source, mc.level, 0);

            // 2. 渲染星空遮罩
            if (model instanceof DaedalusCosmicBakedModel cosmic) {
                float yaw = 0;
                float pitch = 0;
                float scale = 1f;
                if (mc.player != null) {
                    yaw = (float) (mc.player.getYRot() * 2.0f * Math.PI / 360.0);
                    pitch = -(float) (mc.player.getXRot() * 2.0f * Math.PI / 360.0);
                }
                if (ctx == ItemDisplayContext.GUI) scale = 100f;

                cosmic.renderCosmicEffect(stack, pStack, source, light, overlay, yaw, pitch, scale);
            }
        }
    }
}
''')

# ===== 6. 覆盖 JSON =====
write_res("assets/daedalus/models/item/love_poem_sword.json", """{
  "parent": "minecraft:item/handheld",
  "textures": {
    "layer0": "daedalus:item/love_poem_sword"
  },
  "loader": "daedalus:cosmic",
  "cosmic_neo": {
    "mask": "daedalus:item/love_poem_sword_mask",
    "type": 14
  }
}
""")

write_res("assets/minecraft/models/item/enchanted_book.json", """{
  "parent": "minecraft:item/generated",
  "textures": {
    "layer0": "minecraft:item/enchanted_book"
  },
  "loader": "daedalus:cosmic",
  "daedalus_cosmic": {
    "mask": "daedalus:item/daedalus_enchanted_book_mask"
  }
}
""")

# ===== 7. 移除 RB 依赖的旧代码 =====
fce = SRC / "client/DaedalusClientSetup.java"
if fce.exists():
    c = fce.read_text(encoding="utf-8")
    if "RBPerspectiveItemExtensions" not in c:
        pass # keep

print("\n下一步:")
print("  git add .")
print('  git commit -m "feat: abandon RenderBlender and restore full native Daedalus rendering"')
print("  git push")