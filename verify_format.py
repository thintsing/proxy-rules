#!/usr/bin/env python3
"""验证转换后的格式"""
import sys

files = ['reject.txt','microsoft.txt','ai.txt','direct.txt','apple.txt','proxy.txt']
for f in files:
    lines = open('E:/DEV/clash-rules/'+f, encoding='utf-8').read().split('\n')
    rules = []
    domains = []
    for l in lines:
        s = l.strip()
        if s.startswith("  - '") or s.startswith("- '"):
            rule = s.replace("  - '", "").replace("- '", "").replace("'", "")
            rules.append(rule)
            has_prefix = rule.startswith('DOMAIN,') or rule.startswith('DOMAIN-SUFFIX,') or rule.startswith('DOMAIN-KEYWORD,')
            if not has_prefix:
                domains.append(rule)
    print(f'{f:<20} {len(rules):>4}条规则, 纯域名: {len(domains):>4}')
    for r in rules[:4]:
        print(f'  {r}')
    print()