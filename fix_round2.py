





















































                                      boolean isNeo, int neoType) {
                                      int glowColor, float glowWidth, float glowOffset,
                                   IGeometryBakingContext context) {
                                return 1.0f;
                               Function<Material, TextureAtlasSprite> spriteGetter,
                               ModelState modelState, ItemOverrides overrides) {
                            if (keyOpt.isPresent() && keyOpt.get().location().getNamespace().equals(Daedalus.MODID)) {
                            var keyOpt = e.getKey().unwrapKey();
                            }
                        for (var e : enchants.entrySet()) {
                        return 0.0f;
                        var enchants = stack.getEnchantments();
                        }
                      return net.minecraft.tags.BlockTags.INCORRECT_FOR_NETHERITE_TOOL;
                    (stack, world, entity, seed) -> {
                    baker, this.baseModel, spriteGetter, modelState, true);
                    Collections.singletonList(maskLocation),
                    glowColor, glowWidth, glowOffset, isNeo, neoType);
                    ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "enchanted_book"),
                    });
                  'ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "cosmic_neo")')
                  'ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "daedalus_cosmic")')
                  'ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "glow_edge")')
                  'ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "textures/misc/gr.png")')
                  'ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "textures/misc/gr.png")')
                  'ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "textures/misc/gr_m.png")')
                  'ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "textures/misc/gr_m.png")')
                  'ResourceLocation.parse("textures/atlas/blocks.png")')
                  'vertexConsumer.addVertex(matrix, x, y, z)')
                  .attributes(SwordItem.createAttributes(Tiers.NETHERITE, 1314 - 1, -2.4F + 2.3F)));'''
                  @Override public float getAttackDamageBonus() { return 0.0F; }
                  @Override public float getAttackDamageBonus() { return 0.0F; }
                  @Override public float getSpeed() { return 10.0F; }
                  @Override public float getSpeed() { return 10.0F; }
                  @Override public Ingredient getRepairIngredient() { return Ingredient.EMPTY; }
                  @Override public Ingredient getRepairIngredient() { return Ingredient.EMPTY; }
                  @Override public int getEnchantmentValue() { return 25; }
                  @Override public int getEnchantmentValue() { return 25; }
                  @Override public int getLevel() { return 5; }
                  @Override public int getUses() { return 0; }
                  @Override public int getUses() { return 0; }
                  @Override public net.minecraft.tags.TagKey<net.minecraft.world.level.block.Block> getIncorrectBlocksForDrops() {
                  }
                "import net.neoforged.bus.api.SubscribeEvent;",
                "import net.neoforged.bus.api.SubscribeEvent;\nimport net.neoforged.fml.common.EventBusSubscriber;"
                -0.05, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL);
                -0.1, AttributeModifier.Operation.ADD_MULTIPLIED_TOTAL);
                glowColor, glowWidth, glowOffset, isNeo, neoType);
                isNeo = true;
                neoType = GsonHelper.getAsInt(cosmicObj, "type", 0);
                new Properties().rarity(Rarity.EPIC).fireResistant());'''
                ResourceLocation.fromNamespaceAndPath("daedalus", "abyssal_curse_armor"),
                ResourceLocation.fromNamespaceAndPath("daedalus", "abyssal_curse_toughness"),
                ResourceLocation.parse(maskPath),
              "// Pre event: no cancel")
              "event.setResult(net.neoforged.neoforge.common.util.TriState.FALSE)")
              "if (!breach && RANDOM.nextFloat() < lvl * 0.05) { event.setNewDamage(0); return; }")
              }, 1314 - 1, -2.4F + 2.3F,
              }, new Properties().rarity(Rarity.EPIC).fireResistant()
            "import net.minecraft.world.item.ItemStack;",
            "import net.minecraft.world.item.ItemStack;\nimport net.minecraft.core.component.DataComponents;\nimport net.minecraft.world.item.component.CustomData;"
            "import net.neoforged.fml.common.Mod;",
            "import net.neoforged.fml.common.Mod;\nimport net.neoforged.fml.common.EventBusSubscriber;"
            )
            BakedModel bakedBaseModel = this.baseModel.bake(
            c = c.replace(
            c = c[:-1] + helper + "}\n"
            cosmicObj = jsonObject.getAsJsonObject("cosmic_neo");
            glowColor = GsonHelper.getAsInt(glowObj, "color", 16777215);
            glowOffset = GsonHelper.getAsFloat(glowObj, "offset", 0.02f);
            glowWidth = GsonHelper.getAsFloat(glowObj, "width", 1.0f);
            if (cosmicObj != null) {
            ItemProperties.register(Items.ENCHANTED_BOOK,
            JsonObject glowObj = jsonObject.getAsJsonObject("glow_edge");
            new DaedalusModelLoader()
            ResourceLocation.fromNamespaceAndPath(Daedalus.MODID, "cosmic"),
            return new DaedalusCosmicBakedModel(bakedBaseModel,
            this.baseModel = baseModel;
            this.baseModel.resolveParents(modelGetter);
            this.glowColor = glowColor;
            this.glowOffset = glowOffset;
            this.glowWidth = glowWidth;
            this.isNeo = isNeo;
            this.maskLocation = maskLocation;
            this.neoType = neoType;
            }
        # 没有 Mod import 的文件（比如 DaedalusRenderTypes）用另一条路径加
        )
        )
        );
        // 每级 -10% 护甲
        // 每级 -5% 韧性
        @Override
        @Override
        BlockModel baseModel = context.deserialize(clean, BlockModel.class);
        boolean isNeo = false;
        c = c.replace(
        c = c.replace(
        c = c.rstrip()
        clean.remove("cosmic_neo");
        clean.remove("daedalus_cosmic");
        clean.remove("glow_edge");
        clean.remove("loader");
        continue
        continue
        entity.hurt(entity.damageSources().magic(), damageAmount);
        event.enqueueWork(() -> {
        event.register(
        float basePercent = 0.05f;
        float damageAmount = maxHealth * (basePercent + (amplifier * 0.01f));
        float glowOffset = 0.0f;
        float glowWidth = 0.0f;
        float maxHealth = entity.getMaxHealth();
        helper = """
        if "import net.neoforged.bus.api.SubscribeEvent;" in c:
        if (cosmicObj == null) throw new IllegalStateException("Missing 'daedalus_cosmic' or 'cosmic_neo' object.");
        if (cosmicObj == null) {
        if (entity.level().isClientSide) return false;
        if (jsonObject.has("glow_edge")) {
        if c.endswith("}"):
        int glowColor = 0xFFFFFF;
        int neoType = 0;
        JsonObject clean = jsonObject.deepCopy();
        JsonObject cosmicObj = jsonObject.getAsJsonObject("daedalus_cosmic");
        print(f"  [跳过] {path.name} 不存在")
        print(f"  [跳过] {path.name}: 未找到 '{old[:60]}'")
        private final BlockModel baseModel;
        private final boolean isNeo;
        private final float glowOffset;
        private final float glowWidth;
        private final int glowColor;
        private final int neoType;
        private final ResourceLocation maskLocation;
        public BakedModel bake(IGeometryBakingContext context, ModelBaker baker,
        public DaedalusCosmicGeometry(BlockModel baseModel, ResourceLocation maskLocation,
        public void resolveParents(Function<ResourceLocation, UnbakedModel> modelGetter,
        return
        return
        return duration % 20 == 0;
        return new DaedalusCosmicGeometry(baseModel,
        return stack.getOrDefault(DataComponents.CUSTOM_DATA, CustomData.EMPTY).copyTag();
        return this.daedalus$onlyAmountUp;
        return this.daedalus$uncancelable;
        return true;
        stack.set(DataComponents.CUSTOM_DATA, CustomData.of(tag));
        String maskPath = cosmicObj.get("mask").getAsString();
        super(entity);
        super(MobEffectCategory.HARMFUL, 0x100010);
        super(MobEffectCategory.HARMFUL, 0x8B0000);
        this.addAttributeModifier(Attributes.ARMOR,
        this.addAttributeModifier(Attributes.ARMOR_TOUGHNESS,
        this.daedalus$onlyAmountUp = onlyUp;
        this.daedalus$uncancelable = uncancelable;
        }
        }
        }
        }
        }
        });
    "import net.neoforged.neoforge.event.entity.living.*;",
    "import net.neoforged.neoforge.event.entity.living.*;\nimport net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;\nimport net.neoforged.neoforge.event.tick.EntityTickEvent;"
    # getOrCreateTag 已在第 3 步处理
    # 在类末尾（最后一个 } 之前）插入辅助方法
    # 替换 Tier 匿名类
    # 添加 import
    # 简单替换：stack.getOrCreateTag() → getCustomData(stack)
    @Override
    @Override
    @Override
    @Override
    @Override
    @Override
    @Override
    @SubscribeEvent
    @SubscribeEvent
    @Unique private boolean daedalus$onlyAmountUp = false;
    @Unique private boolean daedalus$uncancelable = false;
    c = c.replace("@Mod.EventBusSubscriber", "@EventBusSubscriber")
    c = c.replace("daedalus$isAmountOnlyUp", "daedalus$isOnlyAmountUp")
    c = c.replace("key.getSerializer()", "key.serializer()")
    c = c.replace("s.getOrCreateTag()", "getCustomData(s)")
    c = c.replace("stack.getOrCreateTag()", "getCustomData(stack)")
    c = c.replace("w.getOrCreateTag()", "getCustomData(w)")
    c = c.replace('new ResourceLocation("textures/atlas/blocks.png")',
    c = c.replace('new ResourceLocation(Daedalus.MODID, "cosmic_neo")',
    c = c.replace('new ResourceLocation(Daedalus.MODID, "daedalus_cosmic")',
    c = c.replace('new ResourceLocation(Daedalus.MODID, "glow_edge")',
    c = c.replace('new ResourceLocation(Daedalus.MODID, "textures/misc/gr.png")',
    c = c.replace('new ResourceLocation(Daedalus.MODID, "textures/misc/gr.png")',
    c = c.replace('new ResourceLocation(Daedalus.MODID, "textures/misc/gr_m.png")',
    c = c.replace('new ResourceLocation(Daedalus.MODID, "textures/misc/gr_m.png")',
    c = c.replace('vertexConsumer.vertex(matrix, x, y, z)',
    c = c.replace(old, new)
    c = c.replace(old_tier, new_tier)
    c = gr.read_text(encoding="utf-8")
    c = jf.read_text(encoding="utf-8")
    c = jf.read_text(encoding="utf-8")
    c = lps.read_text(encoding="utf-8")
    c = mld.read_text(encoding="utf-8")
    c = msd.read_text(encoding="utf-8")
    c = path.read_text(encoding="utf-8")
    c = rt.read_text(encoding="utf-8")
    gr.write_text(c, encoding="utf-8")
    if "@Mod.EventBusSubscriber" not in c:
    if "getOrCreateTag()" not in c:
    if "import net.minecraft.core.component.DataComponents;" not in c:
    if "import net.neoforged.fml.common.EventBusSubscriber;" not in c:
    if "import net.neoforged.fml.common.Mod;" not in c:
    if "private static CompoundTag getCustomData(ItemStack stack)" not in c:
    if not path.exists():
    if old not in c:
    jf.write_text(c, encoding="utf-8")
    jf.write_text(c, encoding="utf-8")
    lps.write_text(c, encoding="utf-8")
    mj.write_text(s, encoding="utf-8")
    mld.write_text(c, encoding="utf-8")
    msd.write_text(c, encoding="utf-8")
    new_tier = '''super(new Tier() {
    old_tier = '''super(new Tier() {
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(c, encoding="utf-8")
    path.write_text(content, encoding="utf-8")
    print("  [修改] DaedalusGlowRenderer.java")
    print("  [修改] DaedalusRenderTypes.java")
    print("  [修改] LovePoemSwordItem.java")
    print("  [修改] MixinLivingDamageEvent.java")
    print("  [修改] MixinSynchedEntityData.java")
    print("\n[15] mixins.json 已清理")
    print(f"  [修改] {jf.name}")
    print(f"  [修改] {jf.name}")
    print(f"  [修改] {path.name} {desc}")
    print(f"  [重写] {path.relative_to(P)}")
    private static CompoundTag getCustomData(ItemStack stack) {
    private static void setCustomData(ItemStack stack, CompoundTag tag) {
    public AbyssalCurseEffect() {
    public boolean applyEffectTick(LivingEntity entity, int amplifier) {
    public boolean daedalus$isOnlyAmountUp() {
    public boolean daedalus$isUncancelable() {
    public boolean shouldApplyEffectTickThisTick(int duration, int amplifier) {
    public DaedalusCosmicGeometry read(JsonObject jsonObject, JsonDeserializationContext context) throws JsonParseException {
    public MarkOfSinEffect() {
    public MixinLivingEvent(Entity entity) {
    public static class DaedalusCosmicGeometry implements IUnbakedGeometry<DaedalusCosmicGeometry> {
    public static void clientSetup(FMLClientSetupEvent event) {
    public static void registerGeometryLoaders(ModelEvent.RegisterGeometryLoaders event) {
    public void daedalus$setOnlyAmountUp(boolean onlyUp) {
    public void daedalus$setUncancelable(boolean uncancelable) {
    rt.write_text(c, encoding="utf-8")
    s = mj.read_text(encoding="utf-8")
    s = re.sub(r'\s*"MixinLivingHurtEvent",?', '', s)
    }
    }
    }
    }
    }
    }
    }
    }
    }
    }
    }
    }
    }
    }
    }
 * @author Kzjy<br>
 * @author Kzjy<br>
 * 削减目标的护甲与韧性，并降低其输出伤害
 * 周期性对目标造成基于最大生命值百分比的伤害
 * 深渊诅咒效果<br>
 * 罪孽印记效果<br>
 */
 */
"""
"""
"""
""")
""")
""")
""")
""")
# -*- coding: utf-8 -*-
# 1. @Mod.EventBusSubscriber → @EventBusSubscriber
# 10. LovePoemSwordItem：Tier 接口 + SwordItem 构造器
# 11. MixinSynchedEntityData：getSerializer → serializer
# 12. MixinLivingDamageEvent：daedalus$isAmountOnlyUp → daedalus$isOnlyAmountUp
# 13. MixinLivingEvent：setCanceled / isCanceled 不再可 override
# 14. MixinDamageSource：TagKey 注入保持，但确认 import
# 15. 从 mixins.json 移除 MixinLivingHurtEvent（round1 已删，这里确认）
# 2. DaedalusEvents：LivingAttackEvent / LivingTickEvent / Pre 事件
# 3. ItemStack getOrCreateTag → CustomData
# 4. AbyssalCurseEffect：AttributeModifier 构造器
# 5. MarkOfSinEffect：applyEffectTick 返回 boolean
# 6. ClientSetup：registerGeometryLoaders 签名
# 7. DaedalusRenderTypes：ResourceLocation 构造器
# 8. DaedalusGlowRenderer：ResourceLocation + VertexConsumer
# 9. DaedalusModelLoader：IUnbakedGeometry + ResourceLocation
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# =====================================================================
# Event.Result → TriState（NeoForge 1.21.1 用 TriState）
# import 修正
# LivingAttackEvent 改用 LivingIncomingDamageEvent
# LivingTickEvent → EntityTickEvent
# Pre 事件的 setCanceled / isCanceled 不再存在，改为 setNewDamage(0) 或直接跳过
# 对 onLivingDamageEnforce 和 onLivingAttackEnforce 的取消逻辑做简化
# 旧的 PlayerTickEvent 导入已经在 round1 换成 PlayerTickEvent，无需再改
# 这个类在 1.21.1 下通常仍可用，跳过
#!/usr/bin/env python3
)
/**
/**
@EventBusSubscriber(modid = Daedalus.MODID, value = Dist.CLIENT, bus = EventBusSubscriber.Bus.MOD)
@Mixin(LivingEvent.class)
c = c.replace(
c = c.replace("event.setResult(net.neoforged.bus.api.Event.Result.DENY)",
c = c.replace("if (!breach && RANDOM.nextFloat() < lvl * 0.05) { event.setCanceled(true); return; }",
c = c.replace("if (event.isCanceled()) event.setCanceled(false);",
c = c.replace("LivingAttackEvent", "LivingIncomingDamageEvent")
c = c.replace("LivingEvent.LivingTickEvent", "EntityTickEvent.Post")
c = ev.read_text(encoding="utf-8")
Daedalus 移植 Round 2：NeoForge 1.21.1 API 适配
def replace_file(path: Path, old: str, new: str, desc: str = ""):
def write_file(path: Path, content: str):
ev = SRC / "event" / "DaedalusEvents.java"
ev.write_text(c, encoding="utf-8")
for jf in SRC.rglob("*.java"):
for jf in SRC.rglob("*.java"):
from pathlib import Path
gr = SRC / "client" / "renderer" / "DaedalusGlowRenderer.java"
if gr.exists():
if lps.exists():
if mj.exists():
if mld.exists():
if msd.exists():
if rt.exists():
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import com.kzjy.daedalus.client.model.DaedalusModelLoader;
import com.kzjy.daedalus.duck.IDaedalusLivingEvent;
import java.util.Collections;
import java.util.function.Function;
import net.minecraft.client.renderer.block.model.BlockModel;
import net.minecraft.client.renderer.block.model.ItemOverrides;
import net.minecraft.client.renderer.item.ItemProperties;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.client.resources.model.Material;
import net.minecraft.client.resources.model.ModelBaker;
import net.minecraft.client.resources.model.ModelState;
import net.minecraft.client.resources.model.UnbakedModel;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.GsonHelper;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.item.Items;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.fml.event.lifecycle.FMLClientSetupEvent;
import net.neoforged.neoforge.client.event.ModelEvent;
import net.neoforged.neoforge.client.model.geometry.IGeometryBakingContext;
import net.neoforged.neoforge.client.model.geometry.IGeometryLoader;
import net.neoforged.neoforge.client.model.geometry.IUnbakedGeometry;
import net.neoforged.neoforge.event.entity.EntityEvent;
import net.neoforged.neoforge.event.entity.living.LivingEvent;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import re
lps = SRC / "item" / "LovePoemSwordItem.java"
mj = RES / "daedalus.mixins.json"
mld = SRC / "mixin" / "MixinLivingDamageEvent.java"
msd = SRC / "mixin" / "MixinSynchedEntityData.java"
P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
package com.kzjy.daedalus.client.model;
package com.kzjy.daedalus.effect;
package com.kzjy.daedalus.effect;
package com.kzjy.daedalus.mixin;
package com.kzjy.daedalus;
print("  [修改] DaedalusEvents.java")
print("  git add .")
print("  git push")
print("=" * 60)
print("\n" + "=" * 60)
print("\n[10] 修正 LovePoemSwordItem...")
print("\n[11] 修正 MixinSynchedEntityData...")
print("\n[12] 修正 MixinLivingDamageEvent...")
print("\n[13] 简化 MixinLivingEvent...")
print("\n[1] 修正 @EventBusSubscriber 注解...")
print("\n[2] 修正 DaedalusEvents...")
print("\n[3] 修正 ItemStack NBT API...")
print("\n[4] 修正 AbyssalCurseEffect...")
print("\n[5] 修正 MarkOfSinEffect...")
print("\n[6] 修正 ClientSetup...")
print("\n[7] 修正 DaedalusRenderTypes...")
print("\n[8] 修正 DaedalusGlowRenderer...")
print("\n[9] 修正 DaedalusModelLoader...")
print("\n下一步:")
print("Round 2 修复完成")
print('  git commit -m "fix: NeoForge 1.21.1 API round 2"')
public abstract class MixinLivingEvent extends EntityEvent implements IDaedalusLivingEvent {
public class AbyssalCurseEffect extends MobEffect {
public class ClientSetup {
public class DaedalusModelLoader implements IGeometryLoader<DaedalusModelLoader.DaedalusCosmicGeometry> {
public class MarkOfSinEffect extends MobEffect {
RES = P / "src" / "main" / "resources"
rt = SRC / "client" / "DaedalusRenderTypes.java"
SRC = P / "src" / "main" / "java" / "com" / "kzjy" / "daedalus"
write_file(SRC / "client" / "model" / "DaedalusModelLoader.java", """\
write_file(SRC / "ClientSetup.java", """\
write_file(SRC / "effect" / "AbyssalCurseEffect.java", """\
write_file(SRC / "effect" / "MarkOfSinEffect.java", """\
write_file(SRC / "mixin" / "MixinLivingEvent.java", """\
}
}
}
}
}