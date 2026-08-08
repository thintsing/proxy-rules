#!/usr/bin/env python3
"""验证 direct provider 中的 tailscale 规则"""
import sys, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('E:/DEV/clash-rules/direct_provider.json', 'r', encoding='utf-8') as f:
    raw = f.read().strip()
raw = re.sub(r'^[0-9a-fA-F]+\r?\n', '', raw)
raw = raw.rstrip('0').strip().lstrip('\ufeff')
obj = json.loads(raw)
p = obj.get('provider', obj)
print('ruleCount:', p.get('ruleCount'))
print('behavior:', p.get('behavior'))
print('vehicleType:', p.get('vehicleType'))
print()
print('=== tailscale 相关规则 ===')
for r in p.get('rules', {}):
    payload = r.get('payload', '')
    if 'tailscale' in payload or payload == 'ts.tailscale.com':
        print(f'  {r.get("type")} {payload} -> {r.get("proxy")}')