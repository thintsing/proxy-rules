#!/usr/bin/env python3
"""检查 direct 和 applications providers 中的规则样本"""
import sys, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('E:/DEV/clash-rules/providers_list.json', 'r', encoding='utf-8') as f:
    raw = f.read().strip()
raw = re.sub(r'^[0-9a-fA-F]+\r?\n', '', raw)
raw = raw.rstrip('0').strip().lstrip('\ufeff')
obj = json.loads(raw)
providers = obj.get('providers', {})

for name in ('direct', 'applications'):
    info = providers.get(name, {})
    rules = info.get('rules', {})
    print(f'=== {name} (共 {len(rules)} 条) ===')
    count = 0
    for r in rules:
        payload = r.get('payload', '')
        rtype = r.get('type', '')
        proxy = r.get('proxy', '')
        # 显示最后 10 条规则
        if count >= len(rules) - 10:
            print(f'  [{rtype}] {payload} -> {proxy}')
        count += 1
    print()