package com.kzjy.daedalus;

import com.kzjy.daedalus.client.model.DaedalusModelLoader;
import com.kzjy.daedalus.enchantment.DaedalusBaseEnchantment;
import net.minecraft.client.renderer.item.ItemProperties;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.enchantment.Enchantment;
import net.minecraft.world.item.enchantment.EnchantmentHelper;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.neoforge.client.event.ModelEvent;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;

import java.util.Map;

/**
 * @author Kzjy<br>
 * 客户端初始化<br>
 * 1. 附魔书模型覆写 (检测代达罗斯附魔)<br>
 * 2. 几何模型加载器注册 (Cosmic Model)<br>
 */
@Mod.EventBusSubscriber(modid = Daedalus.MODID, value = Dist.CLIENT, bus = Mod.EventBusSubscriber.Bus.MOD)
public class ClientSetup {

    /**
     * 注册 ItemProperties<br>
     * 遍历附魔书NBT, 若包含模组附魔则返回 1.0f 触发模型替换
     */
    @SubscribeEvent
    public static void clientSetup(final FMLClientSetupEvent event) {
        event.enqueueWork(() -> {
            ItemProperties.register(Items.ENCHANTED_BOOK,
                    new ResourceLocation(Daedalus.MODID, "enchanted_book"),
                    (stack, world, entity, seed) -> {
                        Map<Enchantment, Integer> enchantments = EnchantmentHelper.getEnchantments(stack);
                        if (enchantments.isEmpty()) return 0.0f;

                        for (Enchantment ench : enchantments.keySet()) {
                            if (ench instanceof DaedalusBaseEnchantment) {
                                return 1.0f;
                            }
                        }

                        return 0.0f;
                    });
        });
    }

    @SubscribeEvent
    public static void registerGeometryLoaders(ModelEvent.RegisterGeometryLoaders event) {
        event.register("cosmic", new DaedalusModelLoader());
    }
}
