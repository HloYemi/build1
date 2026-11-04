package com.kzjy.daedalus.client.compat;

import com.kzjy.daedalus.Daedalus;
import com.mojang.blaze3d.vertex.PoseStack;
import committee.nova.mods.renderblender.api.client.model.PerspectiveModel;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.client.extensions.common.IClientItemExtensions;
import org.jetbrains.annotations.NotNull;

public final class RBPerspectiveItemExtensions implements IClientItemExtensions {
    @Override
    public @NotNull ICustomItemRenderer getCustomRenderer(@NotNull ItemStack stack) {
        return CustomRenderer.INSTANCE;
    }

    private static final class CustomRenderer implements ICustomItemRenderer {
        static final CustomRenderer INSTANCE = new CustomRenderer();

        @Override
        public void render(@NotNull ItemStack stack, @NotNull ItemDisplayContext ctx,
                           @NotNull PoseStack pStack, @NotNull MultiBufferSource source,
                           int light, int overlay) {
            Minecraft mc = Minecraft.getInstance();
            BakedModel model = mc.getItemRenderer().getModel(stack, mc.level, mc.player, 0);

            if (model instanceof PerspectiveModel pm) {
                try {
                    // 1.21.1 的 ICustomItemRenderer 调用时，PoseStack 已经处于物品视角的原点，
                    // 不包含原版的 ItemTransform（因为原版不知道我们要怎么渲染）。
                    // 所以我们需要手动应用 PerspectiveModelState 的变换。
                    PerspectiveModel transformed = (PerspectiveModel) pm.applyTransform(ctx, pStack, false);
                    pStack.translate(-0.5D, -0.5D, -0.5D);
                    transformed.renderItem(stack, ctx, pStack, source, light, overlay);
                } catch (Throwable t) {
                    Daedalus.LOGGER.error("[Daedalus] RB renderItem failed", t);
                }
            } else {
                // 如果没有找到 PerspectiveModel，退化为原版渲染
                mc.getItemRenderer().renderStatic(
                        stack, ctx, light, overlay, pStack, source,
                        mc.level, 0
                );
            }
        }
    }
}
