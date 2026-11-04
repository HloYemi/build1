package com.kzjy.daedalus.client.renderer;

import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;

/**
 * @author Kzjy<br>
 * 渲染辅助类
 */
public class DaedalusRenderHelper {
    public static boolean isBlocking(Player player) {
        if (player.isUsingItem()) {
            ItemStack usedItem = player.getUseItem();
            return DaedalusWeaponConfig.isSpecialWeapon(usedItem);
        }
        return false;
    }
}
