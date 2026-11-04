package com.kzjy.daedalus.client;

import com.kzjy.daedalus.Daedalus;
import com.kzjy.daedalus.client.compat.RBPerspectiveItemExtensions;
import com.kzjy.daedalus.registry.DaedalusRegistries;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.extensions.common.RegisterClientExtensionsEvent;

@EventBusSubscriber(modid = Daedalus.MODID, value = Dist.CLIENT, bus = EventBusSubscriber.Bus.MOD)
public final class DaedalusClientSetup {
    @SubscribeEvent
    public static void registerClientExtensions(RegisterClientExtensionsEvent event) {
        event.registerItem(new RBPerspectiveItemExtensions(), DaedalusRegistries.LOVE_POEM_SWORD.get());
    }
}
