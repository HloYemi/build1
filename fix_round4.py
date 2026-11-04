#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daedalus NeoForge 1.21.1 - Round 4
修复剩余 8 个错误
"""
import re
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SRC = P / "src" / "main" / "java" / "com" / "kzjy" / "daedalus"

def write_file(rel: str, content: str):
    path = SRC / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[写入] {rel}")

def replace_in(rel: str, old: str, new: str, desc: str = ""):
    path = SRC / rel
    if not path.exists():
        print(f"[跳过] {rel} 不存在")
        return
    c = path.read_text(encoding="utf-8")
    if old not in c:
        print(f"[跳过] {rel}: 未找到 '{old[:60]}'")
        return
    c = c.replace(old, new)
    path.write_text(c, encoding="utf-8")
    print(f"[修改] {rel} {desc}")

# =====================================================================
# 1. DaedalusClientEvents.java: Mod.EventBusSubscriber.Bus.MOD → EventBusSubscriber.Bus.MOD
# =====================================================================
replace_in("client/DaedalusClientEvents.java",
           "Mod.EventBusSubscriber.Bus.MOD",
           "EventBusSubscriber.Bus.MOD",
           "Bus.MOD")

# =====================================================================
# 2. DaedalusRenderTypes.java: 同样问题
# =====================================================================
replace_in("client/DaedalusRenderTypes.java",
           "Mod.EventBusSubscriber.Bus.MOD",
           "EventBusSubscriber.Bus.MOD",
           "Bus.MOD")

# =====================================================================
# 3. DaedalusEvents.java: TriState.FALSE → Event.Result.DENY
# =====================================================================
ev = SRC / "event" / "DaedalusEvents.java"
c = ev.read_text(encoding="utf-8")
# 移除 TriState import
c = c.replace("import net.neoforged.neoforge.common.util.TriState;\n", "")
# 替换 setResult
c = c.replace("event.setResult(TriState.FALSE);",
              "event.setResult(net.neoforged.bus.api.Event.Result.DENY);")
ev.write_text(c, encoding="utf-8")
print("[修改] DaedalusEvents.java (TriState → Event.Result.DENY)")

# =====================================================================
# 4. DaedalusGlowRenderer.java: 重写 addVertexWithColor，适配 1.21 VertexConsumer
# =====================================================================
gr = SRC / "client" / "renderer" / "DaedalusGlowRenderer.java"
c = gr.read_text(encoding="utf-8")

# 加 import
if "import net.minecraft.client.renderer.LightTexture;" not in c:
    c = c.replace(
        "import net.minecraft.client.renderer.MultiBufferSource;",
        "import net.minecraft.client.renderer.MultiBufferSource;\nimport net.minecraft.client.renderer.LightTexture;\nimport net.minecraft.client.renderer.texture.OverlayTexture;"
    )

# 替换 addVertexWithColor 方法体
old_method = re.search(
    r'    private static void addVertexWithColor\(.*?\n    \}',
    c, re.DOTALL
)
if old_method:
    new_method = '''    private static void addVertexWithColor(VertexConsumer vertexConsumer, Matrix4f matrix, Matrix3f normal, float x, float y, float z, float u, float v, int r, int g, int b, int alpha) {
        vertexConsumer.addVertex(matrix, x, y, z)
                .setColor(r, g, b, alpha)
                .setUv(u, v)
                .setOverlay(OverlayTexture.NO_OVERLAY)
                .setLight(LightTexture.FULL_BRIGHT)
                .setNormal(normal, 0.0F, 1.0F, 0.0F);
    }'''
    c = c[:old_method.start()] + new_method + c[old_method.end():]
    print("[修改] DaedalusGlowRenderer.addVertexWithColor")
gr.write_text(c, encoding="utf-8")

# =====================================================================
# 5. LovePoemSwordItem.java: 完全重写，适配 1.21 签名
# =====================================================================
write_file("item/LovePoemSwordItem.java", '''package com.kzjy.daedalus.item;

import com.kzjy.daedalus.enchantment.util.EnchantmentTheme;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.core.component.DataComponents;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.Style;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.TagKey;
import net.minecraft.util.Unit;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.Tiers;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.UseAnim;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import org.jetbrains.annotations.Nullable;

import java.util.List;

public class LovePoemSwordItem extends SwordItem {

    public LovePoemSwordItem() {
        super(new Tier() {
                  @Override public int getUses() { return 0; }
                  @Override public float getSpeed() { return 10.0F; }
                  @Override public float getAttackDamageBonus() { return 0.0F; }
                  @Override public TagKey<Block> getIncorrectBlocksForDrops() {
                      return BlockTags.INCORRECT_FOR_NETHERITE_TOOL;
                  }
                  @Override public int getEnchantmentValue() { return 25; }
                  @Override public Ingredient getRepairIngredient() { return Ingredient.EMPTY; }
              },
              new Properties().rarity(Rarity.EPIC).fireResistant()
                  .attributes(SwordItem.createAttributes(Tiers.NETHERITE, 1314 - 1, -2.4F + 2.3F)));
    }

    @Override
    public UseAnim getUseAnimation(ItemStack stack) {
        return UseAnim.BLOCK;
    }

    @Override
    public int getUseDuration(ItemStack stack, LivingEntity entity) {
        return 72000;
    }

    @Override
    public InteractionResultHolder<ItemStack> use(Level level, Player player, InteractionHand hand) {
        ItemStack stack = player.getItemInHand(hand);
        player.startUsingItem(hand);
        return InteractionResultHolder.consume(stack);
    }

    @Override
    public ItemStack getDefaultInstance() {
        ItemStack stack = new ItemStack(this);
        stack.set(DataComponents.HIDE_TOOLTIP, Unit.INSTANCE);
        return stack;
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slotId, boolean isSelected) {
        super.inventoryTick(stack, level, entity, slotId, isSelected);
    }

    @Override
    public Component getName(ItemStack stack) {
        return Component.translatable(this.getDescriptionId(stack))
                .withStyle(Style.EMPTY.withColor(EnchantmentTheme.LOVE_BLUE.getPrimaryColor()));
    }

    @Override
    public void appendHoverText(ItemStack stack, Item.TooltipContext context, List<Component> tooltip, TooltipFlag flag) {
        if (Screen.hasAltDown()) {
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc0.line1"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc0.line2"));
        } else {
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc1.line1"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc1.line2"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc1.line3"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc1.line4"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc1.line5"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc1.line6"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.desc1.line7"));
            tooltip.add(Component.translatable("item.daedalus.love_poem_sword.hold_alt"));
        }
    }
}
''')

print("\n" + "=" * 60)
print("Round 4 修复完成")
print("=" * 60)
print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: NeoForge 1.21.1 API round 4"')
print("  git push")