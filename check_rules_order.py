#!/usr/bin/env python3
"""检查规则顺序"""
import sys, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('E:/DEV/clash-rules/rules2.json', 'r', encoding='utf-8') as f:
    raw = f.read().strip()
raw = re.sub(r'^[0-9a-fA-F]+\r?\n', '', raw)
raw = raw.rstrip('0').strip()
raw = raw.lstrip('\ufeff')
obj = json.loads(raw)
rules = obj.get('rules', [])
print(f'=== 规则顺序 (共 {len(rules)} 条) ===')
for i, r in enumerate(rules):
    rtype = r.get('type', '')
    payload = r.get('payload', '')
    proxy = r.get('proxy', '')
    print(f'{i:>3}. {rtype:<15} {payload:<30} -> {proxy}')