#!/usr/bin/env python3
"""检查 applications provider 中的 tailscale 规则"""
import sys, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('E:/DEV/clash-rules/app_provider.json', 'r', encoding='utf-8') as f:
    raw = f.read().strip()
raw = re.sub(r'^[0-9a-fA-F]+\r?\n', '', raw)
raw = raw.rstrip('0').strip().lstrip('\ufeff')
obj = json.loads(raw)
p = obj.get('provider', obj)
print('ruleCount:', p.get('ruleCount'))
print('behavior:', p.get('behavior'))
print('vehicleType:', p.get('vehicleType'))
print()
print('=== tailscale 进程规则 ===')
for r in p.get('rules', {}):
    payload = r.get('payload', '')
    if 'tailscale' in payload.lower():
        proxy = r.get('proxy', '')
        print(f'  {payload} -> {proxy}')