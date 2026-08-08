#!/usr/bin/env python3
"""检查当前配置"""
import sys, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('E:/DEV/clash-rules/current_config.json', 'r', encoding='utf-8') as f:
    raw = f.read()
raw = re.sub(r'^[0-9a-fA-F]+\r?\n', '', raw)
raw = raw.rstrip('0').strip().lstrip('\ufeff')
obj = json.loads(raw)
print('=== 当前配置 ===')
print('mixed-port:', obj.get('mixed-port'))
print('tun enabled:', obj.get('tun', {}).get('enable'))
print()
rp = obj.get('rule-providers', {})
print(f'rule-providers 数量: {len(rp)}')
for name, info in rp.items():
    url = info.get('url', 'N/A')
    uri = info.get('path', 'N/A')
    print(f'  {name:<15} url={url}')