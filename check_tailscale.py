#!/usr/bin/env python3
"""检查 tailscale 连接"""
import json, re, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('E:/DEV/clash-rules/conn2.json', 'r', encoding='utf-8') as f:
    raw = f.read().strip()
raw = re.sub(r'^[0-9a-fA-F]+\r?\n', '', raw)
raw = raw.rstrip('0').strip()
raw = raw.lstrip('\ufeff')
obj = json.loads(raw)
conns = obj.get('connections', [])
print(f'活跃连接数: {len(conns)}')
print()
for c in conns:
    meta = c.get('metadata', {})
    host = meta.get('host', '')
    host = host or meta.get('destinationIP', '')
    rule = c.get('rule', 'N/A')
    rule_payload = c.get('rulePayload', '')
    chain = c.get('chains', [])
    # 只显示 tailscale 相关 + 部分代理走通的
    if 'tailscale' in host.lower() or 'ts' in host.lower() or 'tailscale' in str(chain).lower():
        print(f'[TAILSCALE] host={host}  rule={rule}  rulePayload={rule_payload}  chain={chain}')
    # 也显示所有走代理的连接
    elif 'AI' in str(chain) or '国外' in str(chain) or 'Hysteria' in str(chain):
        if 'google' in host.lower() or 'chatgpt' in host.lower() or 'openai' in host.lower():
            pass  # 跳过已知的 AI 连接
        elif 'CHAT' in str(chain).upper():
            pass
        else:
            print(f'[PROXY] host={host}  rule={rule}  rulePayload={rule_payload}  chain={chain}')