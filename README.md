<div align="center">

# Clash Rules Collection

**个人整理的 Clash 分流规则集 · 开箱即用 · 自动更新**

[![GitHub release](https://img.shields.io/github/v/release/thintsing/clash-rules?style=flat-square&color=blue)](https://github.com/thintsing/clash-rules/releases)
[![GitHub stars](https://img.shields.io/github/stars/thintsing/clash-rules?style=flat-square&color=yellow)](https://github.com/thintsing/clash-rules/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/thintsing/clash-rules?style=flat-square&color=success)](https://github.com/thintsing/clash-rules/commits/main)
[![License](https://img.shields.io/github/license/thintsing/clash-rules?style=flat-square)](LICENSE)
[![Total Rules](https://img.shields.io/badge/Total%20Rules-1157%2B-brightgreen?style=flat-square)](#-规则统计)
[![CDN](https://img.shields.io/badge/CDN-jsDelivr-orange?style=flat-square)](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/reject.txt)

<br>

**仓库地址**: [https://github.com/thintsing/clash-rules](https://github.com/thintsing/clash-rules)

</div>

---

## 规则集概览

| 规则集 | 规则数 | 用途 | CDN 链接 |
|:------:|:-----:|:----:|:--------:|
| reject | **220** | 广告追踪、恶意网站拦截 | [reject.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/reject.txt) |
| proxy | **357** | 国外网站、需要代理的服务 | [proxy.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/proxy.txt) |
| direct | **211** | 国内网站、CDN 加速节点 | [direct.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/direct.txt) |
| apple | **148** | Apple 全系服务 | [apple.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/apple.txt) |
| steam | **45** | Steam 游戏平台 | [steam.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/steam.txt) |
| ai | **50** | AI 服务（OpenAI/Claude等） | [ai.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/ai.txt) |
| icloud | **20** | iCloud 认证/Private Relay/CloudKit | [icloud.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/icloud.txt) |
| private | **26** | 私有网络域名（路由器/内网） | [private.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/private.txt) |
| telegramcidr | **16** | Telegram IP 段 | [telegramcidr.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/telegramcidr.txt) |
| lancidr | **13** | 局域网保留 IP 段 | [lancidr.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/lancidr.txt) |
| applications | **51** | 应用进程匹配（浏览器/游戏/办公） | [applications.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/applications.txt) |

**总计: 1157+ 条规则**，覆盖日常使用全场景。

---

## 特点

| 特点 | 说明 |
|:----|:------|
| **即用** | 直接引用 jsDelivr CDN 链接，无需手动维护 |
| **自动更新** | 搭配 rule-providers，规则每天自动同步 |
| **隐私安全** | 仅含域名/IP规则，不含任何节点信息 |
| **分类清晰** | 11个独立规则集，按优先级精准分流 |
| **持续维护** | 定期跟随主流规则源更新 |

---

## 快速开始

### 在 Clash Verge 中使用

**1. 添加 Merge 配置**

在 Clash Verge -> 配置 -> Merge 中添加以下内容：

```yaml
# 规则集提供者
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

  private:
    type: http
    behavior: domain
    url: "https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/private.txt"
    path: ./ruleset/private.yaml
    interval: 86400

  lancidr:
    type: http
    behavior: ipcidr
    url: "https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/lancidr.txt"
    path: ./ruleset/lancidr.yaml
    interval: 86400

  telegramcidr:
    type: http
    behavior: ipcidr
    url: "https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/telegramcidr.txt"
    path: ./ruleset/telegramcidr.yaml
    interval: 86400

  applications:
    type: http
    behavior: classical
    url: "https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/applications.txt"
    path: ./ruleset/applications.yaml
    interval: 86400

# 分流规则（优先级从高到低）
rules:
  - RULE-SET,applications,DIRECT
  - RULE-SET,private,DIRECT
  - RULE-SET,reject,REJECT
  - RULE-SET,ai,AI-SERVICE
  - RULE-SET,steam,STEAM
  - RULE-SET,apple,APPLE
  - RULE-SET,proxy,PROXY
  - RULE-SET,direct,DIRECT
  - RULE-SET,lancidr,DIRECT
  - RULE-SET,telegramcidr,PROXY
  - GEOIP,CN,DIRECT
  - MATCH,PROXY
```

> **注意**: 模板中的策略组名（DIRECT/PROXY/REJECT等）请替换为你配置中实际的代理组名称。

**2. 重新加载**

点击「重新加载」即可生效，规则集将自动下载。

---

## 规则详情

### reject - 广告追踪拦截

拦截 Google 广告、国内移动广告、社交追踪、数据采集等。

包含: DoubleClick, GoogleAds, Facebook-ads, Umeng, Mopub, AppLovin 等

### proxy - 国外网站代理

涵盖流媒体、社交、开发工具、学术科研、购物出行等。

| 类别 | 包含 |
|:----|:-----|
| 流媒体 | YouTube, Netflix, Spotify, Twitch, Disney+, HBO, Hulu, Abema |
| 社交 | Twitter/X, Facebook, Instagram, Reddit, Telegram, Discord |
| 开发 | GitHub, Docker, NPM, PyPI, Maven, Gradle, GitLab, JetBrains |
| 学术 | arXiv, IEEE, Nature, Springer, ScienceDirect, Google Scholar |
| AI | OpenAI, Claude, Gemini, Perplexity, Poe, Cursor, V0 |
| 购物 | Amazon, eBay, AliExpress, BestBuy, Walmart |
| 旅行 | Booking, Airbnb, Expedia, Agoda, Uber, Lyft |
| 金融 | PayPal, Wise, Revolut, Coinbase, Binance |

### direct - 国内网站直连

涵盖国内主流平台和服务。

| 类别 | 包含 |
|:----|:-----|
| 综合 | Baidu, Alibaba, Tencent, ByteDance, NetEase, Xiaomi |
| 音乐 | NetEase Music, QQ Music, Kugou, Kuwo |
| 视频 | Bilibili, iQiyi, Youku, Douyin, Douyu, Huya |
| 云服务 | Aliyun, Tencent Cloud, Qiniu, UPYun |
| 办公 | Feishu, DingTalk, WPS, Yuque |
| 金融 | Alipay, WeChat Pay, UnionPay, ABOC, ICBC |

---

## 安全说明

- 仅含域名/IP 规则，不包含任何代理节点信息
- 可放心分享、发布、用于 rule-providers
- 建议搭配 Merge 配置使用，节点信息保留在本地

---

## 更新日志

### v1.2 - 2026-06-17
- 新增 5 个规则集: private / telegramcidr / lancidr / applications / icloud
- 规则优先级重构为 7 层体系
- 内联 IP-CIDR 全部迁移到独立规则集
- 规则总数: 1030+ -> 1157+

### v1.1 - 2026-06-17
- 规则大幅扩充: 从 400+ 到 1030+ 条
- proxy.txt 扩充至 355 条（新增开发工具、学术、购物、旅行等）
- direct.txt 扩充至 214 条（新增国内视频、音乐、云服务等）
- reject.txt 扩充至 219 条（新增更多广告网络、追踪服务）
- 美化管理: 添加 badges、Mermaid 统计图、分栏说明
- DNS 优化: Clash 最佳 DNS 实践（respect-rules / prefer-h3）

### v1.0 - 2026-06-17
- 初始版本发布
- 包含 Steam 完整规则（44 条）
- 微软/Google 国内 CDN 分流优化
- Apple 服务规则（148 条）
- AI 服务规则（50 条）

---

## 致谢

- [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules)
- [blackmatrix7/ios_rule_script](https://github.com/blackmatrix7/ios_rule_script)

---

<div align="center">

如果觉得有用，欢迎 Star 支持！

</div>

## License

MIT License 2026 thintsing