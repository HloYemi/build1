#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 4: 移除 LovePoemSwordItem 及其全部依赖 + 生成测试指南
"""
import re
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SRC = P / "src/main/java/com/kzjy/daedalus"
RES = P / "src/main/resources"

# ============ 1. 删除剑及其相关文件 ============
print("[1] 删除剑相关文件...")
to_delete = [
    "item/LovePoemSwordItem.java",
    "mixin/MixinItemInHandRenderer.java",
    "mixin/MixinTooltipColor.java",
    "client/renderer/DaedalusWeaponConfig.java",
    "client/renderer/DaedalusRenderHelper.java",
]
for f in to_delete:
    p = SRC / f
    if p.exists():
        p.unlink()
        print(f"  [删除] {f}")

# ============ 2. 清理 DaedalusRegistries ============
print("\n[2] 清理 DaedalusRegistries...")
reg = SRC / "registry" / "DaedalusRegistries.java"
if reg.exists():
    c = reg.read_text(encoding="utf-8")
    c = re.sub(r'[ \t]*public static final DeferredHolder<Item, Item> LOVE_POEM_SWORD[^\n]*\n', '', c)
    c = re.sub(r'[ \t]*output\.accept\(LOVE_POEM_SWORD\.get\(\)\.getDefaultInstance\(\)\);\n', '', c)
    c = re.sub(r'import com\.kzjy\.daedalus\.item\.LovePoemSwordItem;\n', '', c)
    reg.write_text(c, encoding="utf-8")
    print("  [修改] DaedalusRegistries.java")

# ============ 3. 清理 DaedalusEvents ============
print("\n[3] 清理 DaedalusEvents...")
ev = SRC / "event" / "DaedalusEvents.java"
if ev.exists():
    c = ev.read_text(encoding="utf-8")
    old_block = '''    private static boolean isAbsoluteTrueDamage(ItemStack s) {
        if (s.is(DaedalusRegistries.LOVE_POEM_SWORD.get())) return true;
        return DaedalusConfig.COMMON.stellarEaterEnabled.get()
                && DaedalusEnchantments.getLevel(s, DaedalusEnchantments.STELLAR_EATER) > 0;
    }'''
    new_block = '''    private static boolean isAbsoluteTrueDamage(ItemStack s) {
        return DaedalusConfig.COMMON.stellarEaterEnabled.get()
                && DaedalusEnchantments.getLevel(s, DaedalusEnchantments.STELLAR_EATER) > 0;
    }'''
    if old_block in c:
        c = c.replace(old_block, new_block)
        print("  [修改] isAbsoluteTrueDamage")

    death_block = '''                if (w.is(DaedalusRegistries.LOVE_POEM_SWORD.get())) {
                    DaedalusDeathManager.markForExecution(t);
                    DaedalusDeathManager.executeExecution(t, event.getSource());
                }
'''
    if death_block in c:
        c = c.replace(death_block, '')
        print("  [修改] 移除 markForExecution 段")

    ev.write_text(c, encoding="utf-8")

# ============ 4. 清理 MixinDamageSources ============
print("\n[4] 清理 MixinDamageSources...")
mds = SRC / "mixin" / "MixinDamageSources.java"
if mds.exists():
    c = mds.read_text(encoding="utf-8")
    old_block = '''    private static boolean isBypass(ItemStack s) {
        return (DaedalusConfig.COMMON.stellarEaterEnabled.get()
                && DaedalusEnchantments.getLevel(s, DaedalusEnchantments.STELLAR_EATER) > 0)
                || s.is(DaedalusRegistries.LOVE_POEM_SWORD.get());
    }'''
    new_block = '''    private static boolean isBypass(ItemStack s) {
        return DaedalusConfig.COMMON.stellarEaterEnabled.get()
                && DaedalusEnchantments.getLevel(s, DaedalusEnchantments.STELLAR_EATER) > 0;
    }'''
    if old_block in c:
        c = c.replace(old_block, new_block)
    c = c.replace("import com.kzjy.daedalus.registry.DaedalusRegistries;\n", "")
    mds.write_text(c, encoding="utf-8")
    print("  [修改] MixinDamageSources.java")

# ============ 5. 重写 DaedalusForgeClientEvents（仅保留附魔 tooltip）============
print("\n[5] 重写 DaedalusForgeClientEvents...")
(SRC / "client" / "DaedalusForgeClientEvents.java").write_text('''package com.kzjy.daedalus.client;

import com.kzjy.daedalus.Daedalus;
import com.kzjy.daedalus.client.gui.DaedalusTooltipData;
import com.kzjy.daedalus.enchantment.util.EnchantmentTheme;
import com.kzjy.daedalus.registry.DaedalusEnchantments;
import com.mojang.datafixers.util.Either;
import net.minecraft.client.resources.language.I18n;
import net.minecraft.core.Holder;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.enchantment.Enchantment;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.client.event.RenderTooltipEvent;

@EventBusSubscriber(modid = Daedalus.MODID, value = Dist.CLIENT)
public class DaedalusForgeClientEvents {

    @SubscribeEvent
    public static void onGatherTooltipComponents(RenderTooltipEvent.GatherComponents event) {
        ItemStack s = event.getItemStack();
        for (var entry : s.getEnchantments().entrySet()) {
            Holder<Enchantment> holder = entry.getKey();
            var keyOpt = holder.unwrapKey();
            if (keyOpt.isEmpty()) continue;
            ResourceKey<Enchantment> key = keyOpt.get();
            if (!key.location().getNamespace().equals(Daedalus.MODID)) continue;
            EnchantmentTheme theme = DaedalusEnchantments.getTheme(key);
            if (theme == null) continue;

            String base = holder.value().description().getString();
            String dk = key.location().toLanguageKey("enchantment") + ".desc";
            String full = I18n.exists(dk) ? I18n.get(dk) : "";

            for (int i = 0; i < event.getTooltipElements().size(); i++) {
                var el = event.getTooltipElements().get(i);
                if (el.left().isEmpty()) continue;
                String line = el.left().get().getString();
                boolean isTitle = line.contains(base);
                boolean isDesc = !full.isEmpty() && !isTitle && full.contains(line.trim()) && line.trim().length() > 4;
                if (isTitle || isDesc)
                    event.getTooltipElements().set(i, Either.right(new DaedalusTooltipData(
                            Component.literal(line), theme, -1, true)));
            }
        }
    }
}
''', encoding="utf-8")
print("  [重写] DaedalusForgeClientEvents.java")

# ============ 6. 清理 mixins.json ============
print("\n[6] 更新 mixins.json...")
mj = RES / "daedalus.mixins.json"
if mj.exists():
    c = mj.read_text(encoding="utf-8")
    c = re.sub(r'\s*"MixinItemInHandRenderer",?', '', c)
    c = re.sub(r'\s*"MixinTooltipColor",?', '', c)
    c = re.sub(r',\s*\]', ']', c)
    mj.write_text(c, encoding="utf-8")
    print("  [修改] daedalus.mixins.json")

# ============ 7. 生成测试指南 ============
print("\n[7] 生成测试指南...")
guide = '''# Daedalus 附魔测试指南

> 移植目标：Minecraft 1.21.1 / NeoForge 21.1.x
> 测试方式：创造模式 + 附魔书（`items` 搜索 `Enchanted Book`，用 `/give` 或从创造标签页拿）
> 快速给书：`/give @s enchanted_book{StoredEnchantments:[{id:"daedalus:daedalus_bow",lvl:5}]}`
> 查看配置：`config/daedalus-common.toml`

---

## 附魔速查表

| # | 附魔 | ID | 槽位 | 最大等级 | 核心效果 |
|---|---|---|---|---|---|
| 1 | 代达罗斯之弓 | `daedalus_bow` | 主手/副手 | 5 | 提高拉弓速度 |
| 2 | 深渊凝视 | `abyssal_gaze` | 头盔 | 3 | 视线接触施加深渊诅咒 |
| 3 | 诅咒锁链 | `cursed_chain` | 主手 | 5 | 降低自身伤害 + 反弹诅咒伤害 |
| 4 | 罪孽印记 | `mark_of_sin` | 主手 | 4 | 攻击附加百分比扣血 |
| 5 | 虚空撕裂 | `void_rend` | 主手 | 3 | 真实伤害保底 + 残血斩杀 |
| 6 | 灵魂饥渴 | `soul_thirst` | 主手 | 5 | 击杀收集灵魂，满魂爆发 |
| 7 | 深渊的加护 | `abyssal_protection` | 胸甲 | 5 | 减伤 + 闪避 |
| 8 | 虚空破壁 | `void_breach` | 主手 | 1 | 无视无敌帧 |
| 9 | 神圣裁决 | `divine_judgment` | 主手 | 5 | 对亡灵加伤 + 治愈僵尸村民 |
| 10 | 天使的加护 | `angelic_protection` | 胸甲/护腿 | 4 | 飞行 + 亡灵减伤 + 治疗增幅 |
| 11 | 生命虹吸 | `life_siphon` | 主手 | 5 | 攻击回血 |
| 12 | 耀星之噬 | `stellar_eater` | 主手 | 1 | 绝对真伤，无视一切防御 |
| 13 | 不朽 | `immortal` | 全套盔甲 | 3 | 动态减伤 + 免疫负面效果 |

---

## 详细测试说明

### 1. 代达罗斯之弓
- **装备**：弓 / 弩 / 三叉戟
- **效果**：每级 +5% 蓄力速度
- **测试**：
  1. 拿一把普通弓，拉满一次记时间
  2. 用 `/give @s bow{Enchantments:[{id:"daedalus:daedalus_bow",lvl:5}]}` 拿 5 级弓
  3. 拉满明显更快（5 级约缩短 25%）
- **预期**：无箭矢消耗变化，只是蓄力变快

### 2. 深渊凝视
- **装备**：头盔
- **效果**：看向生物（视锥 0.95、距离 ≤ 20 格、有视线）每 5 tick 施加"深渊诅咒"
- **深渊诅咒本身**：每级 -10% 护甲、-5% 韧性、输出 -10%（最多 -80%）
- **测试**：
  1. 戴 3 级头盔
  2. 看向一只僵尸（别攻击）
  3. 检查僵尸是否出现了紫色药水粒子（深渊诅咒）
  4. 让僵尸攻击你，伤害应该降低
- **坑点**：视线要求很严，必须瞄准目标中心

### 3. 诅咒锁链
- **装备**：主手武器
- **效果**：等级 N 时自身伤害 ×(1 - (0.5 - 0.05N))，并附加 0.1N 倍魔法伤害
- **数值**：
  - 1 级：自身 0.55 倍 + 0.1 倍魔法 = 0.65 倍有效
  - 5 级：自身 0.75 倍 + 0.5 倍魔法 = **1.25 倍有效**
- **测试**：
  1. 5 级附魔打僵尸，血量下降应比无附魔时更多
  2. 但物理伤害数字比无附魔低
- **坑点**：是「负收益前期，正收益后期」

### 4. 罪孽印记
- **装备**：主手武器
- **效果**：命中后施加 `MarkOfSinEffect`（100 tick），每 20 tick 扣 `maxHP * (5% + 1%×amplifier)`
- **数值**：等级 N 时 amp = N-1，单次扣血 = maxHP × (5% + 1%×(N-1))
- **测试**：
  1. 给木剑附 4 级
  2. 打僵尸一刀，看僵尸头顶的红色药水图标
  3. 5 秒内僵尸持续掉血，总计约 `5 × 8% = 40%` 最大生命
- **坑点**：对高强度 Boss 也按百分比扣血，非常强力

### 5. 虚空撕裂
- **装备**：主手武器
- **效果**：至少造成 `ATK × 5% × N` 伤害（无视护甲）；目标血量 < 5% 时有 `10% × N` 概率直接死亡
- **测试**：
  1. 给木剑附 3 级，打一只铁傀儡（护甲高）
  2. 每次至少掉 15% 攻击力，伤害稳定
  3. 把一只僵尸打到残血（血条红），继续攻击，有机会直接秒
- **坑点**：斩杀对 Boss 也有效（除非有无敌）

### 6. 灵魂饥渴
- **装备**：主手武器
- **效果**：每次击杀 + `N` 灵魂（上限 10）；满 10 时下次攻击额外造成 `eventDamage × (4 + (N-1)×0.5)` 魔法伤害，然后清零
- **测试**：
  1. 5 级附魔，杀 10 只怪
  2. 用鼠标悬停武器看 tooltip 是否显示 `Souls: 10/10`
  3. 打下一只怪，伤害爆炸（5 级约 6 倍爆发）
- **坑点**：爆发是纯魔法伤害，不受护甲减免

### 7. 深渊的加护
- **装备**：胸甲
- **效果**：每级 +5% 闪避（完全免疫）、-10% 伤害；对虚空破壁/耀星之噬无效
- **测试**：
  1. 穿 5 级胸甲
  2. 让僵尸围殴 20 次，应该有约 1/4 完全无伤
  3. 其余伤害减半
- **坑点**：闪避走 `setNewDamage(0)`，实际减伤 100%

### 8. 虚空破壁
- **装备**：主手武器
- **效果**：攻击前将目标无敌帧归零，连续攻击不被打断；穿透 `BYPASSES_INVULNERABILITY` 和 `BYPASSES_COOLDOWN`
- **测试**：
  1. 用 1 级附魔的剑，狂点僵尸
  2. 每下都造成伤害（普通剑第二次攻击会被无敌帧挡住）
  3. 攻击凋灵 Boss，无敌计时器也被清零
- **坑点**：不提高伤害，只消除攻击间隔限制

### 9. 神圣裁决
- **装备**：主手武器
- **效果**：对亡灵（僵尸/骷髅/凋灵/僵尸猪灵等）伤害 ×(1 + 10%×N)；命中僵尸村民时 `20%×N` 概率触发治愈
- **测试**：
  1. 5 级附魔打僵尸，伤害是 1.5 倍
  2. 打非亡灵（牛、猪）无加成
  3. 打僵尸村民（用刷怪蛋或自然生成），有概率把它变成普通村民
- **坑点**：治愈走 `startConverting`，等同于金苹果效果

### 10. 天使的加护
- **装备**：胸甲 / 护腿
- **效果**：
  - 亡灵减伤 25%/级（上限 99%）
  - 治疗效果 ×(1 + level)
  - **胸甲 + 护腿同等级时额外 +1 级**，达到 4 级获得创造模式飞行
  - 4 级时治疗量不会为负，最少恢复 5% 最大生命
- **测试**：
  1. 胸甲 4 级 + 护腿 4 级（合成等级 = 4+1 = 5），有创造飞行
  2. 只穿 4 级胸甲，合成等级 = 4，也能飞
  3. 让僵尸打你，伤害只承受 25%（4 级 × 25% = 100%...其实是 min(99%, 4×25%)=99%）
  4. 服用瞬间治疗药水，恢复量放大 5 倍
- **坑点**：飞行能力会在脱下后自动取消

### 11. 生命虹吸
- **装备**：主手武器
- **效果**：命中时回复 `damage × (10% + 5%×(N-1))`
- **数值**：5 级 30% 吸血
- **测试**：
  1. 5 级附魔，故意掉血到 5 心
  2. 打僵尸，血量快速回升
- **坑点**：是吸血不是命中固定值，攻击力越高吸得越多

### 12. 耀星之噬
- **装备**：主手武器
- **效果**：`BypassAll`——穿透护甲、盾牌、无敌帧、抗性、药水、`Cataclysm` 伤害上限；伤害只增不减、不可取消
- **测试**：
  1. 打凋灵（无敌状态），伤害照样生效
  2. 打穿钻石全套的玩家，护甲完全无效
  3. 打手持盾牌的玩家，盾牌不挡伤害
  4. 打自定义血量上限的 Boss，伤害不受限
- **坑点**：这是伤害系统的"降维打击"，可以视为终极武器

### 13. 不朽
- **装备**：全套盔甲（头盔/胸甲/护腿/靴子任意部位，取最高等级）
- **效果**：
  - 受到伤害后进入"减伤累积"状态，持续 `20 + 5×N` tick
  - 每次受伤累积乘数 `×(1 - (50% + 5%×N))`，最低 0.01（即极限 99% 减伤）
  - 状态期间**免疫所有负面药水效果**（无法被施加）
- **测试**：
  1. 穿 3 级全套，被打一下减伤 65%
  2. 立刻再被打，总减伤 = 0.35 × 0.35 = 12.25%（约 88% 减伤）
  3. 3 次连击后几乎无伤
  4. 被人扔中毒药水，无效
- **坑点**：乘法累积所以很快能到极限，35 tick 后自动解除

---

## 测试顺序建议

**第一阶段（机制验证）**：虚空破壁 → 耀星之噬 → 虚空撕裂 → 诅咒锁链
这是伤害系统主线，先确认数值正确。

**第二阶段（防御机制）**：深渊的加护 → 不朽 → 天使的加护
确认减伤叠加和飞行。

**第三阶段（辅助机制）**：生命虹吸 → 灵魂饥渴 → 罪孽印记 → 神圣裁决
确认附加伤害和治疗。

**第四阶段（特殊）**：代达罗斯之弓 → 深渊凝视
这两个是触发型机制，单独测试。

---

## 常见问题排查

| 现象 | 可能原因 |
|---|---|
| 附魔书没显示名字 | `lang/*.json` 缺 `enchantment.daedalus.<id>` |
| 附魔不生效 | 配置 `enabled=false`，检查 `config/daedalus-common.toml` |
| 虚空破壁无效 | 目标没有 `BYPASSES_INVULNERABILITY` 标签支持 |
| 灵魂饥渴不显示 Souls | tooltip 走了 `onItemTooltip`，检查是否被其他 mod 覆盖 |
| 深渊凝视不触发 | 视线角度不够严格（要求 dot > 0.95） |
| 天使加护无法飞行 | 等级 < 4，注意"胸甲 + 护腿同等级 +1"规则 |
'''
(P / "ENCHANTMENT_TEST_GUIDE.md").write_text(guide, encoding="utf-8")
print("  [生成] ENCHANTMENT_TEST_GUIDE.md")

print("\n" + "=" * 60)
print("Round 4 完成")
print("=" * 60)
print("\n下一步:")
print("  git add .")
print('  git commit -m "chore: remove love poem sword, add test guide"')
print("  git push")