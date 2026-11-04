#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daedalus NeoForge 1.21.1 - fix_round.py
当前轮次: Round 7
修复: 附魔 JSON 的 min_cost / max_cost 缺少 per_level_above_first 字段
影响: void_breach.json, stellar_eater.json (max_level=1 的附魔)
机制: 1.21.1 附魔 codec 要求该字段必须存在，即使值为 0
"""
import json
from pathlib import Path

P = Path(r"D:\AAA.DownLoad\Daedalus_Enchantment-main")
ENCH_DIR = P / "src/main/resources/data/daedalus/enchantment"

if not ENCH_DIR.exists():
    print(f"[错误] 目录不存在: {ENCH_DIR}")
    raise SystemExit(1)

print(f"扫描 {ENCH_DIR} 下的附魔 JSON...\n")

fixed = 0
skipped = 0
for f in sorted(ENCH_DIR.glob("*.json")):
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[解析失败] {f.name}: {e}")
        continue

    changed = False
    for key in ("min_cost", "max_cost"):
        if key in data and isinstance(data[key], dict):
            if "per_level_above_first" not in data[key]:
                data[key]["per_level_above_first"] = 0
                changed = True

    if changed:
        f.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8"
        )
        print(f"[修复] {f.name}")
        fixed += 1
    else:
        skipped += 1

print(f"\n修复: {fixed} 个文件，跳过: {skipped} 个文件")

# 校验修复后的 void_breach 和 stellar_eater
for name in ("void_breach", "stellar_eater"):
    target = ENCH_DIR / f"{name}.json"
    if target.exists():
        data = json.loads(target.read_text(encoding="utf-8"))
        print(f"\n{name}.json 修复后:")
        print(f"  max_level = {data.get('max_level')}")
        print(f"  min_cost = {data.get('min_cost')}")
        print(f"  max_cost = {data.get('max_cost')}")

print("\n" + "=" * 60)
print("Round 7 修复完成")
print("=" * 60)
print("\n下一步:")
print("  git add .")
print('  git commit -m "fix: add per_level_above_first to max_level=1 enchantment costs"')
print("  git push")