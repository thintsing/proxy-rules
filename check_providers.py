#!/usr/bin/env python3
"""检查 mihomo rule-provider 加载状态"""
import json
import win32pipe
import win32file

pipe = win32pipe.CreateFile(
    r'\\.\pipe\verge-mihomo',
    win32pipe.GENERIC_READ | win32pipe.GENERIC_WRITE,
    0, None, win32pipe.OPEN_EXISTING, 0, None
)
req = 'GET /providers/rules HTTP/1.1\r\nHost: localhost\r\nAuthorization: Bearer set-your-secret\r\nConnection: close\r\n\r\n'
win32file.WriteFile(pipe, req.encode())
result, data = win32file.ReadFile(pipe, 65536)
win32file.CloseHandle(pipe)
resp = data.decode('utf-8', errors='replace')

if '\r\n\r\n' in resp:
    body = resp.split('\r\n\r\n', 1)[1]
    body = body.rstrip('0').strip()
    obj = json.loads(body)
    print('=== Rule-Provider 加载状态 ===')
    for name, info in sorted(obj.get('providers', {}).items()):
        icon = '✅' if info['ruleCount'] > 0 else '❌'
        print(f'{icon} {name:<15} behavior={info["behavior"]:<8} rules={info["ruleCount"]}')
else:
    print('响应中没有 HTTP 体')
    print(resp[:500])