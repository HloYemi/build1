#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daedalus NeoForge 1.21.1 - Round 6
移除 MobEffectEvent.Applicable 监听（setResult API 不稳定），
改用已有的 onEntityTick 每 10 tick 清除有害效果逻辑。
"""
import re
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
ev = P / "src" / "main" / "java" / "com" / "kzjy" / "daedalus" / "event" / "DaedalusEvents.java"

c = ev.read_text(encoding="utf-8")
orig_len = len(c)

# 1. 删除整个 onMobEffectApplicable 方法（连同上面的 @SubscribeEvent）
pattern = re.compile(
    r'\n    @SubscribeEvent\n    public static void onMobEffectApplicable\(MobEffectEvent\.Applicable event\) \{.*?\n    \}\n',
    re.DOTALL
)
c, n = pattern.subn('\n', c)
print(f"[1] 删除 onMobEffectApplicable: {'成功' if n else '未找到'}")

# 2. 清理 TriState 相关 import
for imp in [
    "import net.neoforged.neoforge.common.TriState;\n",
    "import net.neoforged.neoforge.common.util.TriState;\n",
]:
    if imp in c:
        c = c.replace(imp, "")
        print(f"[2] 移除 import: {imp.strip()}")

# 3. 清理 MobEffectEvent 单独 import（如果有）
for imp in [
    "import net.neoforged.neoforge.event.entity.living.MobEffectEvent;\n",
]:
    if imp in c:
        c = c.replace(imp, "")
        print(f"[3] 移除 import: {imp.strip()}")

ev.write_text(c, encoding="utf-8")
print(f"\n文件长度: {orig_len} -> {len(c)}")

# 快速验证
content = ev.read_text(encoding="utf-8")
if "onMobEffectApplicable" in content:
    print("[警告] onMobEffectApplicable 仍在文件中，请手工检查")
else:
    print("[验证] onMobEffectApplicable 已彻底移除")

if "TriState" in content:
    print("[警告] 仍有 TriState 引用:")
    for line in content.splitlines():
        if "TriState" in line:
            print("   ", line.strip())

print("\n" + "=" * 60)
print("Round 6 修复完成")
print("=" * 60)
print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: remove MobEffectEvent.Applicable listener (final)"')
print("  git push")