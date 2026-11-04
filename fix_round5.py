#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 26: 通过 IClientItemExtensions 接管渲染，修复 RB 的 Mixin 失效问题
"""
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SRC = P / "src/main/java/com/kzjy/daedalus"

print("=" * 60)
print("Round 26: 修复前置库 Mixin 失效，接管物品渲染")
print("=" * 60)

def write(rel, content):
    p = SRC / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[写入] {rel}")

# 1. 创建 RBPerspectiveItemExtensions (核心转发逻辑)
write("client/compat/RBPerspectiveItemExtensions.java", '''package com.kzjy.daedalus.client.compat;

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
''')

# 2. 创建 DaedalusClientSetup 注册事件
write("client/DaedalusClientSetup.java", '''package com.kzjy.daedalus.client;

import com.kzjy.daedalus.Daedalus;
import com.kzjy.daedalus.client.compat.RBPerspectiveItemExtensions;
import com.kzjy.daedalus.registry.DaedalusRegistries;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RegisterClientExtensionsEvent;

@EventBusSubscriber(modid = Daedalus.MODID, value = Dist.CLIENT, bus = EventBusSubscriber.Bus.MOD)
public final class DaedalusClientSetup {
    @SubscribeEvent
    public static void registerClientExtensions(RegisterClientExtensionsEvent event) {
        event.registerItem(new RBPerspectiveItemExtensions(), DaedalusRegistries.LOVE_POEM_SWORD.get());
    }
}
''')

print("\n下一步:")
print("  git add .")
print('  git commit -m "feat: use IClientItemExtensions to fix RB ItemRendererMixin failure on 1.21.1"')
print("  git push")