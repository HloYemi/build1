package com.kzjy.daedalus;

import net.minecraft.client.renderer.item.ItemProperties;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.Items;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;

@EventBusSubscriber(modid = Daedalus.MODID, value = Dist.CLIENT, bus = EventBusSubscriber.Bus.MOD)
public class ClientSetup {
    @SubscribeEvent
    public static void clientSetup(FMLClientSetupEvent event) {
        event.enqueueWork(() -> {
            ItemProperties.register(Items.ENCHANTED_BOOK,
                    ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "enchanted_book"),
                    (stack, world, entity, seed) -> {
                        var enchants = stack.getEnchantments();
                        for (var e : enchants.entrySet()) {
                            var keyOpt = e.getKey().unwrapKey();
                            if (keyOpt.isPresent() && keyOpt.get().location().getNamespace().equals(Daedalus.MODID)) {
                                return 1.0f;
                            }
                        }
                        return 0.0f;
                    });
        });
    }
}
