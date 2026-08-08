#!/usr/bin/env python3
"""检查仍带前缀的规则"""
import os

files = ['reject.txt','microsoft.txt','ai.txt','direct.txt','apple.txt','proxy.txt',
         'steam.txt','icloud.txt','private.txt']
for f in files:
    lines = open('E:/DEV/clash-rules/'+f, encoding='utf-8').read().split('\n')
    prefixed = []
    for l in lines:
        s = l.strip()
        if s.startswith("  - '") or s.startswith("- '"):
            rule = s.replace("  - '", "").replace("- '", "").replace("'", "")
            if rule.startswith('DOMAIN-KEYWORD,') or rule.startswith('DOMAIN,') or rule.startswith('DOMAIN-SUFFIX,'):
                prefixed.append(rule)
    if prefixed:
        print(f'{f}: {len(prefixed)} 条保留前缀:')
        for p in prefixed[:10]:
            print(f'  {p}')
        if len(prefixed) > 10:
            print(f'  ... 还有 {len(prefixed)-10} 条')
        print()