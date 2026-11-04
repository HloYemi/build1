#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
保留剑，修复 HIDE_TOOLTIP 导致的创造物品栏崩溃
"""
import re
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SRC = P / "src/main/java/com/kzjy/daedalus"

# ===== 1. 修改 LovePoemSwordItem.java =====
print("[1] 修改 LovePoemSwordItem.getDefaultInstance()...")
sword = SRC / "item" / "LovePoemSwordItem.java"
if not sword.exists():
    print("  [错误] 文件不存在！请先确认剑源码还在")
    exit(1)

c = sword.read_text(encoding="utf-8")

old_block = '''    @Override
    public ItemStack getDefaultInstance() {
        ItemStack stack = new ItemStack(this);
        stack.set(DataComponents.HIDE_TOOLTIP, Unit.INSTANCE);
        return stack;
    }'''

new_block = '''    @Override
    public ItemStack getDefaultInstance() {
        ItemStack stack = new ItemStack(this);
        // 1.21.1 的 HIDE_TOOLTIP 会让 getTooltipLines() 返回 List.of()（不可变空列表），
        // 不触发 ItemTooltipEvent，并在 CreativeModeInventoryScreen.getTooltipFromContainerItem
        // 中导致 IndexOutOfBoundsException。
        // 改用 HIDE_ADDITIONAL_TOOLTIP：只隐藏属性加成，保留名称 + lore，列表非空。
        stack.set(DataComponents.HIDE_ADDITIONAL_TOOLTIP, Unit.INSTANCE);
        return stack;
    }'''

if old_block in c:
    c = c.replace(old_block, new_block)
    print("  [修改] getDefaultInstance: HIDE_TOOLTIP -> HIDE_ADDITIONAL_TOOLTIP")
elif "HIDE_ADDITIONAL_TOOLTIP" in c:
    print("  [跳过] 已是 HIDE_ADDITIONAL_TOOLTIP")
else:
    # 尝试正则匹配更宽松的写法
    c = re.sub(
        r'stack\.set\(DataComponents\.HIDE_TOOLTIP,\s*Unit\.INSTANCE\)',
        'stack.set(DataComponents.HIDE_ADDITIONAL_TOOLTIP, Unit.INSTANCE)',
        c)
    print("  [修改] 正则替换 HIDE_TOOLTIP -> HIDE_ADDITIONAL_TOOLTIP")

sword.write_text(c, encoding="utf-8")

# ===== 2. 清理 DaedalusForgeClientEvents 的死代码 =====
print("\n[2] 清理 DaedalusForgeClientEvents.ensureNonEmptyTooltip...")
fce = SRC / "client" / "DaedalusForgeClientEvents.java"
if fce.exists():
    c = fce.read_text(encoding="utf-8")
    # 移除 ensureNonEmptyTooltip 方法（ItemTooltipEvent 不会因 HIDE_TOOLTIP 触发，死代码）
    c = re.sub(
        r'\s*@SubscribeEvent\(priority = net\.neoforged\.bus\.api\.EventPriority\.LOWEST\)\s*'
        r'public static void ensureNonEmptyTooltip\(ItemTooltipEvent event\) \{.*?\n    \}',
        '', c, flags=re.DOTALL)
    # 移除未使用的 import
    c = c.replace("import net.minecraft.client.gui.screens.inventory.CreativeModeInventoryScreen;\n", "")
    c = c.replace("import net.minecraft.client.Minecraft;\n", "import net.minecraft.client.Minecraft;\n")
    fce.write_text(c, encoding="utf-8")
    print("  [修改] 移除 ensureNonEmptyTooltip 死代码")
else:
    print("  [跳过] 文件不存在")

# ===== 3. 确认 mixins.json 仍包含剑的两个 mixin =====
print("\n[3] 检查 daedalus.mixins.json...")
mj = P / "src/main/resources/daedalus.mixins.json"
if mj.exists():
    c = mj.read_text(encoding="utf-8")
    need = ["MixinItemInHandRenderer", "MixinTooltipColor"]
    missing = [m for m in need if m not in c]
    if missing:
        print(f"  [警告] 缺少: {missing}，剑的格挡动画/边框效果会失效")
    else:
        print("  [OK] 两个 mixin 都在")

# ===== 4. 确认 DaedalusRegistries 仍注册 LOVE_POEM_SWORD =====
print("\n[4] 检查 DaedalusRegistries...")
reg = SRC / "registry" / "DaedalusRegistries.java"
if reg.exists():
    c = reg.read_text(encoding="utf-8")
    if "LOVE_POEM_SWORD" in c and "LovePoemSwordItem::new" in c:
        print("  [OK] LOVE_POEM_SWORD 注册存在")
    else:
        print("  [错误] LOVE_POEM_SWORD 注册缺失！剑将无法在游戏中出现")

# ===== 5. 确认 Daedalus.java 仍注册 ITEMS =====
print("\n[5] 检查 Daedalus.java...")
main = SRC / "Daedalus.java"
if main.exists():
    c = main.read_text(encoding="utf-8")
    if "ITEMS.register" in c:
        print("  [OK] ITEMS 注册存在")
    else:
        print("  [错误] ITEMS 注册缺失！请恢复 DaedalusRegistries.ITEMS.register(modEventBus)")

# ===== 6. 确认 lang 文件有剑的翻译 =====
print("\n[6] 检查语言文件...")
for lang in ["en_us.json", "zh_cn.json"]:
    lf = P / f"src/main/resources/assets/daedalus/lang/{lang}"
    if lf.exists():
        c = lf.read_text(encoding="utf-8")
        keys = ["item.daedalus.love_poem_sword", "desc1.line1", "hold_alt", "speed_value"]
        missing = [k for k in keys if k not in c]
        if missing:
            print(f"  [警告] {lang} 缺少: {missing}")
        else:
            print(f"  [OK] {lang} 翻译完整")

print("\n" + "=" * 60)
print("修复完成")
print("=" * 60)
print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: use HIDE_ADDITIONAL_TOOLTIP to avoid creative inventory crash"')
print("  git push")
print("\n推送后 Actions 自动构建，完成后从 Artifacts 下载新 jar 替换 mods 里的旧 jar")