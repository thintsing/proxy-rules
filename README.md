<div align="center">

# Clash Rules Collection

**个人整理的 Clash 分流规则集 · 开箱即用 · 自动更新**

[![GitHub release](https://img.shields.io/github/v/release/thintsing/clash-rules?style=flat-square&color=blue)](https://github.com/thintsing/clash-rules/releases)
[![Auto Update](https://img.shields.io/github/actions/workflow/status/thintsing/clash-rules/update-rules.yml?style=flat-square&label=auto-update&logo=githubactions)](https://github.com/thintsing/clash-rules/actions/workflows/update-rules.yml)
[![GitHub last commit](https://img.shields.io/github/last-commit/thintsing/clash-rules?style=flat-square&color=success)](https://github.com/thintsing/clash-rules/commits/main)
[![Total Rules](https://img.shields.io/badge/Total%20Rules-2829%2B-brightgreen?style=flat-square)](#-规则统计)
[![CDN](https://img.shields.io/badge/CDN-jsDelivr-orange?style=flat-square)](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/reject.txt)

</div>

---

## 目录

- [规则集概览](#规则集概览)
- [快速上手](#快速上手)
- [规则优先级](#规则优先级)
- [自动更新](#自动更新)
- [文件说明](#文件说明)
- [许可](#许可)

---

## 规则集概览

| 规则集 | 数量 | 用途 | CDN 链接 |
|:------:|:----:|:----|:--------:|
| reject | 220 | 广告跟踪、恶意网站拦截 | [reject.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/reject.txt) |
| proxy | 356 | 国外网站、需要代理的服务 | [proxy.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/proxy.txt) |
| direct | 205 | 国内网站、CDN 加速节点 | [direct.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/direct.txt) |
| apple | 1729 | Apple 全系服务 | [apple.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/apple.txt) |
| steam | 54 | Steam 游戏平台 | [steam.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/steam.txt) |
| ai | 78 | AI 服务（OpenAI / Claude 等） | [ai.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/ai.txt) |
| icloud | 81 | iCloud 认证 / Private Relay / CloudKit | [icloud.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/icloud.txt) |
| private | 26 | 私有网络域名（路由器 / 内网） | [private.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/private.txt) |
| telegramcidr | 16 | Telegram IP 段 | [telegramcidr.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/telegramcidr.txt) |
| lancidr | 13 | 局域网保留 IP 段 | [lancidr.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/lancidr.txt) |
| applications | 51 | 应用进程匹配（浏览器 / 游戏 / 办公） | [applications.txt](https://cdn.jsdelivr.net/gh/thintsing/clash-rules@main/applications.txt) |

**总计: 2829+ 条规则**

---

## 快速上手

本规则集推荐通过 **Clash Verge 的 Merge（增强配置）** 功能使用，即配即用，无需手动编辑配置文件。

### 方法一：使用 Merge 文件（推荐）

> 适合已经配置好**代理节点**和**代理组**的用户。

**第一步：在 Clash Verge 中添加 Merge**

1. 打开 Clash Verge Rev → 设置 / 增强配置
2. 点击「新建」→ 选择「Merge」
3. 将 [`clash-verge-merge.yaml`](clash-verge-merge.yaml) 的全部内容复制进去
4. 点击「保存」
5. 点击「重新加载配置」生效

> 如果你看不到「增强配置」入口，可以在设置中开启「高级功能」或「开发者模式」。

**第二步：确保代理组名称匹配**

规则集会根据代理组名称进行分流，请确保你的 Clash 配置中包含以下代理组（名称必须完全一致）：

```
🚀 节点选择    ← 手动选择节点
♻️ 自动选择    ← 自动测速选优
🌍 国外媒体    ← 流媒体专用
📲 电报信息    ← Telegram 专用
🤖 AI服务      ← AI 网站专用
🎮 Steam       ← Steam 游戏
🍎 苹果服务    ← Apple 服务（可直连加速下载）
🎯 全球直连    ← 国内直连
🛑 全球拦截    ← 广告拦截
🐟 漏网之鱼    ← 兜底规则
Ⓜ️ 微软服务    ← Microsoft 服务
```

如果你用**不同的组名**，只需修改 `clash-verge-merge.yaml` 中 `RULE-SET` 后面的组名即可。

> 不知道怎么写代理组？参考 [`example-config.yaml`](example-config.yaml) 的完整配置示例。

---

### 方法二：手动编辑配置文件

> 适合使用其他 Clash 客户端（Clash for Windows / OpenClash 等）的用户。

在配置文件的 `rule-providers` 和 `rules` 中添加如下内容：

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

  # ... 其他规则集类似，详见 clash-verge-merge.yaml

# 分流规则（按优先级从高到低）
rules:
  - RULE-SET,applications,DIRECT
  - RULE-SET,private,🎯 全球直连
  - RULE-SET,reject,🛑 全球拦截
  - RULE-SET,ai,🤖 AI服务
  - RULE-SET,steam,🎮 Steam
  - RULE-SET,icloud,🚀 节点选择
  - RULE-SET,apple,🍎 苹果服务
  - RULE-SET,proxy,🚀 节点选择
  - RULE-SET,direct,🎯 全球直连
  - RULE-SET,lancidr,🎯 全球直连
  - RULE-SET,telegramcidr,📲 电报信息
  - GEOIP,CN,🎯 全球直连,no-resolve
  - MATCH,🐟 漏网之鱼
```

> 初次加载时 Clash 会自动从 CDN 下载规则文件，请确保网络通畅。

---

### 方法三：直接引用 URL

如果不想用 `rule-providers`，也可以直接把规则文件的 CDN 链接替换到你的规则中。不过推荐用方法一或二，可以实现**自动更新**。

---

## 规则优先级

规则按以下 **7 层优先级** 匹配，从高到低：

```
第 1 层  applications  →  进程匹配（最高优先，不走代理的应用直接放行）
第 2 层  private       →  内网域名（路由器面板、群晖、NAS 等）
第 3 层  reject        →  广告跟踪、恶意网站（直接拦截）
第 4 层  ai/steam/icloud/apple → 特定服务分流
第 5 层  proxy/direct  →  通用代理 / 国内直连
第 6 层  lancidr/telegramcidr → IP 段匹配
第 7 层  GEOIP,CN / MATCH → GeoIP 兜底
```

> 每条请求从上到下逐条匹配，匹配到即停止，不会继续向下检查。

---

## 自动更新

本仓库使用 GitHub Actions **每天 UTC 22:00（北京时间 06:00）** 自动从 blackmatrix7 同步 Apple / Steam / AI / iCloud 规则：

| 文件 | 来源 | 策略 |
|:----|:-----|:-----|
| apple.txt | blackmatrix7 | 合并补充（保留自定义规则） |
| steam.txt | blackmatrix7 | 合并补充 |
| ai.txt | blackmatrix7 | 合并补充 |
| icloud.txt | blackmatrix7 | 合并补充 |
| reject / proxy / direct | **手动维护** | 上游规则过于庞大，不自动合并 |
| private / lancidr / telegramcidr / applications | **自定义规则** | 无上游来源 |

> 手动触发：进入 GitHub 仓库 → Actions → Auto-Update Rules → Run workflow

利用 Clash 的 `rule-providers` 机制，**规则文件更新后，Clash 客户端在下次启动或下一次请求时会自动拉取最新版本**，无需手动操作。

---

## 文件说明

| 文件 | 说明 |
|:----|:------|
| `*.txt` | 规则数据文件（共 11 个），通过 rule-providers 远程引用 |
| `clash-verge-merge.yaml` | Clash Verge 增强配置（Merge），引用全部规则集 + 七层分流规则 |
| `example-config.yaml` | 完整 Clash 配置示例，含节点 / 代理组 / DNS |
| `.github/workflows/update-rules.yml` | GitHub Actions 自动构建配置 |
| `scripts/merge_rules.py` | 自动合并上游规则的 Python 脚本 |

---

## 许可

[MIT License](LICENSE)