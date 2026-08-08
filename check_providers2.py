#!/usr/bin/env python3
"""Check mihomo rule-provider status from a saved JSON file"""
import json
import re
import sys

with open('E:/DEV/clash-rules/providers_raw.json', 'r', encoding='utf-8-sig') as f:
    raw = f.read().strip()

raw = re.sub(r'^[0-9a-fA-F]+\r?\n', '', raw)
raw = raw.rstrip('0').strip()

obj = json.loads(raw)
print('=== Rule-Provider 加载状态 ===')
for name, info in sorted(obj.get('providers', {}).items()):
    rc = info['ruleCount']
    icon = '[OK]' if rc > 0 else '[X]'
    print(f'{icon} {name:<15} behavior={info["behavior"]:<8} rules={rc}')