# Clash Rules Collection

个人整理的 Clash 分流规则集，基于日常使用优化。

**仓库地址**: https://github.com/thintsing/clash-rules

## 📁 文件说明

| 文件 | 说明 | 用途 |
|------|------|------|
| `direct.txt` | 直连域名列表 | 国内网站、CDN等 |
| `proxy.txt` | 代理域名列表 | 国外网站、需要翻墙的服务 |
| `reject.txt` | 拦截域名列表 | 广告、追踪、恶意网站 |
| `apple.txt` | 苹果服务域名 | Apple 相关服务 |
| `steam.txt` | Steam 游戏平台 | Steam 商店、社区、下载 |
| `ai.txt` | AI 服务域名 | OpenAI、Claude、Gemini 等 |

## 🚀 使用方法

### 在 Clash Verge 中引用

```yaml
rule-providers:
  reject:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/reject.txt"
    path: ./ruleset/reject.yaml
    interval: 86400

  proxy:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/proxy.txt"
    path: ./ruleset/proxy.yaml
    interval: 86400

  direct:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/direct.txt"
    path: ./ruleset/direct.yaml
    interval: 86400

  apple:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/apple.txt"
    path: ./ruleset/apple.yaml
    interval: 86400

  steam:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/steam.txt"
    path: ./ruleset/steam.yaml
    interval: 86400

  ai:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/ai.txt"
    path: ./ruleset/ai.yaml
    interval: 86400

rules:
  - RULE-SET,reject,🛑 全球拦截
  - RULE-SET,ai,🤖 AI服务
  - RULE-SET,steam,🎮 Steam
  - RULE-SET,apple,🍎 苹果服务
  - RULE-SET,proxy,🚀 节点选择
  - RULE-SET,direct,🎯 全球直连
  - MATCH,🐟 漏网之鱼
```

### 代理组配置示例

```yaml
proxy-groups:
  - name: 🚀 节点选择
    type: select
    proxies:
      - ♻️ 自动选择
      - DIRECT

  - name: ♻️ 自动选择
    type: url-test
    url: http://www.gstatic.com/generate_204
    interval: 300
    tolerance: 50
    proxies:
      - 你的节点1
      - 你的节点2

  - name: 🤖 AI服务
    type: select
    proxies:
      - 🚀 节点选择
      - ♻️ 自动选择
      - DIRECT

  - name: 🎮 Steam
    type: select
    proxies:
      - 🚀 节点选择
      - ♻️ 自动选择
      - DIRECT

  - name: 🍎 苹果服务
    type: select
    proxies:
      - DIRECT
      - 🚀 节点选择

  - name: 🎯 全球直连
    type: select
    proxies:
      - DIRECT
      - 🚀 节点选择

  - name: 🛑 全球拦截
    type: select
    proxies:
      - REJECT
      - DIRECT

  - name: 🐟 漏网之鱼
    type: select
    proxies:
      - 🚀 节点选择
      - DIRECT
```

## 📊 规则统计

| 规则集 | 规则数量 | 说明 |
|--------|---------|------|
| `reject.txt` | 50+ | 广告、追踪、恶意网站 |
| `proxy.txt` | 200+ | 国外网站、需要代理的服务 |
| `direct.txt` | 150+ | 国内网站、CDN等 |
| `apple.txt` | 150+ | Apple 相关服务 |
| `steam.txt` | 46 | Steam 游戏平台 |
| `ai.txt` | 30+ | AI 服务（OpenAI、Claude等） |

## 🔗 规则集链接

可以直接复制以下链接使用：

- **Reject**: `https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/reject.txt`
- **Proxy**: `https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/proxy.txt`
- **Direct**: `https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/direct.txt`
- **Apple**: `https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/apple.txt`
- **Steam**: `https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/steam.txt`
- **AI**: `https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/ai.txt`

## 📝 更新日志

### 2026-06-17
- 初始版本发布
- 添加 Steam 完整规则（46条）
- 优化微软服务分流
- 添加 Google 国内 CDN 直连
- 添加 AI 服务规则（OpenAI、Claude、Gemini等）
- 添加 Apple 服务规则

## 🙏 致谢

- 参考 [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules)
- 参考 [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)

## 📄 License

MIT License
