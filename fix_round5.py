#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Round 6: 恢复 RenderBlender 前置依赖（第一步：依赖 + IToolTransform）
DaedalusCosmicBakedModel 暂保持简化版（BakedModelWrapper 透传），
先确认依赖和接口能编译通过，再恢复完整渲染。
"""
import re, zipfile, shutil
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SRC = P / "src/main/java/com/kzjy/daedalus"
LIBS = P / "libs"
MODS = Path(r"D:\GameData\Minecraft\NewMinecraft\.minecraft\versions\1.21.1-NeoForge_21.1.249\mods")

print("=" * 60)
print("Round 6: 恢复 RenderBlender 前置依赖")
print("=" * 60)

# ---------- 1. 定位 RenderBlender jar ----------
rb_jar = None
for d in (LIBS, MODS):
    if d.exists():
        for f in sorted(d.glob("RenderBlender*.jar")):
            rb_jar = f
            break
    if rb_jar:
        break

if not rb_jar:
    print("[错误] 找不到 RenderBlender*.jar")
    print(f"  检查: {LIBS} 或 {MODS}")
    exit(1)
print(f"[找到] {rb_jar}")

# ---------- 2. 检查 jar 内实际类路径 ----------
with zipfile.ZipFile(rb_jar) as z:
    names = z.namelist()
    def find(simple):
        for n in names:
            if n.endswith(f"/{simple}.class") or n == f"{simple}.class":
                return n
        return None
    itool = find("IToolTransform")
    ibow = find("IBowTransform")
    wrapped = find("WrappedItemModel")
    print(f"  IToolTransform      : {itool}")
    print(f"  IBowTransform       : {ibow}")
    print(f"  WrappedItemModel    : {wrapped}")

def to_import(p):
    return p.replace("/", ".").replace(".class", "") if p else None

itool_imp = to_import(itool) or "committee.nova.mods.renderblender.api.iface.transform.IToolTransform"
print(f"  -> IToolTransform import: {itool_imp}")

# ---------- 3. 复制 jar 到 libs ----------
LIBS.mkdir(exist_ok=True)
target = LIBS / rb_jar.name
if not target.exists() or target.stat().st_size != rb_jar.stat().st_size:
    shutil.copy(rb_jar, target)
    print(f"[复制] -> libs/{rb_jar.name}")
else:
    print(f"[跳过] libs/{rb_jar.name} 已存在")

# ---------- 4. 修改 build.gradle ----------
gradle = P / "build.gradle"
c = gradle.read_text(encoding="utf-8")
old_lines = [l for l in c.splitlines() if 'renderblender' in l.lower()]
print(f"[当前 build.gradle renderblender 行] {old_lines}")

new_dep = f"    implementation files('libs/{rb_jar.name}')"
if any('renderblender' in l.lower() for l in c.splitlines()):
    c = re.sub(
        r'(?://\s*)?implementation\s+files\([\'"]libs/[Rr]ender[Bb]lender[^)]+\)',
        new_dep.strip(),
        c)
else:
    c = c.replace("dependencies {", f"dependencies {{\n{new_dep}", 1)
gradle.write_text(c, encoding="utf-8")
print(f"[修改] build.gradle")

# ---------- 5. LovePoemSwordItem implements IToolTransform ----------
sword = SRC / "item/LovePoemSwordItem.java"
c = sword.read_text(encoding="utf-8")
if "implements IToolTransform" not in c:
    if "import committee.nova.mods.renderblender" not in c:
        c = re.sub(
            r'^(import net\.minecraft\.network\.chat\.Style;)',
            f'import net.minecraft.network.chat.Style;\nimport {itool_imp};',
            c, count=1, flags=re.MULTILINE)
    c = c.replace(
        "public class LovePoemSwordItem extends SwordItem {",
        "public class LovePoemSwordItem extends SwordItem implements IToolTransform {")
    sword.write_text(c, encoding="utf-8")
    print(f"[修改] LovePoemSwordItem implements IToolTransform")
else:
    print("[跳过] LovePoemSwordItem 已实现 IToolTransform")

# ---------- 6. 检查 mixins.json 中是否有剑相关的两个 mixin ----------
mj = P / "src/main/resources/daedalus.mixins.json"
if mj.exists():
    c = mj.read_text(encoding="utf-8")
    missing = [m for m in ("MixinItemInHandRenderer", "MixinTooltipColor") if m not in c]
    if missing:
        print(f"[警告] daedalus.mixins.json 缺少: {missing}")
        print(f"       （不影响编译，但剑的格挡动画/彩虹边框会失效）")

# ---------- 7. 检查 DaedalusRegistries ----------
reg = SRC / "registry/DaedalusRegistries.java"
if reg.exists():
    c = reg.read_text(encoding="utf-8")
    if "LOVE_POEM_SWORD" not in c:
        print("[警告] DaedalusRegistries 中 LOVE_POEM_SWORD 缺失！")
    else:
        print("[OK] LOVE_POEM_SWORD 注册存在")

print("\n" + "=" * 60)
print("完成")
print("=" * 60)
print("\n下一步:")
print("  git add .")
print('  git commit -m "feat: restore RenderBlender dependency + IToolTransform"')
print("  git push")
print("\n预期: 编译通过。游戏内剑的手部变换恢复（不再偏斜/放大）。")
print("      但 cosmic 星空、glow_edge 描边、虹光晕仍不渲染（简化版模型）。")
print("      下一步再做 DaedalusCosmicBakedModel 完整恢复。")