# proxy-rules

Clash 规则配置，基于 [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules) 官方规则 + GEOSITE 内置数据库，面向 **Clash Verge Rev**（mihomo 内核）的增强槽（merge / groups）使用方式。

## 架构

```
┌─ 规则优先级 ───────────────────────────────────────────────────┐
│ 0. 强制直连 (1 条)          → bing.com 全系恒定 DIRECT         │
│ 1. 自定义覆盖 (3 RULE-SET)  → AI / Steam / 直连覆盖            │
│ 2. Loyalsoldier 核心 (4)    → applications/reject/proxy/direct │
│ 3. LAN 私有网段 (1 RULE-SET)→ lancidr                          │
│ 4. GEOSITE 补充 (8 条)      → 内置数据库，零网络开销           │
│ 5. GEOIP,CN                 → 国内 IP 直连                     │
│ 6. MATCH                    → 最终兜底                         │
└──────────────────────────────────────────────────────────────┘
                       共 19 条规则
```

设计要点：

- **第 0 层用 `DIRECT` 关键字而非代理组名**。`bing.com` 如果只靠 `GEOSITE,microsoft` 命中 `Ⓜ️ 微软服务`，那是个 `select` 组——在面板里切换过就会跟着变。写死 `DIRECT` 才能恒定直连。
- **第 1 层排在 GEOSITE 之前**，保证自定义覆盖优先级最高。
- **GEOSITE 段零网络开销**，分类数据来自内核自带的 `geosite.dat`，不产生额外请求。

## 文件说明

| 文件 | 用途 |
|------|------|
| `clash-verge-merge.yaml` | **Clash Verge Rev merge 模板**：8 个 rule-provider + 19 条规则 + DNS 策略 |
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

模板末尾有一段 `dns.nameserver-policy`：

```yaml
dns:
  nameserver-policy:
    "bing.com":
      - 223.5.5.5
    "+.bing.com":
      - 223.5.5.5
```

**背景**：在 `fake-ip` + `fallback-filter: geoip:CN` 的配置下，`bing.com` 会解析到微软国际 anycast IP（如 `150.171.x.x`），被判定为非 CN → 触发境外 fallback DNS。如果那个 fallback 在本网络不可达，就表现为「解析超时、页面打不开」。

**注意：规则层直连和 DNS 策略必须同时存在**——只写 `DOMAIN-SUFFIX,bing.com,DIRECT` 而不修 DNS，仍然会卡在解析阶段（实测：只加规则层时 `rewards.bing.com` 反而从 308 变成超时）。

如果你用的是自己的 DNS 配置，**整段删掉**即可；需要时再照葫芦画瓢追加其它微软域名。

## Shadowrocket 使用

1. 导入配置：
   ```
   https://raw.githubusercontent.com/thintsing/proxy-rules/main/shadowrocket/shadowrocket_full.conf
   ```
2. 在 `[Proxy]` 段落填入节点

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
| 某网站打不开，关掉 Clash 就正常 | 该域名被解析到非 CN IP，触发了不可达的境外 fallback DNS | 规则层加 `DOMAIN-SUFFIX,<域名>,DIRECT` **且** DNS 层加 `nameserver-policy` |
| 改了增强槽位但不生效 | 只重启了 `clash-verge-service` | 重启 GUI 进程 `clash-verge.exe` |

## 许可

规则数据版权归 [Loyalsoldier/clash-rules](https://github.com/Loyalsoldier/clash-rules) 所有，本仓库为二次整理与增强槽封装。
