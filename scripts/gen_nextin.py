import os, sys

rules_dir = r'E:\dev\clash-rules'
output_dir = r'E:\dev\clash-rules\nextin'
os.makedirs(output_dir, exist_ok=True)

# ── 1. Rule-providers YAML ──
yaml_lines = []
yaml_lines.append('# NexTIN (星拓) 规则集配置 - 基于 Clash Meta (Mihomo) 内核')
yaml_lines.append('# 适用于 iPhone / iPad / Mac / Apple TV')
yaml_lines.append('# 使用方式：NexTIN → 配置 → 导入配置文件 → 选择此文件')
yaml_lines.append('')

# domain rules
yaml_lines.append('rule-providers:')
for fn, name in [
    ('reject.txt', 'reject'), ('private.txt', 'private'), ('apple.txt', 'apple'),
    ('microsoft.txt', 'microsoft'), ('steam.txt', 'steam'), ('icloud.txt', 'icloud'),
    ('direct.txt', 'direct'), ('ai.txt', 'ai'), ('proxy.txt', 'proxy'),
    ('applications.txt', 'applications'),
]:
    fp = os.path.join(rules_dir, fn)
    if not os.path.exists(fp):
        continue
    yaml_lines.append(f'  {name}:')
    yaml_lines.append(f'    type: http')
    yaml_lines.append(f'    behavior: domain')
    yaml_lines.append(f'    url: "https://cdn.jsdelivr.net/gh/thintsing/proxy-rules@main/{fn}"')
    yaml_lines.append(f'    path: ./ruleset/{name}.yaml')
    yaml_lines.append(f'    interval: 86400')

# ipcidr rules
for fn, name, behavior in [
    ('lancidr.txt', 'lancidr', 'ipcidr'),
    ('telegramcidr.txt', 'telegramcidr', 'ipcidr'),
    ('cncidr.txt', 'cncidr', 'ipcidr'),
]:
    fp = os.path.join(rules_dir, fn)
    if not os.path.exists(fp):
        continue
    yaml_lines.append(f'  {name}:')
    yaml_lines.append(f'    type: http')
    yaml_lines.append(f'    behavior: {behavior}')
    yaml_lines.append(f'    url: "https://cdn.jsdelivr.net/gh/thintsing/proxy-rules@main/{fn}"')
    yaml_lines.append(f'    path: ./ruleset/{name}.yaml')
    yaml_lines.append(f'    interval: 86400')

yaml_lines.append('')
yaml_lines.append('# 分流规则（优先级从高到低）')
yaml_lines.append('rules:')
yaml_lines.append('  - RULE-SET,applications,DIRECT')
yaml_lines.append('  - RULE-SET,private,DIRECT')
yaml_lines.append('  - RULE-SET,reject,REJECT')
yaml_lines.append('  - RULE-SET,ai,Proxy')
yaml_lines.append('  - RULE-SET,steam,DIRECT')
yaml_lines.append('  - RULE-SET,icloud,DIRECT')
yaml_lines.append('  - RULE-SET,apple,DIRECT')
yaml_lines.append('  - RULE-SET,proxy,Proxy')
yaml_lines.append('  - RULE-SET,direct,DIRECT')
yaml_lines.append('  - RULE-SET,microsoft,DIRECT')
yaml_lines.append('  - RULE-SET,lancidr,DIRECT')
yaml_lines.append('  - RULE-SET,cncidr,DIRECT')
yaml_lines.append('  - RULE-SET,telegramcidr,Proxy')
yaml_lines.append('  - GEOIP,CN,DIRECT,no-resolve')
yaml_lines.append('  - MATCH,Proxy')

yaml_path = os.path.join(output_dir, 'nextin_rules.yaml')
with open(yaml_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(yaml_lines) + '\n')
print(f'Generated: nextin_rules.yaml ({len(yaml_lines)} lines)')


# ── 2. Combined plain-text rule file ──
# NexTIN supports importing rules in "domain,policy" format
sr_lines = [
    '# NexTIN (星拓) 规则集 - Generated from thintsing/proxy-rules',
    '# 导入方式：NexTIN → 配置 → 导入配置 → 从 URL 下载',
    '# URL: https://raw.githubusercontent.com/thintsing/proxy-rules/main/nextin/nextin_rules.conf',
    '',
]

# Build in order: REJECT -> DIRECT -> Proxy -> IP-CIDR -> Final
sections = [
    ('# Reject (ads + malware)', 'reject.txt', 'REJECT'),
    ('# Private / LAN', 'private.txt', 'DIRECT'),
    ('# Apple', 'apple.txt', 'DIRECT'),
    ('# Microsoft', 'microsoft.txt', 'DIRECT'),
    ('# Steam', 'steam.txt', 'DIRECT'),
    ('# iCloud', 'icloud.txt', 'DIRECT'),
    ('# Direct (Chinese CDN + misc)', 'direct.txt', 'DIRECT'),
    ('# AI', 'ai.txt', 'Proxy'),
    ('# Proxy (foreign sites)', 'proxy.txt', 'Proxy'),
]

for header, fn, policy in sections:
    sr_lines.append(header)
    fp = os.path.join(rules_dir, fn)
    if not os.path.exists(fp):
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if s and not s.startswith('#'):
                sr_lines.append(f'{s},{policy}')

sr_lines.extend([
    '',
    '# IP-CIDR',
    '# LAN',
    'IP-CIDR,10.0.0.0/8,DIRECT',
    'IP-CIDR,172.16.0.0/12,DIRECT',
    'IP-CIDR,192.168.0.0/16,DIRECT',
    'IP-CIDR,100.64.0.0/10,DIRECT',
    '# Telegram',
    'IP-CIDR,91.108.4.0/22,Proxy',
    'IP-CIDR,91.108.56.0/22,Proxy',
    'IP-CIDR,149.154.160.0/20,Proxy',
    '',
    '# Final fallback',
    'GEOIP,CN,DIRECT',
    'FINAL,Proxy',
])

combined_path = os.path.join(output_dir, 'nextin_rules.conf')
with open(combined_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(sr_lines) + '\n')
print(f'Generated: nextin_rules.conf ({len(sr_lines)} lines)')

print()
print('Done!')