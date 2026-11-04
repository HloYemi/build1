package com.kzjy.daedalus;

import com.kzjy.daedalus.config.DaedalusConfig;
import com.kzjy.daedalus.registry.DaedalusRegistries;
import com.mojang.logging.LogUtils;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import org.slf4j.Logger;

@Mod(Daedalus.MODID)
public class Daedalus {
    public static final String MODID = "daedalus";
    public static final Logger LOGGER = LogUtils.getLogger();

    public Daedalus(IEventBus modEventBus, ModContainer modContainer) {
        DaedalusRegistries.ITEMS.register(modEventBus);
        DaedalusRegistries.MOB_EFFECTS.register(modEventBus);
        DaedalusRegistries.CREATIVE_MODE_TABS.register(modEventBus);
        modContainer.registerConfig(ModConfig.Type.COMMON, DaedalusConfig.COMMON_SPEC);
    }
}
