# Clash Rules Collection

个人整理的 Clash 分流规则集，基于日常使用优化。

## 📁 文件说明

| 文件 | 说明 | 用途 |
|------|------|------|
| `direct.txt` | 直连域名列表 | 国内网站、CDN等 |
| `proxy.txt` | 代理域名列表 | 国外网站、需要翻墙的服务 |
| `reject.txt` | 拦截域名列表 | 广告、追踪、恶意网站 |
| `apple.txt` | 苹果服务域名 | Apple 相关服务 |
| `microsoft.txt` | 微软服务域名 | Microsoft 相关服务 |
| `steam.txt` | Steam 游戏平台 | Steam 商店、社区、下载 |
| `ai.txt` | AI 服务域名 | OpenAI、Claude、Gemini 等 |

## 🚀 使用方法

### 在 Clash Verge 中引用

```yaml
rule-providers:
  direct:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/你的用户名/clash-rules@main/direct.txt"
    path: ./ruleset/direct.yaml
    interval: 86400
  
  proxy:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/你的用户名/clash-rules@main/proxy.txt"
    path: ./ruleset/proxy.yaml
    interval: 86400
    
  reject:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/你的用户名/clash-rules@main/reject.txt"
    path: ./ruleset/reject.yaml
    interval: 86400

rules:
  - RULE-SET,reject,🛑 全球拦截
  - RULE-SET,proxy,🚀 节点选择
  - RULE-SET,direct,🎯 全球直连
  - MATCH,🐟 漏网之鱼
```

## 📊 规则统计

- 直连规则：约 150+ 条
- 代理规则：约 100+ 条
- 拦截规则：约 50+ 条
- Steam规则：约 46 条
- AI服务：约 15 条

## 📝 更新日志

### 2026-06-17
- 初始版本发布
- 添加 Steam 完整规则
- 优化微软服务分流
- 添加 Google 国内 CDN 直连

## 🙏 致谢

- 参考 [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules)
- 参考 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)

## 📄 License

MIT License
