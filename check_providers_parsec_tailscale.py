#!/usr/bin/env python3
"""检查所有 providers 中的 tailscale 和 parsec 规则"""
import sys, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('E:/DEV/clash-rules/providers_list.json', 'r', encoding='utf-8') as f:
    raw = f.read().strip()
raw = re.sub(r'^[0-9a-fA-F]+\r?\n', '', raw)
raw = raw.rstrip('0').strip().lstrip('\ufeff')
obj = json.loads(raw)
providers = obj.get('providers', {})

for name, info in sorted(providers.items()):
    for r in info.get('rules', {}):
        payload = r.get('payload', '')
        if 'tailscale' in payload.lower() or 'parsec' in payload.lower() or 'parsecd' in payload.lower() or 'Parsec' in payload:
            proxy = r.get('proxy', '')
            print(f'[{name}] {payload} -> {proxy}')