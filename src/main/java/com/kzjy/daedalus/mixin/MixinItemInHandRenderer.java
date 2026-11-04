package com.kzjy.daedalus.mixin;

import com.kzjy.daedalus.client.renderer.DaedalusRenderHelper;
import com.kzjy.daedalus.client.renderer.DaedalusWeaponConfig;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.AbstractClientPlayer;
import net.minecraft.client.renderer.ItemInHandRenderer;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.ItemDisplayContext;
import net.minecraft.world.item.ItemStack;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * @author Kzjy<br>
 * 手持物品渲染混入<br>
 * 实现特殊武器的瞬时格挡动画<br>
 */
@Mixin(ItemInHandRenderer.class)
public class MixinItemInHandRenderer {

    @Inject(method = "renderArmWithItem", at = @At("HEAD"), cancellable = true)
    private void renderArmWithItem(AbstractClientPlayer player, float partialTicks, float pitch,
                                   InteractionHand hand, float swingProgress, ItemStack stack,
                                   float equipProgress, PoseStack poseStack,
                                   MultiBufferSource buffer, int combinedLight, CallbackInfo ci) {

        if (DaedalusWeaponConfig.isSpecialWeapon(stack) && DaedalusRenderHelper.isBlocking(player)) {
            if (hand == player.getUsedItemHand()) {
                ci.cancel();
                renderInstantBlocking(player, partialTicks, pitch, hand, swingProgress,
                        stack, poseStack, buffer, combinedLight);
            }
        }
    }

    @Unique
    private void renderInstantBlocking(AbstractClientPlayer player, float partialTicks, float pitch,
                                       InteractionHand hand, float swingProgress, ItemStack stack,
                                       PoseStack poseStack, MultiBufferSource buffer, int combinedLight) {
        poseStack.pushPose();
        float instantEquipProgress = 1.0F;

        boolean isMainHand = (hand == InteractionHand.MAIN_HAND);
        int sideMultiplier = isMainHand ? 1 : -1;

        poseStack.translate(sideMultiplier * 0.56F, -0.52F + instantEquipProgress * -0.6F, -0.72F);

        poseStack.mulPose(Axis.XP.rotation(4.5F + 0.1F));
        poseStack.mulPose(Axis.YP.rotation(0.3F - 0.04F));
        poseStack.mulPose(Axis.ZP.rotation(-4.7F - 0.22F));
        poseStack.translate(0.14F - 0.4, -0.11F + 0.34, 0.6F);

        try {
            Minecraft.getInstance().getItemRenderer().renderStatic(stack, ItemDisplayContext.FIRST_PERSON_RIGHT_HAND,
                    combinedLight, OverlayTexture.NO_OVERLAY, poseStack,
                    buffer, player.level(), 0);
        } catch (Exception ignored) {
        }

        poseStack.popPose();
    }
}
