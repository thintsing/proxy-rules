#!/usr/bin/env python3
"""将 behavior:domain 规则文件转换为纯域名格式（对齐 Loyalsoldier 规范）
- DOMAIN,x / DOMAIN-SUFFIX,x → x （mihomo 对纯域名按 DOMAIN-SUFFIX 匹配）
- DOMAIN-KEYWORD,x → 保留 DOMAIN-KEYWORD,x （关键字匹配无法用纯域名表达）
"""
import os

BASE = 'E:/DEV/clash-rules/'

# behavior: domain 的文件
FILES = [
    'reject.txt', 'proxy.txt', 'direct.txt', 'apple.txt',
    'steam.txt', 'ai.txt', 'icloud.txt', 'private.txt', 'microsoft.txt',
]

def convert(path):
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    lines = raw.split('\n')

    out = []
    rules_count = 0
    for line in lines:
        stripped = line.strip()
        # 只处理 payload 条目
        if stripped.startswith("  - '") or stripped.startswith("- '"):
            # 提取规则内容
            rule = stripped
            for prefix in ("  - '", "- '"):
                if rule.startswith(prefix):
                    rule = rule[len(prefix):]
                    break
            if rule.endswith("'"):
                rule = rule[:-1]
            # 展开转义
            rule = rule.replace("''", "'")
            
            # 转换前缀
            if rule.startswith('DOMAIN-SUFFIX,'):
                rule = rule[len('DOMAIN-SUFFIX,'):]
            elif rule.startswith('DOMAIN,'):
                rule = rule[len('DOMAIN,'):]
            # DOMAIN-KEYWORD 保留原样
            # 其他（纯域名）保持不变
            
            # 重新转义并包装
            escaped = rule.replace("'", "''")
            out.append("  - '{}'".format(escaped))
            rules_count += 1
        else:
            out.append(line)

    content = '\n'.join(out).rstrip('\n') + '\n'
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    return rules_count

for f in FILES:
    path = os.path.join(BASE, f)
    n = convert(path)
    print(f'OK {f} -> {n} rules')

print('\nDone.')