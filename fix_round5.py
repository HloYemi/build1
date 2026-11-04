#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 5: 重写 LovePoemSwordItem.java，彻底移除 getDefaultInstance()
删除原因: HIDE_TOOLTIP 使 getTooltipLines() 返回 List.of()，
         导致 CreativeModeInventoryScreen.getTooltipFromContainerItem 中 add(1,...) 越界崩溃。
"""
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SWORD = P / "src/main/java/com/kzjy/daedalus/item/LovePoemSwordItem.java"

print("=" * 60)
print("Round 5: 重写 LovePoemSwordItem.java")
print("=" * 60)

if not SWORD.exists():
    print(f"[错误] 文件不存在: {SWORD}")
    print("如果之前跑过 fix_round4.py 删了它，从 git 恢复：")
    print("  git checkout HEAD -- src/main/java/com/kzjy/daedalus/item/LovePoemSwordItem.java")
    exit(1)

NEW_CONTENT = '''package com.kzjy.daedalus.item;

import com.kzjy.daedalus.enchantment.util.EnchantmentTheme;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.Style;
import net.minecraft.tags.BlockTags;
import net.minecraft.tags.TagKey;
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

    // getDefaultInstance() 已移除：
    // 原实现中 stack.set(DataComponents.HIDE_TOOLTIP, Unit.INSTANCE)
    // 会让 getTooltipLines() 返回不可变空列表，
    // 进而在 CreativeModeInventoryScreen.getTooltipFromContainerItem
    // 对空列表执行 add(1, ...) 时抛出 IndexOutOfBoundsException。
    // 移除后走 vanilla 默认行为，tooltip 非空，不再崩溃。

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
'''

old = SWORD.read_text(encoding="utf-8")

if old.strip() == NEW_CONTENT.strip():
    print("[跳过] 文件内容已是最新，无需修改")
else:
    SWORD.write_text(NEW_CONTENT, encoding="utf-8")
    print(f"[写入] {SWORD.relative_to(P)}")
    print(f"[信息] 原文件 {len(old)} 字符 -> 新文件 {len(NEW_CONTENT)} 字符")

c = SWORD.read_text(encoding="utf-8")
print()
print("--- 验证 ---")
print(f"HIDE_TOOLTIP 存在: {'是' if 'HIDE_TOOLTIP' in c else '否'}")
print(f"getDefaultInstance 存在: {'是' if 'getDefaultInstance' in c else '否'}")
print(f"DataComponents import 存在: {'是' if 'DataComponents' in c else '否'}")
print(f"Unit import 存在: {'是' if 'Unit.INSTANCE' in c else '否'}")

if "HIDE_TOOLTIP" not in c and "getDefaultInstance" not in c:
    print("\n[成功] 源码已清理干净")
else:
    print("\n[警告] 仍有残留，请手动检查")

print()
print("下一步:")
print("  git add .")
print('  git commit -m "fix: remove getDefaultInstance override from LovePoemSwordItem"')
print("  git push")