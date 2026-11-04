package com.kzjy.daedalus.item;

import com.kzjy.daedalus.enchantment.util.EnchantmentTheme;
import committee.nova.mods.renderblender.api.iface.IToolTransform;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.Style;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResultHolder;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.item.SwordItem;
import net.minecraft.world.item.Tier;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.UseAnim;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.level.Level;
import org.jetbrains.annotations.Nullable;

import java.util.List;

public class LovePoemSwordItem extends SwordItem implements IToolTransform {

    public LovePoemSwordItem() {
        super(new Tier() {
                  @Override public int getUses() { return 0; }
                  @Override public float getSpeed() { return 10.0F; }
                  @Override public float getAttackDamageBonus() { return 0.0F; }
                  @Override public int getLevel() { return 5; }
                  @Override public int getEnchantmentValue() { return 25; }
                  @Override public Ingredient getRepairIngredient() { return Ingredient.EMPTY; }
              }, 1314 - 1, -2.4F + 2.3F,
                new Properties().rarity(Rarity.EPIC).fireResistant());
    }

    @Override
    public UseAnim getUseAnimation(ItemStack stack) {
        return UseAnim.BLOCK;
    }

    @Override
    public int getUseDuration(ItemStack stack) {
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
        stack.getOrCreateTag().putInt("HideFlags", 2);
        return stack;
    }

    @Override
    public void inventoryTick(ItemStack stack, Level level, Entity entity, int slotId, boolean isSelected) {
        super.inventoryTick(stack, level, entity, slotId, isSelected);
        if (!stack.getOrCreateTag().contains("HideFlags") || stack.getOrCreateTag().getInt("HideFlags") != 2) {
            stack.getOrCreateTag().putInt("HideFlags", 2);
        }
    }

    @Override
    public Component getName(ItemStack stack) {
        if (!stack.getOrCreateTag().contains("HideFlags")) {
            stack.getOrCreateTag().putInt("HideFlags", 2);
        }
        return Component.translatable(this.getDescriptionId(stack))
                .withStyle(Style.EMPTY.withColor(EnchantmentTheme.LOVE_BLUE.getPrimaryColor()));
    }

    @Override
    public void appendHoverText(ItemStack stack, @Nullable Level level, List<Component> tooltip, TooltipFlag flag) {
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
