#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将 Clash 规则集 .txt 文件转换为 YAML 格式（带 payload: 字段）
mihomo 的 type:http rule-provider 要求 YAML 格式才有 payload 字段
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))

# 需要转换的文件（applications.txt 已含 payload:，跳过）
FILES = [
    "reject.txt", "proxy.txt", "direct.txt", "apple.txt",
    "steam.txt", "ai.txt", "icloud.txt", "private.txt",
    "microsoft.txt", "lancidr.txt", "telegramcidr.txt", "cncidr.txt",
]

def convert(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        raw = f.read()
    lines = raw.splitlines()

    header = []      # 文件头注释
    payload = []     # 规则条目
    in_header = True

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_header:
                header.append("")
            continue
        if stripped.startswith("#"):
            header.append(line)
            continue
        # 规则数据
        in_header = False
        # 转义单引号
        escaped = stripped.replace("'", "''")
        payload.append("  - '{}'".format(escaped))

    # 组装 YAML
    out_lines = []
    # 去掉头部末尾多余空行
    while header and header[-1] == "":
        header.pop()
    out_lines.extend(header)
    if out_lines and out_lines[-1] != "":
        out_lines.append("")
    out_lines.append("payload:")
    out_lines.extend(payload)

    content = "\n".join(out_lines) + "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

    return len(payload)

for f in FILES:
    p = os.path.join(BASE, f)
    if not os.path.exists(p):
        print("SKIP {} not found".format(f))
        continue
    n = convert(p)
    print("OK {} -> {} rules".format(f, n))

print("\nDone.")