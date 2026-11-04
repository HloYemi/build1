package com.kzjy.daedalus.client.renderer;

import com.kzjy.daedalus.item.LovePoemSwordItem;
import net.minecraft.world.item.ItemStack;

import java.util.HashSet;
import java.util.Set;

/**
 * @author Kzjy<br>
 * 武器渲染配置<br>
 * 判定特殊格挡动画应用对象<br>
 */
public class DaedalusWeaponConfig {
    private static final Set<Class<?>> SPECIAL_WEAPONS = new HashSet<>();

    static {
        registerWeapon(LovePoemSwordItem.class);
    }

    public static void registerWeapon(Class<?> weaponClass) {
        SPECIAL_WEAPONS.add(weaponClass);
    }

    public static boolean isSpecialWeapon(ItemStack stack) {
        if (stack.isEmpty()) return false;
        return SPECIAL_WEAPONS.stream()
                .anyMatch(weaponClass -> weaponClass.isInstance(stack.getItem()));
    }
}
