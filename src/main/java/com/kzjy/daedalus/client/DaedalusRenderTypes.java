package com.kzjy.daedalus.client;

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
import net.neoforged.neoforge.client.event.RegisterShadersEvent;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.common.EventBusSubscriber;

@EventBusSubscriber(value = Dist.CLIENT, modid = Daedalus.MODID, bus = Mod.EventBusSubscriber.Bus.MOD)
public class DaedalusRenderTypes extends RenderType {

    public DaedalusRenderTypes(String name, VertexFormat format, VertexFormat.Mode mode, int bufferSize, boolean affectsCrumbling, boolean sortOnUpload, Runnable setupState, Runnable clearState) {
        super(name, format, mode, bufferSize, affectsCrumbling, sortOnUpload, setupState, clearState);
    }

    public static ShaderInstance cosmicShader;
    public static ShaderInstance cosmicNeoShader;
    public static ShaderInstance glowEdgeShader;

    private static final ResourceLocation GR_GLOW_TEX = new ResourceLocation(Daedalus.MODID, "textures/misc/gr.png");
    private static final ResourceLocation MAP_GLOW_TEX = new ResourceLocation(Daedalus.MODID, "textures/misc/gr_m.png");

    @SubscribeEvent
    public static void registerShaders(RegisterShadersEvent event) {
        try {
            event.registerShader(new ShaderInstance(event.getResourceProvider(), new ResourceLocation(Daedalus.MODID, "daedalus_cosmic"), DefaultVertexFormat.NEW_ENTITY),
                    shaderInstance -> cosmicShader = shaderInstance);

            event.registerShader(new ShaderInstance(event.getResourceProvider(), new ResourceLocation(Daedalus.MODID, "cosmic_neo"), DefaultVertexFormat.NEW_ENTITY),
                    shaderInstance -> cosmicNeoShader = shaderInstance);

            event.registerShader(new ShaderInstance(event.getResourceProvider(), new ResourceLocation(Daedalus.MODID, "glow_edge"), DefaultVertexFormat.NEW_ENTITY),
                    shaderInstance -> glowEdgeShader = shaderInstance);
        } catch (Exception e) {
            Daedalus.LOGGER.error("Failed to register Daedalus shaders", e);
        }
    }

    public static final RenderType DAEDALUS_COSMIC = create("daedalus_cosmic",
            DefaultVertexFormat.NEW_ENTITY, VertexFormat.Mode.QUADS, 256, true, true,
            RenderType.CompositeState.builder()
                    .setShaderState(new RenderStateShard.ShaderStateShard(() -> cosmicShader))
                    .setTextureState(new RenderStateShard.TextureStateShard(new ResourceLocation("textures/atlas/blocks.png"), false, false))
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
                    .setTextureState(new RenderStateShard.TextureStateShard(new ResourceLocation("textures/atlas/blocks.png"), false, false))
                    .setTransparencyState(TRANSLUCENT_TRANSPARENCY)
                    .setWriteMaskState(COLOR_WRITE)
                    .setCullState(NO_CULL)
                    .setLightmapState(LIGHTMAP)
                    .setOverlayState(OVERLAY)
                    .createCompositeState(true));

    public static final RenderType GLOWING_OUTLINE = create("glowing_outline",
            DefaultVertexFormat.NEW_ENTITY, VertexFormat.Mode.QUADS, 256, true, true,
            RenderType.CompositeState.builder()
                    .setShaderState(new RenderStateShard.ShaderStateShard(() -> glowEdgeShader))
                    .setTextureState(new RenderStateShard.TextureStateShard(new ResourceLocation("textures/atlas/blocks.png"), false, false))
                    .setTransparencyState(TRANSLUCENT_TRANSPARENCY)
                    .setCullState(NO_CULL)
                    .setLightmapState(LIGHTMAP)
                    .setWriteMaskState(COLOR_WRITE)
                    .setLayeringState(VIEW_OFFSET_Z_LAYERING)
                    .createCompositeState(true));

    private static final RenderStateShard.TransparencyStateShard ADDITIVE_TRANSPARENCY = new RenderStateShard.TransparencyStateShard("additive_transparency", () -> {
        RenderSystem.enableBlend();
        RenderSystem.blendFunc(GlStateManager.SourceFactor.SRC_ALPHA, GlStateManager.DestFactor.ONE);
    }, () -> {
        RenderSystem.disableBlend();
        RenderSystem.defaultBlendFunc();
    });

    public static final RenderType GR_GLOW_DEPTH = create("gr_glow_depth",
            DefaultVertexFormat.POSITION_COLOR_TEX_LIGHTMAP, VertexFormat.Mode.TRIANGLES, 256, false, true,
            RenderType.CompositeState.builder()
                    .setShaderState(RENDERTYPE_ENTITY_TRANSLUCENT_EMISSIVE_SHADER)
                    .setTextureState(new RenderStateShard.TextureStateShard(GR_GLOW_TEX, false, false))
                    .setTransparencyState(ADDITIVE_TRANSPARENCY)
                    .setCullState(NO_CULL)
                    .setLightmapState(LIGHTMAP)
                    .setWriteMaskState(COLOR_WRITE)
                    .createCompositeState(false));

    public static final RenderType GR_GLOW_NO_DEPTH = create("gr_glow_no_depth",
            DefaultVertexFormat.POSITION_COLOR_TEX_LIGHTMAP, VertexFormat.Mode.TRIANGLES, 256, false, true,
            RenderType.CompositeState.builder()
                    .setShaderState(RENDERTYPE_ENTITY_TRANSLUCENT_EMISSIVE_SHADER)
                    .setTextureState(new RenderStateShard.TextureStateShard(GR_GLOW_TEX, false, false))
                    .setTransparencyState(ADDITIVE_TRANSPARENCY)
                    .setCullState(NO_CULL)
                    .setLightmapState(LIGHTMAP)
                    .setWriteMaskState(COLOR_WRITE)
                    .setDepthTestState(NO_DEPTH_TEST)
                    .createCompositeState(false));

    public static final RenderType GR_GLOW_DEPTH_2 = create("gr_glow_depth_2",
            DefaultVertexFormat.POSITION_COLOR_TEX_LIGHTMAP, VertexFormat.Mode.TRIANGLES, 256, false, true,
            RenderType.CompositeState.builder()
                    .setShaderState(RENDERTYPE_ENTITY_TRANSLUCENT_EMISSIVE_SHADER)
                    .setTextureState(new RenderStateShard.TextureStateShard(MAP_GLOW_TEX, false, false))
                    .setTransparencyState(ADDITIVE_TRANSPARENCY)
                    .setCullState(NO_CULL)
                    .setLightmapState(LIGHTMAP)
                    .setWriteMaskState(COLOR_WRITE)
                    .createCompositeState(false));
}
