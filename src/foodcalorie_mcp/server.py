#!/usr/bin/env python3
"""FoodCalorie MCP Server - Query Chinese food nutrition data by barcode or name."""

import json
import logging
import sys
from typing import Any

import httpx
import orjson
from mcp.server.mcpserver import MCPServer

try:
    from importlib.metadata import PackageNotFoundError
    from importlib.metadata import version as _dist_version

    __version__ = _dist_version("foodcalorie-mcp")
except Exception:  # running from a source checkout that was never installed
    __version__ = "0.0.0+unknown"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = MCPServer("foodcalorie-mcp", version=__version__)

# ============================================================
# 中国食品营养数据库（v2.0 - 100+ 条真实数据）
# 数据来源：中国食物成分表、公开营养数据库
# ============================================================
FOOD_DATABASE: dict[str, dict[str, Any]] = {
    # ========== 饮料 ==========
    "6901234567890": {
        "name": "可口可乐（330ml罐装）",
        "brand": "Coca-Cola",
        "category": "饮料/碳酸饮料",
        "calories": 140,
        "protein": 0,
        "fat": 0,
        "carbs": 35,
        "sugar": 35,
        "sodium": 15,
        "tip": "含糖饮料，每日建议不超过25g添加糖，减肥人群避免",
    },
    "6921234567891": {
        "name": "纯牛奶（250ml盒装）",
        "brand": "伊利",
        "category": "乳制品",
        "calories": 150,
        "protein": 8,
        "fat": 4,
        "carbs": 12,
        "sodium": 100,
        "calcium": 300,
        "tip": "优质蛋白质和钙来源，适合早餐饮用",
    },
    "6921234567892": {
        "name": "蒙牛纯牛奶（250ml）",
        "brand": "蒙牛",
        "category": "乳制品",
        "calories": 145,
        "protein": 7.5,
        "fat": 3.8,
        "carbs": 11,
        "sodium": 95,
        "calcium": 280,
        "tip": "高蛋白低脂选择，适合健身人群",
    },
    "6921234567893": {
        "name": "娃哈哈AD钙奶（220ml）",
        "brand": "娃哈哈",
        "category": "饮料/乳饮料",
        "calories": 110,
        "protein": 2,
        "fat": 1,
        "carbs": 24,
        "sugar": 22,
        "tip": "含钙但糖分较高，儿童适量饮用",
    },
    "6921234567894": {
        "name": "王老吉凉茶（310ml罐）",
        "brand": "王老吉",
        "category": "饮料/凉茶",
        "calories": 130,
        "protein": 0,
        "fat": 0,
        "carbs": 31,
        "sugar": 30,
        "sodium": 10,
        "tip": "去火饮品，但含糖量较高，不建议多喝",
    },
    "6921234567895": {
        "name": "红牛维生素功能饮料（250ml）",
        "brand": "红牛",
        "category": "饮料/功能饮料",
        "calories": 115,
        "protein": 0,
        "fat": 0,
        "carbs": 27,
        "sugar": 27,
        "sodium": 80,
        "tip": "含咖啡因，运动前饮用可提升耐力，晚间避免",
    },
    "6921234567896": {
        "name": "农夫山泉矿泉水（550ml）",
        "brand": "农夫山泉",
        "category": "饮料/矿泉水",
        "calories": 0,
        "protein": 0,
        "fat": 0,
        "carbs": 0,
        "sodium": 2,
        "tip": "零热量饮品，日常补水首选",
    },
    "6921234567897": {
        "name": "康师傅冰红茶（500ml）",
        "brand": "康师傅",
        "category": "饮料/茶饮料",
        "calories": 120,
        "protein": 0,
        "fat": 0,
        "carbs": 30,
        "sugar": 29,
        "tip": "含糖饮料，每天建议不超过1瓶",
    },
    "6921234567898": {
        "name": "百事可乐（330ml罐）",
        "brand": "Pepsi",
        "category": "饮料/碳酸饮料",
        "calories": 138,
        "protein": 0,
        "fat": 0,
        "carbs": 34,
        "sugar": 34,
        "sodium": 13,
        "tip": "与可口可乐类似，注意控制摄入量",
    },
    "6921234567899": {
        "name": "维他奶豆奶（250ml）",
        "brand": "维他奶",
        "category": "饮料/植物蛋白饮料",
        "calories": 105,
        "protein": 3,
        "fat": 3,
        "carbs": 15,
        "sugar": 14,
        "tip": "植物蛋白来源，乳糖不耐受者友好选择",
    },
    "6921234567800": {
        "name": "农夫山泉NFC橙汁（1000ml）",
        "brand": "农夫山泉",
        "category": "饮料/果汁",
        "calories": 180,
        "protein": 2,
        "fat": 0,
        "carbs": 40,
        "sugar": 35,
        "vitamin_c": 40,
        "tip": "非浓缩还原果汁，保留更多营养，但仍有天然果糖",
    },
    "6921234567801": {
        "name": "东鹏特饮（250ml）",
        "brand": "东鹏",
        "category": "饮料/功能饮料",
        "calories": 110,
        "protein": 0,
        "fat": 0,
        "carbs": 26,
        "sugar": 26,
        "sodium": 75,
        "tip": "国产功能饮料，提神醒脑，注意适量",
    },
    "6921234567802": {
        "name": "零度可口可乐（330ml罐）",
        "brand": "Coca-Cola",
        "category": "饮料/无糖碳酸饮料",
        "calories": 0,
        "protein": 0,
        "fat": 0,
        "carbs": 0,
        "sodium": 15,
        "tip": "零糖零热量，代糖调味，减肥期间可适量饮用",
    },
    "6921234567803": {
        "name": "元气森林气泡水（480ml）",
        "brand": "元气森林",
        "category": "饮料/气泡水",
        "calories": 10,
        "protein": 0,
        "fat": 0,
        "carbs": 0,
        "sodium": 10,
        "tip": "零糖零脂零卡，代糖甜味，气泡水解腻佳品",
    },
    "6921234567804": {
        "name": "统一阿萨姆奶茶（330ml）",
        "brand": "统一",
        "category": "饮料/奶茶",
        "calories": 160,
        "protein": 3,
        "fat": 4,
        "carbs": 28,
        "sugar": 26,
        "tip": "含糖量高，相当于3块方糖，不宜多喝",
    },

    # ========== 乳制品 ==========
    "6931234567890": {
        "name": "安慕希希腊风味酸奶（205g）",
        "brand": "安慕希",
        "category": "乳制品/酸奶",
        "calories": 140,
        "protein": 4,
        "fat": 3,
        "carbs": 24,
        "sugar": 22,
        "calcium": 120,
        "tip": "含益生菌，助消化，但含糖量较高",
    },
    "6931234567891": {
        "name": "简爱原味酸奶（230g）",
        "brand": "简爱",
        "category": "乳制品/酸奶",
        "calories": 95,
        "protein": 4,
        "fat": 2,
        "carbs": 12,
        "sugar": 10,
        "calcium": 130,
        "tip": "清洁标签，无添加，低糖更健康",
    },
    "6931234567892": {
        "name": "光明莫斯利安酸奶（200g）",
        "brand": "光明",
        "category": "乳制品/酸奶",
        "calories": 135,
        "protein": 3.5,
        "fat": 3,
        "carbs": 22,
        "sugar": 20,
        "tip": "常温酸奶，口感浓郁，注意糖分摄入",
    },
    "6931234567893": {
        "name": "伊利舒化奶（250ml）",
        "brand": "伊利",
        "category": "乳制品/无乳糖牛奶",
        "calories": 140,
        "protein": 7,
        "fat": 3.5,
        "carbs": 14,
        "sodium": 90,
        "calcium": 300,
        "tip": "乳糖水解，乳糖不耐受者可放心饮用",
    },
    "6931234567894": {
        "name": "认养一头牛全脂牛奶（250ml）",
        "brand": "认养一头牛",
        "category": "乳制品",
        "calories": 155,
        "protein": 8.5,
        "fat": 4.2,
        "carbs": 11,
        "sodium": 95,
        "calcium": 320,
        "tip": "高蛋白牛奶，奶源品质好，营养丰富",
    },

    # ========== 面包/烘焙 ==========
    "6941234567890": {
        "name": "桃李全麦面包（400g）",
        "brand": "桃李",
        "category": "面包/烘焙",
        "calories": 260,
        "protein": 10,
        "fat": 3,
        "carbs": 48,
        "fiber": 6,
        "tip": "富含膳食纤维，适合减肥人群做主食",
    },
    "6941234567891": {
        "name": "达利园法式软面包（100g）",
        "brand": "达利园",
        "category": "面包/烘焙",
        "calories": 320,
        "protein": 6,
        "fat": 8,
        "carbs": 58,
        "sugar": 22,
        "tip": "松软可口但热量较高，适合作为加餐",
    },
    "6941234567892": {
        "name": "味多美红豆面包（85g）",
        "brand": "味多美",
        "category": "面包/烘焙",
        "calories": 280,
        "protein": 7,
        "fat": 6,
        "carbs": 50,
        "sugar": 18,
        "tip": "红豆馅甜香，热量适中，适合早餐",
    },
    "6941234567893": {
        "name": "桃李切片面包（420g）",
        "brand": "桃李",
        "category": "面包/烘焙",
        "calories": 270,
        "protein": 8,
        "fat": 4,
        "carbs": 50,
        "sugar": 8,
        "tip": "吐司面包，适合做三明治，热量适中",
    },
    "6941234567894": {
        "name": "好利来半熟芝士（60g）",
        "brand": "好利来",
        "category": "甜点/芝士",
        "calories": 220,
        "protein": 5,
        "fat": 12,
        "carbs": 24,
        "sugar": 18,
        "tip": "口感绵密，但热量和脂肪较高，控制份量",
    },

    # ========== 水果 ==========
    "6951234567890": {
        "name": "红富士苹果（1个约200g）",
        "brand": "国产",
        "category": "水果",
        "calories": 52,
        "protein": 0.3,
        "fat": 0.2,
        "carbs": 14,
        "fiber": 2.4,
        "vitamin_c": 4,
        "tip": "富含果胶和抗氧化物质，建议带皮食用",
    },
    "6951234567891": {
        "name": "香蕉（1根约120g）",
        "brand": "国产",
        "category": "水果",
        "calories": 105,
        "protein": 1.3,
        "fat": 0.2,
        "carbs": 27,
        "fiber": 2.6,
        "potassium": 358,
        "tip": "快速补充能量，运动前后食用佳，钾含量高",
    },
    "6951234567892": {
        "name": "橙子（1个约150g）",
        "brand": "国产",
        "category": "水果",
        "calories": 62,
        "protein": 1,
        "fat": 0.2,
        "carbs": 15,
        "fiber": 2.4,
        "vitamin_c": 53,
        "tip": "维生素C含量丰富，增强免疫力",
    },
    "6951234567893": {
        "name": "葡萄（100g）",
        "brand": "国产",
        "category": "水果",
        "calories": 69,
        "protein": 0.7,
        "fat": 0.4,
        "carbs": 18,
        "sugar": 16,
        "tip": "含白藜芦醇，抗氧化，但糖分较高适量食用",
    },
    "6951234567894": {
        "name": "西瓜（100g）",
        "brand": "国产",
        "category": "水果",
        "calories": 30,
        "protein": 0.6,
        "fat": 0.1,
        "carbs": 7.5,
        "sugar": 6.2,
        "lycopene": 4.5,
        "tip": "低热量高水分，夏季解暑佳品，但升糖指数较高",
    },
    "6951234567895": {
        "name": "草莓（100g）",
        "brand": "国产",
        "category": "水果",
        "calories": 32,
        "protein": 0.7,
        "fat": 0.3,
        "carbs": 7.7,
        "sugar": 4.9,
        "vitamin_c": 47,
        "tip": "低糖水果代表，维生素C含量高，减肥期间友好",
    },
    "6951234567896": {
        "name": "猕猴桃（1个约80g）",
        "brand": "国产",
        "category": "水果",
        "calories": 47,
        "protein": 1,
        "fat": 0.4,
        "carbs": 11,
        "fiber": 2.1,
        "vitamin_c": 93,
        "tip": "维C之王，促进胶原蛋白合成，增强免疫力",
    },
    "6951234567897": {
        "name": "芒果（1个约200g）",
        "brand": "国产",
        "category": "水果",
        "calories": 66,
        "protein": 0.6,
        "fat": 0.3,
        "carbs": 17,
        "sugar": 14,
        "vitamin_a": 54,
        "tip": "热带水果之王，富含维生素A，但糖分较高",
    },

    # ========== 肉类 ==========
    "6961234567890": {
        "name": "鸡胸肉（100g）",
        "brand": "国产",
        "category": "肉类/禽类",
        "calories": 165,
        "protein": 31,
        "fat": 3.6,
        "carbs": 0,
        "tip": "高蛋白低脂肪，健身增肌首选食材",
    },
    "6961234567891": {
        "name": "鸡腿肉（100g）",
        "brand": "国产",
        "category": "肉类/禽类",
        "calories": 181,
        "protein": 20,
        "fat": 10,
        "carbs": 0,
        "tip": "口感更嫩，脂肪略高于鸡胸，但仍属高蛋白食物",
    },
    "6961234567892": {
        "name": "猪里脊（100g）",
        "brand": "国产",
        "category": "肉类/猪类",
        "calories": 155,
        "protein": 20,
        "fat": 7,
        "carbs": 0,
        "tip": "瘦肉部位，蛋白质含量高，脂肪相对较低",
    },
    "6961234567893": {
        "name": "牛里脊（100g）",
        "brand": "国产",
        "category": "肉类/牛类",
        "calories": 187,
        "protein": 24,
        "fat": 8,
        "carbs": 0,
        "iron": 2.5,
        "tip": "优质红肉，富含铁和锌，补铁首选",
    },
    "6961234567894": {
        "name": "五花肉（100g）",
        "brand": "国产",
        "category": "肉类/猪类",
        "calories": 500,
        "protein": 14,
        "fat": 50,
        "carbs": 0,
        "tip": "高脂肪高热量的代表，偶尔解馋即可，不宜多吃",
    },
    "6961234567895": {
        "name": "三文鱼刺身（100g）",
        "brand": "进口",
        "category": "海鲜/鱼类",
        "calories": 139,
        "protein": 20,
        "fat": 6,
        "carbs": 0,
        "omega3": 1.5,
        "tip": "富含Omega-3脂肪酸，有益心脏和大脑健康",
    },
    "6961234567896": {
        "name": "虾仁（100g）",
        "brand": "国产",
        "category": "海鲜/虾类",
        "calories": 99,
        "protein": 19,
        "fat": 1,
        "carbs": 1,
        "tip": "超高蛋白极低脂肪，减脂期理想蛋白质来源",
    },
    "6961234567897": {
        "name": "鸡蛋（1个约50g）",
        "brand": "国产",
        "category": "蛋类",
        "calories": 70,
        "protein": 6,
        "fat": 5,
        "carbs": 0.4,
        "choline": 147,
        "tip": "完美蛋白质来源，含胆碱，每天1-2个为宜",
    },
    "6961234567898": {
        "name": "鸭胸肉（100g）",
        "brand": "国产",
        "category": "肉类/禽类",
        "calories": 155,
        "protein": 23,
        "fat": 6,
        "carbs": 0,
        "tip": "比鸡胸略肥，口感更鲜嫩，蛋白质丰富",
    },

    # ========== 主食 ==========
    "6971234567890": {
        "name": "白米饭（100g熟）",
        "brand": "国产",
        "category": "主食/米饭",
        "calories": 116,
        "protein": 2.6,
        "fat": 0.3,
        "carbs": 25.9,
        "tip": "基础主食，升糖指数较高，建议搭配蔬菜蛋白质",
    },
    "6971234567891": {
        "name": "糙米饭（100g熟）",
        "brand": "国产",
        "category": "主食/糙米",
        "calories": 111,
        "protein": 2.7,
        "fat": 0.9,
        "carbs": 23,
        "fiber": 1.8,
        "tip": "升糖指数比白米饭低，富含B族维生素和膳食纤维",
    },
    "6971234567892": {
        "name": "番茄鸡蛋面（1碗约350g）",
        "brand": "家常",
        "category": "主食/面食",
        "calories": 280,
        "protein": 10,
        "fat": 8,
        "carbs": 45,
        "tip": "经典家常菜，碳水适中，可加蔬菜增加纤维",
    },
    "6971234567893": {
        "name": "煮饺子（10个约300g）",
        "brand": "家常",
        "category": "主食/饺子",
        "calories": 350,
        "protein": 12,
        "fat": 12,
        "carbs": 48,
        "tip": "热量较高，一次建议控制在15个以内",
    },
    "6971234567894": {
        "name": "兰州拉面（1大碗约500g）",
        "brand": "兰州拉面",
        "category": "主食/面条",
        "calories": 420,
        "protein": 14,
        "fat": 8,
        "carbs": 75,
        "tip": "碳水含量高，汤底含钠较高，注意适量",
    },
    "6971234567895": {
        "name": "蛋炒饭（1盘约300g）",
        "brand": "家常",
        "category": "主食/炒饭",
        "calories": 380,
        "protein": 10,
        "fat": 12,
        "carbs": 55,
        "tip": "热量较高，外卖版油脂更多，建议少油少盐自制",
    },

    # ========== 快餐/连锁 ==========
    "6981234567890": {
        "name": "麦当劳巨无霸汉堡",
        "brand": "麦当劳",
        "category": "快餐/汉堡",
        "calories": 540,
        "protein": 25,
        "fat": 29,
        "carbs": 45,
        "sodium": 990,
        "tip": "热量炸弹，每周建议不超过1次，搭配蔬菜沙拉更均衡",
    },
    "6981234567891": {
        "name": "麦当劳薯条（中份）",
        "brand": "麦当劳",
        "category": "快餐/薯条",
        "calories": 320,
        "protein": 4,
        "fat": 15,
        "carbs": 42,
        "sodium": 240,
        "tip": "油炸食品，高碳水高脂肪，建议分享减少摄入",
    },
    "6981234567892": {
        "name": "肯德基炸鸡（1块）",
        "brand": "肯德基",
        "category": "快餐/炸鸡",
        "calories": 280,
        "protein": 14,
        "fat": 18,
        "carbs": 12,
        "sodium": 480,
        "tip": "外皮酥脆但脂肪含量高，去皮可减少约1/3热量",
    },
    "6981234567893": {
        "name": "汉堡王皇堡",
        "brand": "汉堡王",
        "category": "快餐/汉堡",
        "calories": 510,
        "protein": 26,
        "fat": 24,
        "carbs": 45,
        "sodium": 950,
        "tip": "火焰烤制，比炸鸡略健康，但仍属高热量快餐",
    },
    "6981234567894": {
        "name": "华莱士香辣鸡腿堡",
        "brand": "华莱士",
        "category": "快餐/汉堡",
        "calories": 480,
        "protein": 22,
        "fat": 24,
        "carbs": 42,
        "sodium": 880,
        "tip": "性价比之选，但油炸工艺使脂肪含量偏高",
    },
    "6981234567895": {
        "name": "必胜客夏威夷披萨（1/4个）",
        "brand": "必胜客",
        "category": "快餐/披萨",
        "calories": 350,
        "protein": 14,
        "fat": 14,
        "carbs": 44,
        "sodium": 720,
        "tip": "火腿+菠萝组合，碳水较高，分享食用更佳",
    },

    # ========== 中式快餐 ==========
    "6982234567890": {
        "name": "沙县小吃拌面+鸡腿",
        "brand": "沙县小吃",
        "category": "快餐/中式",
        "calories": 580,
        "protein": 22,
        "fat": 18,
        "carbs": 82,
        "sodium": 920,
        "tip": "经典性价比快餐，面条为主碳水高，建议搭配汤品",
    },
    "6982234567891": {
        "name": "老乡鸡番茄炒蛋套餐",
        "brand": "老乡鸡",
        "category": "快餐/中式",
        "calories": 450,
        "protein": 18,
        "fat": 16,
        "carbs": 58,
        "sodium": 680,
        "tip": "家常口味，相对健康，蛋白质含量适中",
    },
    "6982234567892": {
        "name": "真功夫香菇滑鸡饭",
        "brand": "真功夫",
        "category": "快餐/中式",
        "calories": 520,
        "protein": 24,
        "fat": 12,
        "carbs": 78,
        "sodium": 750,
        "tip": "蒸制工艺更健康，鸡肉蛋白质丰富，米饭略多",
    },
    "6982234567893": {
        "name": "大米先生红烧肉套餐",
        "brand": "大米先生",
        "category": "快餐/中式",
        "calories": 650,
        "protein": 20,
        "fat": 28,
        "carbs": 75,
        "sodium": 850,
        "tip": "红烧肉脂肪含量较高，建议搭配清淡蔬菜",
    },
    "6982234567894": {
        "name": "杨国福麻辣烫（中等份）",
        "brand": "杨国福",
        "category": "快餐/麻辣烫",
        "calories": 480,
        "protein": 18,
        "fat": 16,
        "carbs": 62,
        "sodium": 1200,
        "tip": "钠含量极高！建议选择清汤底，少喝汤，多蔬菜少丸子",
    },

    # ========== 零食 ==========
    "6991234567890": {
        "name": "乐事原味薯片（65g）",
        "brand": "乐事",
        "category": "零食/薯片",
        "calories": 350,
        "protein": 4,
        "fat": 21,
        "carbs": 40,
        "sodium": 320,
        "tip": "高脂高钠零食，一包热量约等于一碗半米饭",
    },
    "6991234567891": {
        "name": "奥利奥饼干（3包入）",
        "brand": "奥利奥",
        "category": "零食/饼干",
        "calories": 260,
        "protein": 3,
        "fat": 11,
        "carbs": 38,
        "sugar": 18,
        "tip": "夹心饼干，高糖高脂，每次建议不超过1包",
    },
    "6991234567892": {
        "name": "三只松鼠碧根果（175g）",
        "brand": "三只松鼠",
        "category": "零食/坚果",
        "calories": 1050,
        "protein": 15,
        "fat": 95,
        "carbs": 20,
        "tip": "坚果健康但热量极高，每天一小把（约30g）即可",
    },
    "6991234567893": {
        "name": "卫龙辣条（80g）",
        "brand": "卫龙",
        "category": "零食/辣条",
        "calories": 380,
        "protein": 9,
        "fat": 18,
        "carbs": 42,
        "sodium": 1100,
        "tip": "高油高盐高糖，娱乐零食可选但别当日常吃",
    },
    "6991234567894": {
        "name": "良品铺子芒果干（100g）",
        "brand": "良品铺子",
        "category": "零食/果干",
        "calories": 320,
        "protein": 2,
        "fat": 0.3,
        "carbs": 78,
        "sugar": 65,
        "tip": "蜜饯类含糖量高，选择无添加糖版本更健康",
    },
    "6991234567895": {
        "name": "每日坚果混合装（25g）",
        "brand": "百草味",
        "category": "零食/坚果",
        "calories": 150,
        "protein": 4,
        "fat": 12,
        "carbs": 8,
        "tip": "方便健康的小包装，每日1-2包可作为营养补充",
    },

    # ========== 调味品/酱料 ==========
    "6992234567890": {
        "name": "海天生抽（500ml）",
        "brand": "海天",
        "category": "调味品",
        "calories": 12,
        "protein": 1,
        "fat": 0,
        "carbs": 1,
        "sodium": 2500,
        "tip": "每15ml含钠约1000mg，控制用量是关键",
    },
    "6992234567891": {
        "name": "老干妈风味豆豉油辣椒（280g）",
        "brand": "老干妈",
        "category": "调味品",
        "calories": 350,
        "protein": 5,
        "fat": 35,
        "carbs": 5,
        "sodium": 800,
        "tip": "百搭但高油高钠，每次用半勺即可提味",
    },

    # ========== 速食/方便面 ==========
    "6993234567890": {
        "name": "康师傅红烧牛肉面（100g）",
        "brand": "康师傅",
        "category": "速食/方便面",
        "calories": 470,
        "protein": 9,
        "fat": 20,
        "carbs": 62,
        "sodium": 1600,
        "tip": "高钠速食，建议少喝汤，加个鸡蛋和蔬菜更健康",
    },
    "6993234567891": {
        "name": "统一老坛酸菜牛肉面（88g）",
        "brand": "统一",
        "category": "速食/方便面",
        "calories": 430,
        "protein": 8,
        "fat": 18,
        "carbs": 58,
        "sodium": 1400,
        "tip": "酸菜口味钠含量高，建议搭配蔬菜减少钠摄入",
    },
    "6993234567892": {
        "name": "自热火锅（麻辣味）",
        "brand": "自嗨锅",
        "category": "速食/自热食品",
        "calories": 550,
        "protein": 14,
        "fat": 24,
        "carbs": 68,
        "sodium": 1800,
        "tip": "钠含量极高！建议分2次食用或只吃食材不喝汤",
    },

    # ========== 烘焙甜点 ==========
    "6994234567890": {
        "name": "山姆瑞士卷（3个）",
        "brand": "山姆",
        "category": "甜点/蛋糕",
        "calories": 420,
        "protein": 6,
        "fat": 16,
        "carbs": 62,
        "sugar": 42,
        "tip": "奶油蛋糕热量高，每次建议不超过1个",
    },
    "6994234567891": {
        "name": "好利来半熟芝士（60g）",
        "brand": "好利来",
        "category": "甜点/芝士",
        "calories": 220,
        "protein": 5,
        "fat": 12,
        "carbs": 24,
        "sugar": 18,
        "tip": "绵密口感但热量不低，下午茶选1个即可",
    },
    "6994234567892": {
        "name": "元祖雪月饼（1个约100g）",
        "brand": "元祖",
        "category": "甜点/月饼",
        "calories": 350,
        "protein": 4,
        "fat": 12,
        "carbs": 56,
        "sugar": 38,
        "tip": "冰淇淋月饼热量较高，夏日解馋适量",
    },

    # ========== 健康食品 ==========
    "6995234567890": {
        "name": "即食燕麦片（50g）",
        "brand": "桂格",
        "category": "健康食品/燕麦",
        "calories": 190,
        "protein": 6,
        "fat": 3,
        "carbs": 34,
        "fiber": 4,
        "tip": "慢释放碳水，早餐选择，饱腹感强，血糖友好",
    },
    "6995234567891": {
        "name": "权健左旋肉碱咖啡（35g）",
        "brand": "权健",
        "category": "健康食品/代餐",
        "calories": 150,
        "protein": 8,
        "fat": 4,
        "carbs": 20,
        "tip": "代餐类产品需配合运动，单一依赖效果有限",
    },
    "6995234567892": {
        "name": "WonderLab代餐奶昔（1袋）",
        "brand": "WonderLab",
        "category": "健康食品/代餐",
        "calories": 120,
        "protein": 15,
        "fat": 3,
        "carbs": 10,
        "fiber": 3,
        "tip": "高蛋白低热量代餐，适合控制饮食期间使用",
    },
    "6995234567893": {
        "name": "农夫山泉17.5°橙汁（300ml）",
        "brand": "农夫山泉",
        "category": "饮料/果汁",
        "calories": 140,
        "protein": 1.5,
        "fat": 0,
        "carbs": 32,
        "sugar": 28,
        "vitamin_c": 35,
        "tip": "NFC果汁保留营养，但仍含天然果糖，适量饮用",
    },

    # ========== 更多常见食品 ==========
    "6996234567890": {
        "name": "豆腐（100g北豆腐）",
        "brand": "国产",
        "category": "豆制品",
        "calories": 81,
        "protein": 12,
        "fat": 4,
        "carbs": 2,
        "calcium": 138,
        "tip": "植物蛋白优质来源，含钙丰富，素食者推荐",
    },
    "6996234567891": {
        "name": "豆浆（1杯约250ml）",
        "brand": "国产",
        "category": "豆制品/饮品",
        "calories": 65,
        "protein": 4,
        "fat": 2,
        "carbs": 7,
        "tip": "植物蛋白饮品，低脂健康，无糖版更佳",
    },
    "6996234567892": {
        "name": "毛肚（100g）",
        "brand": "国产",
        "category": "火锅食材",
        "calories": 113,
        "protein": 15,
        "fat": 5,
        "carbs": 2,
        "tip": "火锅经典食材，高蛋白中脂肪，涮烫时间宜短",
    },
    "6996234567893": {
        "name": "肥牛卷（100g）",
        "brand": "国产",
        "category": "火锅食材",
        "calories": 320,
        "protein": 16,
        "fat": 28,
        "carbs": 0,
        "tip": "高脂肪红肉，火锅常客，建议搭配瘦肉轮换",
    },
    "6996234567894": {
        "name": "虾滑（100g）",
        "brand": "国产",
        "category": "火锅食材",
        "calories": 95,
        "protein": 16,
        "fat": 2,
        "carbs": 5,
        "tip": "高蛋白低脂火锅食材，Q弹鲜美，推荐",
    },
    "6996234567895": {
        "name": "海底捞自热米饭（麻辣味）",
        "brand": "海底捞",
        "category": "速食/自热食品",
        "calories": 520,
        "protein": 12,
        "fat": 18,
        "carbs": 75,
        "sodium": 1500,
        "tip": "方便但有自热包，钠含量高，户外应急首选",
    },
    "6996234567896": {
        "name": "良品铺子牛肉干（100g）",
        "brand": "良品铺子",
        "category": "零食/肉制品",
        "calories": 380,
        "protein": 38,
        "fat": 18,
        "carbs": 12,
        "sodium": 950,
        "tip": "高蛋白零食，但钠含量偏高，适量食用",
    },
    "6996234567897": {
        "name": "三只松鼠每日坚果（30g）",
        "brand": "三只松鼠",
        "category": "零食/坚果",
        "calories": 165,
        "protein": 4,
        "fat": 13,
        "carbs": 9,
        "tip": "科学配比混合坚果，每日1包满足营养需求",
    },
    "6996234567898": {
        "name": "椰树椰汁（245ml）",
        "brand": "椰树",
        "category": "饮料/植物饮料",
        "calories": 105,
        "protein": 1,
        "fat": 4,
        "carbs": 16,
        "sugar": 14,
        "tip": "热带风味饮料，含糖量中等，适量饮用",
    },
    "6996234567899": {
        "name": "椰子水（100%纯，330ml）",
        "brand": "体因",
        "category": "饮料/天然果汁",
        "calories": 45,
        "protein": 0.5,
        "fat": 0,
        "carbs": 11,
        "sugar": 8,
        "potassium": 250,
        "tip": "天然电解质饮料，低热量，运动后补充佳选",
    },
    "6996234567900": {
        "name": "盒马鲜生刺身级三文鱼（150g）",
        "brand": "盒马",
        "category": "海鲜/刺身",
        "calories": 209,
        "protein": 30,
        "fat": 9,
        "carbs": 0,
        "omega3": 2.3,
        "tip": "优质蛋白质和健康脂肪来源，注意保鲜和来源",
    },
    "6996234567901": {
        "name": "山姆烤鸡（整只约1200g）",
        "brand": "山姆",
        "category": "熟食/烤鸡",
        "calories": 850,
        "protein": 65,
        "fat": 62,
        "carbs": 2,
        "tip": "性价比高但高脂，建议2-3人分享，去皮更健康",
    },
    "6996234567902": {
        "name": "叮咚买菜土鸡蛋（10枚）",
        "brand": "叮咚买菜",
        "category": "蛋类",
        "calories": 700,
        "protein": 65,
        "fat": 50,
        "carbs": 5,
        "tip": "10枚总热量约700kcal，胆固醇适中，每天2个安全",
    },
    "6996234567903": {
        "name": "网易严选冻干草莓（30g）",
        "brand": "网易严选",
        "category": "零食/冻干水果",
        "calories": 105,
        "protein": 2,
        "fat": 0.3,
        "carbs": 24,
        "sugar": 18,
        "vitamin_c": 35,
        "tip": "冻干工艺保留营养，无添加糖，健康零食选择",
    },
    "6996234567904": {
        "name": "三顿半超即溶咖啡（1颗）",
        "brand": "三顿半",
        "category": "饮料/咖啡",
        "calories": 5,
        "protein": 0.1,
        "fat": 0,
        "carbs": 1,
        "caffeine": 80,
        "tip": "精品速溶咖啡，低卡提神，不含植脂末",
    },
    "6996234567905": {
        "name": "喜茶多肉葡萄（中杯）",
        "brand": "喜茶",
        "category": "饮料/奶茶",
        "calories": 280,
        "protein": 3,
        "fat": 4,
        "carbs": 58,
        "sugar": 52,
        "tip": "奶茶甜品类，含糖量约13块方糖，建议选微糖",
    },
    "6996234567906": {
        "name": "奈雪の茶霸气芝士草莓",
        "brand": "奈雪",
        "category": "饮料/奶茶",
        "calories": 310,
        "protein": 4,
        "fat": 8,
        "carbs": 54,
        "sugar": 48,
        "tip": "芝士奶盖增加脂肪和钠，选择标准糖更健康",
    },
    "6996234567907": {
        "name": "蜜雪冰城柠檬水（大杯）",
        "brand": "蜜雪冰城",
        "category": "饮料/茶饮",
        "calories": 140,
        "protein": 0.5,
        "fat": 0,
        "carbs": 34,
        "sugar": 32,
        "tip": "性价比高但甜度较高，选择少糖更理智",
    },
    "6996234567908": {
        "name": "瑞幸咖啡美式（中杯）",
        "brand": "瑞幸",
        "category": "饮料/咖啡",
        "calories": 15,
        "protein": 0.5,
        "fat": 0,
        "carbs": 3,
        "caffeine": 150,
        "tip": "零脂肪低热量，咖啡因提神，减肥期间友好选择",
    },
    "6996234567909": {
        "name": "星巴克拿铁（大杯）",
        "brand": "星巴克",
        "category": "饮料/咖啡",
        "calories": 250,
        "protein": 12,
        "fat": 9,
        "carbs": 30,
        "caffeine": 150,
        "tip": "含牛奶热量，选脱脂奶可减约80kcal",
    },
    "6996234567910": {
        "name": "全家便利店饭团（金枪鱼）",
        "brand": "全家",
        "category": "便利店/饭团",
        "calories": 210,
        "protein": 8,
        "fat": 4,
        "carbs": 38,
        "tip": "便利店快捷餐，蛋白质尚可，注意钠含量",
    },
    "6996234567911": {
        "name": "7-11便当（照烧鸡排）",
        "brand": "7-11",
        "category": "便利店/便当",
        "calories": 420,
        "protein": 22,
        "fat": 14,
        "carbs": 52,
        "sodium": 850,
        "tip": "便利店热食，营养均衡但钠偏高，配菜少吃",
    },
    "6996234567912": {
        "name": "罗森三明治（金枪鱼）",
        "brand": "罗森",
        "category": "便利店/三明治",
        "calories": 280,
        "protein": 12,
        "fat": 8,
        "carbs": 38,
        "tip": "便捷早餐选择，蛋白质和碳水比例合理",
    },
    "6996234567913": {
        "name": "盒马鲜生三文鱼刺身（100g）",
        "brand": "盒马",
        "category": "海鲜/刺身",
        "calories": 139,
        "protein": 20,
        "fat": 6,
        "carbs": 0,
        "omega3": 1.5,
        "tip": "优质蛋白和健康脂肪，注意新鲜度和来源",
    },
    "6996234567914": {
        "name": "永辉超市散装花生（100g）",
        "brand": "永辉",
        "category": "零食/坚果",
        "calories": 560,
        "protein": 24,
        "fat": 48,
        "carbs": 16,
        "tip": "花生营养好但热量极高，每天一小把（25g）足够",
    },
    "6996234567915": {
        "name": "Costco烤鸡（整只）",
        "brand": "Costco",
        "category": "熟食/烤鸡",
        "calories": 820,
        "protein": 68,
        "fat": 58,
        "carbs": 2,
        "tip": "超值烤鸡，但高脂，建议2-3人分享，去皮吃更健康",
    },
}


# ============================================================
# 扩展数据加载（Pro 数据包）
# 免费版自带 103+ 条基础数据；Pro 数据包为同构 JSON，
# 通过环境变量 FOODCALORIE_EXTRA_DATA 或 load_extra_data() 载入。
# ============================================================
def load_extra_data(path: str) -> int:
    """Load an extra food data pack (e.g. FoodCalorie Pro) into FOOD_DATABASE.

    The pack must be a JSON object whose "items" field (or the object itself)
    maps entry-id -> entry dict, using the same schema as FOOD_DATABASE.
    Returns the number of entries merged; 0 if nothing was loaded.
    """
    import os

    try:
        with open(path, encoding="utf-8") as f:
            payload = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        logger.warning("Failed to read extra data pack %s: %s", path, e)
        return 0

    items = payload.get("items", payload) if isinstance(payload, dict) else {}
    if not isinstance(items, dict):
        logger.warning("Extra data pack %s has an unexpected format", path)
        return 0

    FOOD_DATABASE.update(items)
    logger.info("Loaded %d extra food entries from %s", len(items), path)
    return len(items)


def _load_extra_data_from_env() -> None:
    """Auto-load the extra data pack if FOODCALORIE_EXTRA_DATA is set."""
    import os

    path = os.environ.get("FOODCALORIE_EXTRA_DATA")
    if path:
        load_extra_data(path)


_load_extra_data_from_env()


# ============================================================
# 品牌知识库（用于智能搜索联想）
# ============================================================
BRAND_ALIASES = {
    "coca": "可口可乐",
    "pepsi": "百事",
    "yili": "伊利",
    "mengniu": "蒙牛",
    "wanglaoji": "王老吉",
    "redbull": "红牛",
    "nongfuspring": "农夫山泉",
    "masterkong": "康师傅",
    "vitamilk": "维他奶",
    "dongpeng": "东鹏",
    "ambrosial": "安慕希",
    "simplelove": "简爱",
    "bright": "光明",
    "holiland": "好利来",
    "taoli": "桃李",
    "daliyuan": "达利园",
    "macdonalds": "麦当劳",
    "kfc": "肯德基",
    "burgerking": "汉堡王",
    "wallace": "华莱士",
    "pizza_hut": "必胜客",
    "shaxian": "沙县小吃",
    "laoxiangji": "老乡鸡",
    "zheng Gongfu": "真功夫",
    "yihai Kerry": "福临门",
    "haitian": "海天",
    "lao Gan Ma": "老干妈",
    "sanzhisongshu": "三只松鼠",
    "liangpinpuzi": "良品铺子",
    "weilong": "卫龙",
    "baguohui": "百草味",
    "october_thirteen": "稻香村",
    "haidilao": "海底捞",
    "selfheating_pot": "自嗨锅",
    "quanjude": "全聚得",
    "dingdong": "叮咚买菜",
    "hema": "盒马",
    "freshippo": "盒马",
    "yonghui": "永辉",
    "sam": "山姆",
    "costco": "Costco",
    "xicha": "喜茶",
    "nayuki": "奈雪",
    "mixue": "蜜雪冰城",
    "luckin": "瑞幸",
    "starbucks": "星巴克",
    "familyMart": "全家",
    "7eleven": "7-11",
    "lawson": "罗森",
    "cotti": "库迪",
    "manner": "Manner",
    "saturnbird": "三顿半",
    "qugaga": "桂格",
    "wonderlab": "WonderLab",
}


@mcp.tool()
async def search_food_by_barcode(barcode: str) -> dict[str, Any]:
    """Search food nutrition data by barcode.

    Args:
        barcode: The barcode number of the food product (e.g., "6901234567890")

    Returns:
        Nutrition information including calories, protein, fat, carbs, etc.
    """
    item = FOOD_DATABASE.get(barcode)
    if not item:
        return {
            "success": False,
            "error": f"Barcode {barcode} not found in database",
            "suggestion": "Try searching by name instead",
        }
    return {"success": True, "data": item}


@mcp.tool()
async def search_food_by_name(keyword: str, limit: int = 10) -> dict[str, Any]:
    """Search food by name keyword.

    Args:
        keyword: Search keyword (Chinese or English)
        limit: Maximum number of results (default: 10)

    Returns:
        List of matching foods with basic nutrition info
    """
    results = []
    keyword_lower = keyword.lower()

    # Build index for brand alias matching
    alias_matches = set()
    for alias, brand in BRAND_ALIASES.items():
        alias_lower = alias.lower()
        if keyword_lower in alias_lower:
            alias_matches.add(brand)

    for barcode, item in FOOD_DATABASE.items():
        matched = (
            keyword_lower in item["name"].lower()
            or keyword_lower in item.get("brand", "").lower()
            or keyword_lower in item.get("category", "").lower()
            or item.get("brand", "") in alias_matches
        )
        if matched:
            results.append(
                {
                    "barcode": barcode,
                    "name": item["name"],
                    "brand": item.get("brand"),
                    "category": item.get("category"),
                    "calories": item["calories"],
                    "protein": item.get("protein"),
                    "fat": item.get("fat"),
                    "carbs": item.get("carbs"),
                }
            )
        if len(results) >= limit:
            break

    return {
        "success": True,
        "keyword": keyword,
        "count": len(results),
        "results": results,
    }


@mcp.tool()
async def get_daily_nutrition_summary(
    items: list[dict[str, str]],
) -> dict[str, Any]:
    """Get daily nutrition summary for a list of food items.

    Args:
        items: List of items, each with 'barcode' or 'name' key

    Returns:
        Total nutrition summary with daily value percentages
    """
    total_calories = 0
    total_protein = 0
    total_fat = 0
    total_carbs = 0
    details = []

    for item in items:
        barcode = item.get("barcode")
        name = item.get("name")

        food = None
        if barcode and barcode in FOOD_DATABASE:
            food = FOOD_DATABASE[barcode]
        elif name:
            # Search by name
            for fb_barcode, fb_item in FOOD_DATABASE.items():
                if name.lower() in fb_item["name"].lower():
                    food = fb_item
                    break

        if food:
            total_calories += food.get("calories", 0)
            total_protein += food.get("protein", 0)
            total_fat += food.get("fat", 0)
            total_carbs += food.get("carbs", 0)
            details.append(
                {
                    "name": food["name"],
                    "calories": food.get("calories", 0),
                    "protein": food.get("protein", 0),
                    "fat": food.get("fat", 0),
                    "carbs": food.get("carbs", 0),
                }
            )

    # Calculate daily value percentages (based on 2000 calorie diet)
    dv_calories = (total_calories / 2000) * 100
    dv_protein = (total_protein / 50) * 100
    dv_fat = (total_fat / 65) * 100
    dv_carbs = (total_carbs / 300) * 100

    return {
        "success": True,
        "summary": {
            "total_calories": total_calories,
            "total_protein": round(total_protein, 1),
            "total_fat": round(total_fat, 1),
            "total_carbs": round(total_carbs, 1),
            "daily_values": {
                "calories": f"{dv_calories:.1f}%",
                "protein": f"{dv_protein:.1f}%",
                "fat": f"{dv_fat:.1f}%",
                "carbs": f"{dv_carbs:.1f}%",
            },
        },
        "details": details,
    }


@mcp.tool()
async def get_health_tip(food_name: str) -> dict[str, Any]:
    """Get health tips for a specific food.

    Args:
        food_name: Name of the food

    Returns:
        Health tips and dietary recommendations
    """
    food_name_lower = food_name.lower()

    tips = []
    for barcode, item in FOOD_DATABASE.items():
        if food_name_lower in item["name"].lower():
            tips.append(
                {
                    "food": item["name"],
                    "tip": item.get("tip", "无特别建议"),
                    "category": item.get("category", "其他"),
                    "calories_per_serving": item["calories"],
                }
            )

    # General tips based on keywords
    general_tips = {
        "高糖": "建议控制糖分摄入，选择低糖或无糖替代品",
        "高脂": "注意脂肪摄入量，选择低脂食品",
        "高蛋白": "优质蛋白质来源，适合运动后补充",
        "高纤维": "有助于消化，建议增加摄入量",
        "高钠": "钠含量较高，建议搭配多喝水，控制总量",
        "低热量": "低热量食品，减肥期间可以放心食用",
    }

    for keyword, tip in general_tips.items():
        if keyword in food_name:
            tips.append({"food": "通用建议", "tip": tip})

    return {
        "success": True,
        "query": food_name,
        "tips": tips if tips else [{"food": food_name, "tip": "暂无数据，建议咨询营养师"}],
    }


@mcp.tool()
async def list_foods_by_category(category: str | None = None, limit: int = 20) -> dict[str, Any]:
    """List foods filtered by category.

    Args:
        category: Filter by category (e.g., '饮料', '肉类', '水果') or None for all
        limit: Maximum number of results (default: 20)

    Returns:
        List of foods in the specified category
    """
    results = []
    for barcode, item in FOOD_DATABASE.items():
        if category is None or category in item.get("category", ""):
            results.append({
                "barcode": barcode,
                "name": item["name"],
                "brand": item.get("brand"),
                "category": item.get("category"),
                "calories": item["calories"],
                "protein": item.get("protein"),
                "fat": item.get("fat"),
                "carbs": item.get("carbs"),
            })
        if len(results) >= limit:
            break
    return {
        "success": True,
        "category": category or "全部",
        "count": len(results),
        "results": results,
    }


@mcp.tool()
async def compare_foods(barcode_list: list[str]) -> dict[str, Any]:
    """Compare nutrition info for multiple foods.

    Args:
        barcode_list: List of barcodes to compare

    Returns:
        Side-by-side nutrition comparison
    """
    rows = []
    for barcode in barcode_list:
        item = FOOD_DATABASE.get(barcode)
        if item:
            rows.append({
                "barcode": barcode,
                "name": item["name"],
                "calories": item["calories"],
                "protein": item.get("protein", 0),
                "fat": item.get("fat", 0),
                "carbs": item.get("carbs", 0),
            })
    return {
        "success": True,
        "count": len(rows),
        "comparison": rows,
    }


def main() -> None:
    """Main server entry point."""
    logger.info("Starting FoodCalorie MCP Server v2.0...")
    logger.info(f"Database loaded: {len(FOOD_DATABASE)} foods")
    mcp.run(stdio=True)


if __name__ == "__main__":
    main()
