#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daedalus NeoForge 1.21.1 - Round 6
修复运行时 Mixin 崩溃: MixinSynchedEntityData 无法定位 @Shadow entity 字段
"""
import re
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
SRC = P / "src" / "main" / "java" / "com" / "kzjy" / "daedalus"
RES = P / "src" / "main" / "resources"

# 1. 删除 MixinSynchedEntityData.java
msd = SRC / "mixin" / "MixinSynchedEntityData.java"
if msd.exists():
    msd.unlink()
    print("[删除] MixinSynchedEntityData.java")
else:
    print("[跳过] MixinSynchedEntityData.java 不存在")

# 2. 从 mixins.json 移除对应条目
mj = RES / "daedalus.mixins.json"
if mj.exists():
    s = mj.read_text(encoding="utf-8")
    before = s
    s = re.sub(r',\s*"MixinSynchedEntityData"(?=\s*[,\]])', '', s)
    s = re.sub(r'"MixinSynchedEntityData"\s*,?\s*', '', s)
    if s != before:
        mj.write_text(s, encoding="utf-8")
        print("[修改] daedalus.mixins.json: 移除 MixinSynchedEntityData")
    else:
        print("[跳过] mixins.json 中没有 MixinSynchedEntityData 条目")
    print("\n当前 mixins.json 内容:")
    print(mj.read_text(encoding="utf-8"))

# 3. 检查是否有其它地方引用 MixinSynchedEntityData
for jf in SRC.rglob("*.java"):
    c = jf.read_text(encoding="utf-8")
    if "MixinSynchedEntityData" in c:
        print(f"[警告] {jf.name} 仍引用 MixinSynchedEntityData，需要手工检查")

print("\n" + "=" * 60)
print("Round 6 修复完成")
print("=" * 60)
print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: remove MixinSynchedEntityData (1.21.1 SynchedEntityData has no entity field)"')
print("  git push")