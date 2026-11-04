#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 17: 全面拥抱前置库，清理旧版 Shader，解决黑块问题
"""
from pathlib import Path
import shutil

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SRC = P / "src/main/java/com/kzjy/daedalus"
RES = P / "src/main/resources"

print("=" * 60)
print("Round 17: 转移渲染至 RenderBlender 标准，清理旧 Shader")
print("=" * 60)

def write(rel, content):
    p = RES / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print(f"[写入] {rel}")

def remove_file(rel):
    p = SRC / rel
    if p.exists():
        p.unlink()
        print(f"[删除] {rel}")

# 1. 重写模型 JSON，使用 RenderBlender 标准 loader
# 剑：直接使用本体贴图做 mask，避免读取错误
write("assets/daedalus/models/item/love_poem_sword.json", """{
  "parent": "minecraft:item/handheld",
  "textures": { "layer0": "daedalus:item/love_poem_sword" },
  "loader": "renderblender:cosmic",
  "cosmic": { "mask": "daedalus:item/love_poem_sword" }
}
""")

# 附魔书：直接使用原版书贴图做 mask
write("assets/minecraft/models/item/enchanted_book.json", """{
  "parent": "minecraft:item/generated",
  "textures": { "layer0": "minecraft:item/enchanted_book" },
  "loader": "renderblender:cosmic",
  "cosmic": { "mask": "minecraft:item/enchanted_book" }
}
""")

# 2. 彻底删除自带 Shader 和专属渲染类（因为 1.21.1 接口变动导致它们变黑）
remove_file("client/DaedalusRenderTypes.java")
remove_file("client/model/DaedalusModelLoader.java")
remove_file("client/model/DaedalusCosmicBakedModel.java")

shader_dir = RES / "assets/daedalus/shaders/core"
if shader_dir.exists():
    shutil.rmtree(shader_dir)
    print("[删除] assets/daedalus/shaders/core/ 整个目录")

# 3. 清理 ClientSetup，去掉旧 Loader 注册
setup = SRC / "ClientSetup.java"
if setup.exists():
    setup.write_text('''package com.kzjy.daedalus;

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
''', encoding="utf-8")
    print("[重写] ClientSetup.java (移除了自定义模型加载器注册)")

print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: migrate entirely to renderblender loaders and strip broken custom shaders"')
print("  git push")