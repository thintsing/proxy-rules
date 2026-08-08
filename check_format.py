#!/usr/bin/env python3
"""检查规则文件格式，对比 Loyalsoldier"""
import os

base = 'E:/DEV/clash-rules/'
files = ['reject.txt','proxy.txt','direct.txt','apple.txt','steam.txt',
         'ai.txt','icloud.txt','private.txt','microsoft.txt',
         'lancidr.txt','telegramcidr.txt','cncidr.txt','applications.txt']

for f in files:
    path = os.path.join(base, f)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    lines = content.split('\n')
    rules = [l.strip() for l in lines if l.strip().startswith("  - '") or l.strip().startswith("- '")]
    
    samples = []
    has_domain_prefix = False
    has_ipcidr_prefix = False
    process_name = False
    
    for r in rules[:5]:
        rule = r.replace("  - '", "").replace("- '", "").replace("'", "")
        samples.append(rule)
        if rule.startswith('DOMAIN,') or rule.startswith('DOMAIN-SUFFIX,') or rule.startswith('DOMAIN-KEYWORD,'):
            has_domain_prefix = True
        if rule.startswith('IP-CIDR,') or rule.startswith('IP-CIDR6,'):
            has_ipcidr_prefix = True
        if rule.startswith('PROCESS-NAME,'):
            process_name = True
    
    format_type = '纯域名' if not has_domain_prefix and not has_ipcidr_prefix and not process_name else ''
    if has_domain_prefix:
        format_type = 'DOMAIN-前缀'
    if has_ipcidr_prefix:
        format_type = 'IP-CIDR-前缀' if 'IP-CIDR' in format_type else 'IP-CIDR-前缀'
    if process_name:
        format_type = 'PROCESS-NAME'
    if has_domain_prefix and has_ipcidr_prefix:
        format_type = '混合格式'
    
    print(f'{f:<20} {len(rules):>4}条 → {format_type}')
    print(f'  {" | ".join(samples)}')
    print()