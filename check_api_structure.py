#!/usr/bin/env python3
"""检查 API 响应结构"""
import sys, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('E:/DEV/clash-rules/providers_list.json', 'r', encoding='utf-8') as f:
    raw = f.read().strip()
raw = re.sub(r'^[0-9a-fA-F]+\r?\n', '', raw)
raw = raw.rstrip('0').strip().lstrip('\ufeff')
obj = json.loads(raw)

# 检查 response 结构
print('顶层 keys:', list(obj.keys()))

# 检查 direct provider 的结构
dp = obj.get('providers', {}).get('direct', {})
print()
print('direct provider keys:', list(dp.keys()))
print('direct ruleCount:', dp.get('ruleCount'))
print('direct rules type:', type(dp.get('rules')))
if isinstance(dp.get('rules'), dict):
    print('direct rules keys:', list(dp.get('rules', {}).keys())[:5])