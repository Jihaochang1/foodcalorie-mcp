# FoodCalorie MCP Server

> 中国食品营养数据MCP服务器 - 扫码查热量，健康饮食更轻松

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![MCP SDK](https://img.shields.io/badge/MCP-v2.x-green.svg)](https://github.com/modelcontextprotocol/python-sdk)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/foodcalorie-mcp.svg)](https://pypi.org/project/foodcalorie-mcp/)
[![PyPI downloads](https://img.shields.io/pypi/dm/foodcalorie-mcp.svg)](https://pypi.org/project/foodcalorie-mcp/)

---

## 🚀 快速开始

### 安装

```bash
pip install -e .
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
| `search_food_by_barcode` | 通过条形码查询食品营养数据 | `barcode: string` |
| `search_food_by_name` | 通过名称关键词搜索食品（支持品牌联想） | `keyword: string`, `limit: int` |
| `get_daily_nutrition_summary` | 计算每日营养摄入汇总及每日值占比 | `items: list[dict]` |
| `get_health_tip` | 获取健康饮食建议 | `food_name: string` |
| `list_foods_by_category` | 按类别列出食品 | `category: string?`, `limit: int` |
| `compare_foods` | 多食品营养成分对比 | `barcode_list: list[str]` |

---

## 💡 使用示例

### 查询特定食品
```
用户: 查询条形码6901234567890的营养信息
AI: 调用 search_food_by_barcode(barcode="6901234567890")
```

### 计算每日摄入
```
用户: 我今天吃了可乐、牛奶和鸡胸肉，帮我计算总热量
AI: 调用 get_daily_nutrition_summary(items=[{"barcode":"6901234567890"}, ...])
```

### 按类别浏览
```
AI: 调用 list_foods_by_category(category="肉类", limit=5)
```

### 对比食品
```
AI: 调用 compare_foods(barcode_list=["6961234567890", "6961234567896"])
```

---

## 🎯 免费 vs Pro

### Free Tier（免费）
- ✅ 100+ 条中国食品数据库
- ✅ 条形码查询
- ✅ 名称搜索（支持中英文）
- ✅ 每日营养汇总
- ✅ 健康饮食建议
- ✅ 品类浏览 & 营养对比

### Pro Tier（¥49 买断制）
- ✅ **所有Free功能**
- ✅ **116条连锁餐饮品牌数据**（肯德基、麦当劳、星巴克、瑞幸、蜜雪冰城等14个品牌）
- ✅ 含咖啡因、钠含量、过敏原等详细营养指标
- ✅ 每条数据带官方来源链接（可溯源）
- ✅ 小版本更新免费（新增品牌持续加入）
- ✅ 三行代码即可集成到您的 MCP 服务

> 💰 **立即购买** 👉 [查看 FoodCalorie Pro 详情页](https://jihaochang1.github.io/foodcalorie-pro/) 扫码支付宝 ¥49 买断

### Enterprise（定制报价）
- ✅ **所有Pro功能**
- ✅ API 访问权限
- ✅ 私有数据集定制
- ✅ 专属技术支持
- ✅ 品牌白标选项
- ✅ SLA 保障

---

## 📦 数据库覆盖

| 分类 | 数量 | 代表品牌 |
|------|------|----------|
| 饮料 | 22 | 可口可乐、农夫山泉、元气森林、瑞幸、喜茶... |
| 快餐 | 11 | 麦当劳、肯德基、汉堡王、沙县、老乡鸡... |
| 零食 | 10 | 乐事、奥利奥、三只松鼠、卫龙... |
| 水果 | 8 | 苹果、香蕉、草莓、猕猴桃... |
| 乳制品 | 7 | 伊利、蒙牛、安慕希、简爱... |
| 肉类 | 6 | 鸡胸肉、牛肉、猪肉、三文鱼... |
| 主食 | 6 | 米饭、面条、饺子、炒饭... |
| 便利店 | 3 | 全家、7-11、罗森便当 |
| 火锅食材 | 3 | 毛肚、肥牛、虾滑 |
| ... | ... | ... |

---

## 🛠️ 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/

# 代码格式化
ruff format src/
```

---

## 📄 许可证

Apache-2.0

---

## 🤝 贡献

欢迎 PR！请先 Fork 并创建特性分支。

---

## 💼 技术服务 & 商业合作

### MCP 定制开发
基于你的数据源或业务场景，快速开发专属 MCP Server。

- **定价**: ¥2,000 - 10,000 / 项目
- **交付**: 完整代码 + 文档 + 部署支持
- **联系**: [GitHub Issues](https://github.com/Jihaochang1/foodcalorie-mcp/issues) 或邮件

### MCP 技术咨询
帮你排查 MCP 配置问题、调试工具逻辑、优化性能。

- **定价**: ¥500 - 1,000 / 小时
- **形式**: 远程视频 / 文字沟通
- **联系**: [GitHub Issues](https://github.com/Jihaochang1/foodcalorie-mcp/issues)

### 企业私有化部署
为企业提供本地化部署 + 定制化数据接入。

- **定价**: ¥10,000 起（根据需求报价）
- **包含**: 部署 + 培训 + 3个月技术支持

### 联系方式
- **邮箱**: jihaochang1@github.com
- **GitHub**: [@Jihaochang1](https://github.com/Jihaochang1)
- **付款方式**: 联系后提供（支持支付宝 / 银行转账）

---

*让 AI 帮你吃得健康！* 🥗

**⭐ 如果觉得有用，请给个 Star！你的支持是我持续维护的动力**
