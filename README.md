# proxy-rules

Clash 规则配置，基于 [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules) 官方规则 + GEOSITE 内置数据库，面向 **Clash Verge Rev**（mihomo 内核）的增强槽（merge / groups）使用方式。

## 架构

规则自上而下匹配，命中即止，共 **40 条**：

| 层 | 规则 | 说明 |
|---|---|---|
| 0 | 强制直连 ×22 | `bing.com` / `bing.net` + 微软账号链路 20 条，全部写死 `DIRECT` |
| 1 | 自定义覆盖 ×3 | `custom-ai` → 🤖 AI服务；`custom-steam` → 🎮 Steam；`custom-direct` → 🎯 全球直连 |
| 2 | Loyalsoldier 核心 ×4 | `applications` / `reject` / `proxy` / `direct` |
| 3 | LAN 私有网段 ×1 | `lancidr`（**带 `no-resolve`**，见下方设计要点） |
| 4 | GEOSITE ×8 | 内置数据库，零网络开销 |
| 5 | `GEOIP,CN` ×1 | 国内 IP 直连（`no-resolve`） |
| 6 | `MATCH` | 最终兜底 → 🐟 漏网之鱼 |

设计要点：

- **第 0 层用 `DIRECT` 关键字而非代理组名**。`bing.com` 如果只靠 `GEOSITE,microsoft` 命中 `Ⓜ️ 微软服务`，那是个 `select` 组——在面板里切换过就会跟着变。写死 `DIRECT` 才能恒定直连。
- **第 1 层排在 GEOSITE 之前**，保证自定义覆盖优先级最高。
- **GEOSITE 段零网络开销**，分类数据来自内核自带的 `geosite.dat`，不产生额外请求。
- **IP 类规则一律带 `no-resolve`**（`GEOIP,CN`、`RULE-SET,lancidr`，以及你自己的第 0 层 `IP-CIDR`）。不带的话 mihomo 会为**每条域名连接**先做一次本地解析 —— 用国内 `nameserver` 时，等于把走代理的域名也暴露给阿里/腾讯。详见「常见问题」最后两行。

> **`bing.net` 为什么要单独列**：它被 Loyalsoldier 的 `proxy.txt` 收进了代理名单，于是 `*.bing.net` 会绕道境外节点。而 `bing.net` 的真实服务（如 Windows Defender 遥测 `ts1.tc.mm.bing.net`）在国内本就有就近节点，走代理反而更慢甚至失败。

> **微软账号链路（20 条）为什么要单独列**：Loyalsoldier 的 `proxy.txt` 显式收录了 `+.live.com` / `+.microsoft.com` / `+.bingapis.com` / `+.hotmail.com` / `+.msedge.net` 等，而 `RULE-SET,proxy` 排在 `GEOSITE,microsoft` **之前** → `Ⓜ️ 微软服务` 这个组被彻底架空，**改成「全球直连」或任何节点都不会被命中**。想强直连只能加在第 0 层。加完后登录（OAuth）与 Bing 搜索会走同一出口 IP，避免 IP 分裂被风控。

## 文件说明

| 文件 | 用途 |
|------|------|
| `clash-verge-merge.yaml` | **Clash Verge Rev merge 模板**：8 个 rule-provider + 40 条规则 + DNS 策略（含 `fallback` 修复） |
| `clash-verge-groups.yaml` | **Clash Verge Rev groups 模板**：补齐 merge 规则引用、但机场订阅通常没有的 2 个代理组 |
| `custom-ai.txt` | AI 服务域名覆盖（Clash 用 `behavior: classical`） |
| `custom-steam.txt` | Steam / Blizzard 游戏覆盖 |
| `custom-direct.txt` | 直连覆盖（Tailscale / msftncsi / VNC / 国内游戏） |
| `example-config.yaml` | 从零手写 Clash 配置时的完整示例（含节点、代理组、规则） |
| `shadowrocket/shadowrocket_full.conf` | Shadowrocket 完整配置 |
| `loyalsoldier/*.txt` | Loyalsoldier 各分类规则快照，14 个（**归档用**，模板并不引用，见下方说明） |

> **关于 `loyalsoldier/` 目录**：模板里 provider 的 `url` 直接指向 Loyalsoldier 的官方 release 地址，**不**引用本目录。本目录只是快照归档，不参与运行，也不影响自动更新。仓库内没有任何文件引用这些本地路径。
>
> 用途是「离线兜底 / 版本对照」：想查某个域名当前是否被拦截，或想把 provider 改成本地 `type: file` 时，可以直接拿这里的文件用。
>
> | 项 | 值 |
> |---|---|
> | 快照来源 | `Loyalsoldier/clash-rules` 的 `release` 分支 |
> | 上游 commit | `4aeabf1f571334a89c2e6a1f5d608d323d24ae4c` |
> | 刷新时间 | 2026-09-18（上游提交于 2026-09-18T00:41:19Z） |
>
> 覆盖 14 个分类：`apple` / `applications` / `cncidr` / `direct` / `gfw` / `google` / `greatfire` / `icloud` / `lancidr` / `private` / `proxy` / `reject` / `telegramcidr` / `tld-not-cn`。

## 依赖

- **[Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules)**（5 个文件，由模板远程加载）
  - `proxy.txt` — 国外代理
  - `direct.txt` — 国内直连
  - `reject.txt` — 广告拦截
  - `applications.txt` — 进程规则
  - `lancidr.txt` — 局域网 IP 段
- **mihomo 内置数据库**
  - `geosite.dat` — GEOSITE 分类
  - `geoip.dat` — GEOIP 国家

## Clash Verge Rev 使用

Clash Verge Rev 的「增强」功能有三个独立槽位，本仓库用其中两个：

### 1. 配置 merge 模板

订阅 → 右键 → **编辑增强** → `merge` 槽位，填入：

```
https://raw.githubusercontent.com/thintsing/proxy-rules/main/clash-verge-merge.yaml
```

### 2. 配置 groups 模板

同一个「编辑增强」界面 → `groups` 槽位，填入：

```
https://raw.githubusercontent.com/thintsing/proxy-rules/main/clash-verge-groups.yaml
```

**为什么需要这一步**：merge 模板的规则里引用了 `🤖 AI服务` 和 `🎮 Steam` 两个代理组，但大多数机场订阅里没有这两个组名。如果组不存在，这两条 `RULE-SET` 规则目标落空，Clash 会**启动失败**。groups 模板用 `append` 把这两个组补进去，**不需要改动会自动更新的订阅文件本身**（改订阅的话下次更新就被覆盖了）。

### 3. 重启生效

改完增强槽位后必须**重启 Clash**（托盘右键「重启 Clash」，或完全退出 `clash-verge.exe` 再打开）。

> ⚠️ 只重启 `clash-verge-service` 服务**不会**重新生成配置——配置是由 GUI 进程 `clash-verge.exe` 在启动时合并生成的。

## 重要：务必按自己的环境调整这两处

模板无法替你猜环境，以下两处**导入前请检查**：

### ① `proxy` 字段 —— 决定规则集能否下载成功

```yaml
reject:
  type: http
  url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/reject.txt"
  interval: 86400
  proxy: "♻️ 自动选择"      # ← 这里换成你订阅里实际存在的代理组名
```

**为什么必须加**：mihomo 拉取 rule-provider 时，是**内核自身发起出站连接**，会绕过它自己的 TUN 和规则引擎（防环考虑）——等价于「真·直连」。所以在无法直连 `raw.githubusercontent.com` 的网络（比如国内直连环境）下，不加该字段会报：

```
[Provider] ... pull error: dns resolve failed: couldn't find ip
[Provider] ... pull error: TLS handshake timeout
```

**如果你的网络本就能直连 GitHub，删掉这 8 行 `proxy:` 即可。**

### ② 模板里的组名 —— 必须与你的订阅一致

两个模板都用到了这些组名，请对照自己订阅里实际存在的组名修改：

| 组名 | 出现在 | 说明 |
|------|--------|------|
| `♻️ 自动选择` | merge 的 8 个 `proxy:` + groups 的 `proxies` | url-test 自动测速组 |
| `🚀 节点选择` | groups 的 `proxies` | 主选择组 |
| `🎯 全球直连` / `🌍 国外媒体` / `🛑 全球拦截` / `🐟 漏网之鱼` | merge 的 `rules` 目标 | ACL4SSR 常见命名 |
| `🍎 苹果服务` / `Ⓜ️ 微软服务` / `📲 电报信息` | merge 的 `rules` 目标 | — |

> 这些是 ACL4SSR 体系下的常见组名，多数机场订阅都遵循这套命名。**如果规则目标指向了不存在的组，Clash 会直接启动失败**，日志里能看到 `proxy group [xxx] not found`。

### ③ DNS 策略（可选，遇到再开）

模板末尾有一个 `dns:` 块，包含两部分：

```yaml
dns:
  fallback:
    - https://223.5.5.5/dns-query
    - https://doh.pub/dns-query
  nameserver-policy:
    "bing.com":
      - 223.5.5.5
    "+.bing.com":
      - 223.5.5.5
    # …bing.net + 微软账号链路 20 条，每条都是 bare + "+." 两种 key
```

**`fallback` 那两行是必须的**。订阅自带的 `dns.fallback` 常见为 `https://1.1.1.1/dns-query` / `https://dns.google/dns-query`，这两个在国内都不可达；而 `fallback-filter: {geoip: true, geoip-code: CN}` 的语义是「nameserver 解析结果若不是中国 IP，就改用 fallback 的答案」。两者叠加 → **任何解析到非中国 IP 的域名，只要需要 mihomo 本地解析，就必然失败**，表现为直连时 5s 拨号超时 / HTTP 502。

实测受害面（2026-10-13）：`lencr.org` / `ocsp.digicert.com` —— 这是 Windows 取**中间证书（AIA）**与**吊销列表（OCSP）**的地址。取不到中间证书 → 证书链建不起来 → 浏览器判「证书不可信」、页面打不开（`login.tailscale.com` 的签发者正是 `CN=YE1, O=Let's Encrypt`，AIA 落在 `lencr.org`）。所以这条修复的意义远超「某些网站打不开」。

> 在 Clash Verge Rev 的 merge 槽位里，`dns.fallback` 是**替换**而非追加 —— 写上去之后原值会消失。

**`nameserver-policy` 是第 0 层直连规则的配套**。背景：在 `fake-ip` + `fallback-filter: geoip:CN` 的配置下，bing 域会解析到微软国际 anycast IP（如 `150.171.x.x`、`204.79.197.200`），被判定为非 CN → 触发境外 fallback DNS。

**规则层直连和 DNS 策略必须同时存在**——只写 `DOMAIN-SUFFIX,bing.com,DIRECT` 而不修 DNS，仍然会卡在解析阶段（实测：只加规则层时 `rewards.bing.com` 反而从 308 变成超时）。反过来也成立：一个域**走代理**时不查本地 DNS 所以看不出问题，一旦改直连就会暴露——`bing.net` 就是这种情况（改直连后 `cn.bing.net` 立即报 `dns resolve failed`）。

如果你用的是自己的 DNS 配置，**两段都可以整段删掉**；需要时再照葫芦画瓢追加其它域名（注意每条都要 `bare` + `+.` 两种 key）。

## Shadowrocket 使用

1. 导入配置：
   ```
   https://raw.githubusercontent.com/thintsing/proxy-rules/main/shadowrocket/shadowrocket_full.conf
   ```
2. 在 `[Proxy]` 段落填入节点

### DNS 与防泄露（2026-10-13 修订，重要）

Shadowrocket 的 DNS 行为和 Clash **不是一套机制**，这份 conf 的 DNS 处理要点：

- **DNS 覆写只对「直连类域名」生效**。匹配到 `Proxy` 策略的域名由代理服务器远端解析，不经过本地 DNS —— 这是好事，也是整套方案的前提。
- **但只要规则里出现 IP 类规则**（`IP-CIDR` / `GEOIP` / IP 段的 `RULE-SET`），Shadowrocket 为了判断是否命中，会**先把域名交给本地 DNS 解析一次**，然后再按规则决定走向。于是即使这个域名最后走代理，国内 DNS 也已经看到这次查询 —— 泄漏测试里冒出 AliDNS / DNSPod 就是这么来的，**与 Clash 侧 `lancidr` 缺 `no-resolve` 是同一个病**。
- **修法：给 IP 类规则统一加 `no-resolve`**（Shadowrocket 官方修饰符，语义与 Clash 一致 —— 域名请求直接跳过该规则，不做本地解析；只有「按 IP 访问」时才匹配）。本模板已对私网段（改为手写）与 `GEOIP,CN` 全部加上。
- `dns-server` / `direct-dns-server` 用国内 DoH（`doh.pub` + `dns.alidns.com`），`fallback-dns-server` 也换成 DoH 而**不是 `system`**（原来主 DoH 超时后会回退明文系统 DNS）。全程不出现明文 DNS。
- `hijack-dns = true` 拦截 App 发往硬编码 IP（如 `8.8.8.8`）的查询，堵住「App 自带 DNS 绕过 Shadowrocket」这条路。
- 第 0 层那 22 条 `DOMAIN-SUFFIX` 直连（bing + 微软账号链路）是**域名级匹配，不触发解析**，与 Clash merge 模板保持一致。

**自测方法**：小火箭 → 配置页 → 「测试规则」，输入一个国外域名，看它命中的规则名与策略；或看 Proxy Logs 里该连接的规则。若要测 DNS 泄露，在手机上用浏览器打开泄漏测试站点 —— **正常结果应该只剩代理节点所在地区的解析器**，不再出现 AliDNS / DNSPod 的出口 IP。

## 从零手写配置

不用 Clash Verge Rev、想自己写完整配置的话，参考 `example-config.yaml`（含节点、代理组、规则的完整骨架）。

## 更新

- **规则集**（`reject` / `proxy` / `direct` / `applications` / `lancidr`）：模板设了 `interval: 86400`，**每 24 小时自动拉取**，无需手动维护。
- **模板本身**：Clash Verge Rev 的增强槽位会在订阅更新时一并拉取；改动后重启 Clash 生效。
- `loyalsoldier/*.txt` 是归档快照，**不自动更新**，需要时手动从上游重新拉取（见上方快照表格记录的上游 commit）。

## 常见问题

| 现象 | 原因 | 处理 |
|------|------|------|
| 启动失败 / `proxy group [xxx] not found` | 规则引用的组名订阅里没有 | 导入 `clash-verge-groups.yaml`，或按订阅实际组名改规则 |
| 日志反复 `pull error: dns resolve failed` | provider 直连拉不到 GitHub | 给 provider 加 `proxy:` 字段 |
| 某网站打不开，关掉 Clash 就正常 | 该域名被解析到非 CN IP，触发了不可达的境外 fallback DNS | 把 `dns.fallback` 换成境内可达 DoH；该域名若要直连，再补 `DOMAIN-SUFFIX,<域名>,DIRECT` **且** `nameserver-policy` |
| **DNS 泄漏测试出现一堆国内解析器（阿里/腾讯），但请求明明是走代理的** | `RULE-SET,lancidr` 是 `behavior: ipcidr` 且**没带 `no-resolve`** → mihomo 会为**每条域名连接**先本地解析一次，而 `nameserver` 是国内 DNS | 改成 `RULE-SET,lancidr,🎯 全球直连,no-resolve`。实测中国解析器 8 条 → **0 条**。代价：该规则此后只对「按 IP 访问」生效，用**域名**访问内网需另加第 0 层 `DOMAIN-SUFFIX` 直连规则并配 `nameserver-policy` |
| 改了增强槽位但不生效 | 只重启了 `clash-verge-service` | 重启 GUI 进程 `clash-verge.exe` |

## 许可

规则数据版权归 [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules) 所有，本仓库为二次整理与增强槽封装。
