#!/usr/bin/env python3
"""检查 tailscale 连接"""
import sys, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('E:/DEV/clash-rules/conn3.json', 'r', encoding='utf-8') as f:
    raw = f.read().strip()
raw = re.sub(r'^[0-9a-fA-F]+\r?\n', '', raw)
raw = raw.rstrip('0').strip().lstrip('\ufeff')
obj = json.loads(raw)
conns = obj.get('connections', [])
print(f'活跃连接数: {len(conns)}')
print()
# 查找所有包含 tailscale 或 100.x 尾缀的
for c in conns:
    meta = c.get('metadata', {})
    host = meta.get('host', '')
    dst = meta.get('destinationIP', '') or meta.get('destinationIP', '')
    port = meta.get('destinationPort', '')
    network = meta.get('network', '')
    type_ = meta.get('type', '')
    rule = c.get('rule', '')
    rule_payload = c.get('rulePayload', '')
    chain = c.get('chains', [])
    
    # 检查 tailscale 相关
    is_tailscale = False
    if 'tailscale' in host.lower():
        is_tailscale = True
    if '100.' in host or '100.' in dst:
        is_tailscale = True
    if host and 'tailscale' in host.lower():
        is_tailscale = True
    
    # 只看非 AI 的代理连接
    if not is_tailscale:
        # 检查是否走代理
        if 'Hysteria' in str(chain) and 'AI' not in str(chain) and 'google' not in host.lower() and 'chatgpt' not in host.lower() and 'openai' not in host.lower():
            if host or dst:
                print(f'[PROXY] host={host:<40} ip={dst:<20} port={port:<5} {network}/{type_}  rule={rule:<15} -> {chain}')
    
    if is_tailscale:
        print(f'[TAILSCALE] host={host:<40} ip={dst:<20} port={port:<5} {network}/{type_}  rule={rule:<15} chain={chain}')