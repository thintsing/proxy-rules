#!/usr/bin/env python3
"""检查 providers 列表中的 tailscale 规则"""
import sys, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('E:/DEV/clash-rules/providers_list.json', 'r', encoding='utf-8') as f:
    raw = f.read().strip()
raw = re.sub(r'^[0-9a-fA-F]+\r?\n', '', raw)
raw = raw.rstrip('0').strip().lstrip('\ufeff')
obj = json.loads(raw)
providers = obj.get('providers', {})

print(f'providers 数量: {len(providers)}')
print()
for name, info in sorted(providers.items()):
    rc = info.get('ruleCount', 0)
    bt = info.get('behavior', '')
    vt = info.get('vehicleType', '')
    print(f'{name:<15} ruleCount={rc:<5} behavior={bt:<10} vehicleType={vt}')
    if name in ('direct', 'applications'):
        # 检查 tailscale 相关规则
        for r in info.get('rules', {}):
            payload = r.get('payload', '')
            if 'tailscale' in payload.lower() or 'parsec' in payload.lower() or 'parsecd' in payload.lower() or 'Parsec' in payload:
                print(f'    -> {payload}  proxy={r.get("proxy", "")}')