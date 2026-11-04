package com.kzjy.daedalus.item;

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
