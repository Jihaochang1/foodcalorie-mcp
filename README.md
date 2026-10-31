# FoodCalorie MCP Server

**Chinese food & restaurant-chain nutrition data for AI agents** — 6 MCP tools so your agent stops guessing how many calories are in a Luckin coconut latte.

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![MCP SDK](https://img.shields.io/badge/MCP-v2.x-green.svg)](https://github.com/modelcontextprotocol/python-sdk)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/foodcalorie-mcp.svg)](https://pypi.org/project/foodcalorie-mcp/)
[![PyPI downloads](https://img.shields.io/pypi/dm/foodcalorie-mcp.svg)](https://pypi.org/project/foodcalorie-mcp/)

**[English](#english) · [中文](#中文)**

---

<a name="english"></a>

## English

### Why this exists

English nutrition data is everywhere — OpenFoodFacts, USDA, MyFitnessPal. **Chinese chain-restaurant menu data is not.** Ask an agent "how many calories in a Luckin coconut latte?" and it will either hallucinate a number or hand you a US Starbucks value as if it were the same thing.

This server gives your agent the actual data, with source links, and — just as importantly — **tells it when a field is missing instead of inventing one**.

### Install

```bash
pip install foodcalorie-mcp
```

> Mirror lag: Aliyun/Tsinghua mirrors can be a few days behind. To get the current version immediately, add `--index-url https://pypi.org/simple`.

### Configure

```json
{
  "mcpServers": {
    "foodcalorie": {
      "command": "python",
      "args": ["-m", "foodcalorie_mcp.server"]
    }
  }
}
```

Works with Claude Desktop, Cursor, Cline, WorkBuddy — anything that speaks MCP over stdio.

### Tools

| Tool | What it does |
|---|---|
| `search_food_by_name` | **Primary lookup.** Keyword search, Chinese or English, brand-aware (`瑞幸`, `luckin`, `蜜雪`) |
| `get_daily_nutrition_summary` | Sum a day's intake and show % of daily reference values |
| `compare_foods` | Side-by-side macro comparison across several items |
| `list_foods_by_category` | Browse by category (drinks / fast food / snacks / dairy / fruit…) |
| `get_health_tip` | Short dietary note for a given food |
| `search_food_by_barcode` | Barcode lookup — **see caveat below before relying on it** |

### ⚠️ Barcode caveat (read this first)

The free database is keyed on **example barcodes** (`6901234567890`-style sequential placeholders), **not real EAN codes printed on packaging.** So:

- Scanning a real product barcode **will not find it** — that is not a bug, there is simply no real-barcode mapping in the free set.
- Use `search_food_by_name` or `list_foods_by_category` instead.
- `search_food_by_barcode` is kept for signature compatibility and for you to load your own mapping into.

We put this at the top rather than let you discover it after installing.

### Data coverage (stated honestly)

Free tier: **103 items**, calories/protein/fat/carbs **103/103**.

Pro tier: **116 items across 14 Chinese chains** — calories **116/116**, official source link **116/116**, but macros are only present where the official page actually publishes them:

| Field | Coverage |
|---|---|
| Calories · source link · brand · item name | 116 / 116 |
| Protein | 59 / 116 |
| Fat | 61 / 116 |
| Carbs | 54 / 116 |
| Sugar | 15 / 116 |
| Sodium | 4 / 116 |
| Caffeine | 21 / 116 |
| **Allergens** | **0 — not provided** |

If you need "all 20 fields filled on every row", this is not that product — datasets like that are mostly fabricated. If you need "present means real, absent means absent", that is exactly the design premise here.

### Pricing

| Channel | Price | Delivery |
|---|---|---|
| **Agensi** (overseas, recommended) | **$6.99 USD** one-time | Instant, auto-delivered → <https://www.agensi.io/skills/foodcalorie-pro-data> |
| Direct (Alipay / WeChat, China) | **¥29** early bird → ¥49 | Manual, within 12h → <https://jihaochang1.github.io/foodcalorie-pro/> |

Details: <https://jihaochang1.github.io/foodcalorie-pro/en.html>

Both are one-time purchases, not subscriptions. Code is Apache-2.0; the Pro data pack is single-user, non-transferable.

### Maintainer

PRs to the official MCP SDK: `modelcontextprotocol/python-sdk` [#3746](https://github.com/modelcontextprotocol/python-sdk/pull/3746), `typescript-sdk` [#3076](https://github.com/modelcontextprotocol/typescript-sdk/pull/3076) / [#3118](https://github.com/modelcontextprotocol/typescript-sdk/pull/3118).

---

<a name="中文"></a>

## 中文

> 中国食品营养数据 MCP 服务器 —— 让 AI Agent 查得到、算得准、不瞎猜

> 🍔 **FoodCalorie Pro（¥49 一次性买断，早鸟 ¥29 限时至 2026-11-04）**
> 在免费版 103 条通用食品之外，另含 **116 条 / 14 个连锁品牌**的菜单数据（肯德基 24、海底捞 20、蜜雪冰城 16、麦当劳 14、星巴克 14、瑞幸 11、喜茶 5、古茗 4…），**卡路里 116/116 全覆盖**，每条都带官方来源链接。
> 营养字段按实际覆盖如实标注：蛋白质 59/116、脂肪 61/116、碳水 54/116、糖 15/116、钠 4/116、咖啡因 21/116。**不含过敏原数据**——不是漏了，是不提供，也明确告诉 agent 不要猜。
> 👉 **[查看 Pro 详情与购买](https://jihaochang1.github.io/foodcalorie-pro/)**

## 🚀 快速开始

### 安装

```bash
pip install foodcalorie-mcp
```

### 运行

```bash
foodcalorie-mcp
```

### 配置 Claude / Cursor / WorkBuddy

在 `.claude/settings.json` 或 `cursorrules` 中添加：

```json
{
  "mcpServers": {
    "foodcalorie": {
      "command": "python",
      "args": ["-m", "foodcalorie_mcp.server"]
    }
  }
}
```

---

## 📖 可用工具

| 工具 | 描述 | 参数 |
|------|------|------|
| `search_food_by_barcode` | 通过条码查询（⚠️ 见下方「关于条码」） | `barcode: string` |
| `search_food_by_name` | 通过名称关键词搜索（中英文均可，支持品牌联想） | `keyword: string`, `limit: int` |
| `get_daily_nutrition_summary` | 计算每日营养摄入汇总及每日值占比 | `items: list[dict]` |
| `get_health_tip` | 获取健康饮食建议 | `food_name: string` |
| `list_foods_by_category` | 按类别列出食品 | `category: string?`, `limit: int` |
| `compare_foods` | 多食品营养成分对比 | `barcode_list: list[str]` |

### ⚠️ 关于条码（请先读这一段）

免费版数据库的键是**示例条码**（`6901234567890` 这类连号占位值），**不是真实商品包装上的 EAN 条码**。因此：

- **拿真实商品扫码来查，查不到**——这不是 bug，是数据里没有真实条码映射。
- 可用的查询方式是 **`search_food_by_name`（名称关键词）**，或用 `list_foods_by_category` 按类别浏览。
- `search_food_by_barcode` 目前只对内置示例条码有效，保留它是为了兼容工具签名和自建映射（你可以把自己的条码表灌进来覆盖）。

我们宁可把这件事写在最前面，也不想你装上之后踩坑才发现。

---

## 💡 使用示例

### 按名称查询（推荐）

```
用户: 蜜雪冰城柠檬水多少卡？
AI: 调用 search_food_by_name(keyword="蜜雪冰城柠檬水")
```

### 计算每日摄入

```
用户: 我今天喝了可乐、一杯牛奶，还吃了鸡胸肉，算一下总热量
AI: 先 search_food_by_name 定位条目，再调用 get_daily_nutrition_summary(items=[...])
```

### 按类别浏览

```
AI: 调用 list_foods_by_category(category="快餐", limit=5)
```

### 对比食品

```
AI: 调用 compare_foods(barcode_list=["6901234567890", "6921234567896"])
```

---

## 🎯 免费版 vs Pro

### Free（免费，Apache-2.0）

- ✅ 103 条通用中国食品数据
- ✅ 6 个 MCP 工具
- ✅ 热量 / 蛋白质 / 脂肪 / 碳水 **103/103 全覆盖**
- ✅ 名称搜索（中英文）、品类浏览、营养对比、每日汇总
- ⚠️ 条码为示例值，非真实 EAN（见上）
- ⚠️ 钠、糖、维生素、矿物质等字段**部分条目才有**，缺的会返回空而不是 0

### Pro（¥49 买断，早鸟 ¥29 限时至 2026-11-04）

- ✅ **免费版全部功能**
- ✅ **116 条 / 14 个连锁品牌**菜单数据
- ✅ **卡路里 116/116**，来源链接 116/116（每条可溯源到官方营养页）
- ✅ 蛋白质 59、脂肪 61、碳水 54、糖 15、钠 4、咖啡因 21（如实标注，不做填充猜测）
- ✅ 明确告知 agent「缺失字段不要推算」，避免一本正经地编
- ✅ 一个环境变量加载，小版本更新免费
- ❌ **不含过敏原数据**（当前没有可靠来源，宁缺勿造）

### 数据完整度（这是 Pro 的真实质量表）

| 字段 | 覆盖 | 说明 |
|---|---|---|
| 热量 | 116/116 | 全部有值 |
| 官方来源链接 | 116/116 | 全部可溯源 |
| 品牌 / 品名 / 规格 | 116/116 | 全部有值 |
| 蛋白质 | 59/116 | 官方页有标注的才录 |
| 脂肪 | 61/116 | 同上 |
| 碳水 | 54/116 | 同上 |
| 糖 | 15/116 | 中国区营养表常不标糖 |
| 钠 | 4/116 | 覆盖率低，别当完整数据用 |
| 咖啡因 | 21/116 | 仅咖啡/茶饮类品牌标注 |
| 过敏原 | 0 | **不提供** |

> 如果你需要的是「每条 20 个字段全满」的完美数据集，这个产品不适合你——那种数据市面上基本都是编的。如果你要的是「有就是有、没有就说没有」的数据，这是它的设计前提。

### Enterprise（项目制报价，¥10,000 起）

- ✅ 私有化部署 + 自有菜品/商品数据录入
- ✅ 自定义 schema、对接你的内部系统
- ✅ 培训 + 3 个月技术支持
- ✅ 需求评估后报价，不做标准套餐

---

## 💳 购买方式

| 渠道 | 价格 | 交付 | 适合 |
|---|---|---|---|
| **官网直购**（支付宝 / 微信） | **¥29 早鸟**（限时至 2026-11-04），之后 ¥49 | 人工发送（通常 12 小时内） | 国内用户 |
| **Agensi 平台** | **$6.99 USD** | **自动交付、平台代扣税，即时下载** | 海外用户（推荐） |
| **PayPal** | **$6.99 USD** | 邮件索取收款请求，付完即发 | 海外用户，不想走平台 |

- 官网（支付宝 / 微信 / PayPal / Agensi）：<https://jihaochang1.github.io/foodcalorie-pro/>
- Agensi 直接购买：<https://www.agensi.io/skills/foodcalorie-pro-data>
- 企业采购 / 定制：对公转账，见下方联系方式

付款后请把**订单截图或交易号**发给下面的联系方式，换取下载链接（Agensi 购买会自动交付，无需邮件）。

---

## 📦 免费版覆盖情况

| 一级分类 | 数量 | 代表条目 |
|------|------|----------|
| 饮料 | 22 | 可口可乐、元气森林、农夫山泉、瑞幸、喜茶… |
| 快餐 | 11 | 麦当劳、肯德基、汉堡王、沙县、老乡鸡… |
| 零食 | 10 | 乐事、奥利奥、三只松鼠、卫龙… |
| 水果 | 8 | 苹果、香蕉、草莓、猕猴桃… |
| 乳制品 | 7 | 伊利、蒙牛、安慕希、简爱… |
| 肉类 | 6 | 鸡胸肉、牛肉、猪肉、三文鱼… |
| 主食 | 6 | 米饭、面条、饺子、炒饭… |
| 便利店 | 3 | 全家、7-11、罗森便当 |
| 火锅食材 | 3 | 毛肚、肥牛、虾滑 |
| 其他 | 27 | 蛋类、豆制品、海鲜、调味品、速食、甜点… |

> 「快餐」里的品牌条目是**通用参考值**（如「汉堡王皇堡」），不是逐 SKU 的官方菜单数据。逐 SKU 的官方数据在 Pro 包里。

---

## 🛠️ 开发

```bash
git clone https://github.com/Jihaochang1/foodcalorie-mcp
cd foodcalorie-mcp
pip install -e ".[dev]"

pytest tests/
ruff format src/
```

---

## 📄 许可证

代码 Apache-2.0。Pro 数据包为**单用户、不可转让**授权，禁止再分发。

---

## 🤝 联系

- GitHub Issues：<https://github.com/Jihaochang1/foodcalorie-mcp/issues>（48 小时内回复，付费用户优先）
- 邮件：`jihaochang1@github.com`（购买 / 定制 / 合作）

---

*数据能不编就不编，编一次就没人再信了。* 🥗

**⭐ 觉得有用请给个 Star，这是持续维护唯一的正反馈。**
