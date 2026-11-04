package com.kzjy.daedalus.client.compat;

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
