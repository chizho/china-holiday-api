"""
生成生产环境 OpenAPI 文档（中文 + 英文两份）
过滤：去掉 /health 和 /holiday/refresh
"""
import json, copy

from app.main import create_app

app = create_app()
schema = app.openapi()

# -- 过滤掉非生产接口
EXCLUDE_PATHS = ["/health", "/public-china-holiday/holiday/refresh"]
schema["paths"] = {
    k: v for k, v in schema["paths"].items() if k not in EXCLUDE_PATHS
}


# ============================================================
# 中文版（原样保留）
# ============================================================
zh_schema = copy.deepcopy(schema)
zh_schema["info"]["title"] = "China Date Toolkit API"
zh_schema["info"]["description"] = (
    "中国日期工具包接口服务，提供法定假日、农历、生肖、黄历、工作日、节气等查询。\n\n"
    "## 功能模块\n"
    "- **日期查询**：农历转换、生肖、星座、天干地支、黄历、节气\n"
    "- **假日查询**：法定假日、调休安排\n"
    "- **工作日计算**：判断、推算、计数\n"
    "- **节气查询**：二十四节气列表\n\n"
    "## 鉴权\n"
    "生产环境需在请求头携带 `X-RapidAPI-Proxy-Secret` 进行身份验证。\n\n"
    "## 多语言\n"
    "所有接口支持 `lang` 参数（zh/en/ja/ko/vi/es/fr/de），默认 zh。"
)

with open("public-china-holiday-zh.json", "w", encoding="utf-8") as f:
    json.dump(zh_schema, f, ensure_ascii=False, indent=2)
print("[OK] public-china-holiday-zh.json")


# ============================================================
# 英文版 — 翻译所有 description / summary / field description
# ============================================================

en_schema = copy.deepcopy(schema)

# -- info
en_schema["info"]["title"] = "China Date Toolkit API"
en_schema["info"]["description"] = (
    "China Date Toolkit API — Provides queries for Chinese public holidays, "
    "lunar calendar, Chinese zodiac, Tung Shing (almanac), workday calculations, "
    "and 24 solar terms.\n\n"
    "## Features\n"
    "- **Date Query**: Lunar conversion, zodiac, constellation, Heavenly Stems & Earthly Branches, almanac, solar terms\n"
    "- **Holiday Query**: Statutory holidays and adjusted workday schedules\n"
    "- **Workday**: Check, calculate, and count working days\n"
    "- **Solar Terms**: List of 24 solar terms for a given year\n\n"
    "## Authentication\n"
    "Production requests require `X-RapidAPI-Proxy-Secret` header.\n\n"
    "## Internationalization\n"
    "All endpoints support `lang` parameter (zh/en/ja/ko/vi/es/fr/de), default is zh."
)

# -- 翻译映射表
I18N_PATHS = {
    "/public-china-holiday/date": {
        "summary": "Comprehensive Date Query",
        "description": (
            "Returns comprehensive Chinese calendar information for a given date, "
            "including lunar date, zodiac, constellation, Heavenly Stems & Earthly Branches, "
            "Tung Shing almanac, and solar terms. Supports lang parameter for output language. "
            "For deep cultural terms, non-zh responses use translated or pinyin main fields and include *_py pinyin fields for reference."

        ),
    },
    "/public-china-holiday/holiday/query": {
        "summary": "Query Holiday Info by Date",
        "description": (
            "Returns whether the given date is a public holiday, holiday name, and adjusted workday info. "
            "Supports lang parameter for output language."
        ),
    },
    "/public-china-holiday/holiday/list": {
        "summary": "List Holidays by Year",
        "description": (
            "Returns all statutory holidays and adjusted workday arrangements for the given year. "
            "Supports lang parameter for output language."
        ),
    },
    "/public-china-holiday/workday": {
        "summary": "Check Workday",
        "description": (
            "Returns whether the given date is a working day and the reason "
            "(e.g., public holiday, weekend, adjusted workday). "
            "Supports lang parameter for output language."
        ),
    },
    "/public-china-holiday/workday/calculate": {
        "summary": "Workday Calculation",
        "description": (
            "Two modes: ① Pass workdays to calculate a target date. ② Pass end_date to count working days. "
            "Supports lang parameter for output language."
        ),
    },
    "/public-china-holiday/solar-term/list": {
        "summary": "List 24 Solar Terms by Year",
        "description": (
            "Returns all 24 solar terms for the given year with name, date, and type (Jie or Qi). "
            "Supports lang parameter for output language."
        ),
    },
    "/public-china-holiday/solar-term/current": {
        "summary": "Query Current Solar Term",
        "description": (
            "Returns the previous and next solar terms for the given date, and whether the date itself is a solar term. "
            "Supports lang parameter for output language."
        ),
    },
}

# -- 翻译参数描述
I18N_PARAMS = {
    "date": "Gregorian date in YYYY-MM-DD format, e.g. 2025-10-01",
    "lang": "Output language: zh/en/ja/ko/vi/es/fr/de",
    "year": "Year, e.g. 2025",
    "start_date": "Start date in YYYY-MM-DD format",
    "workdays": "Mode 1: Number of working days to add (positive=future, negative=past)",
    "end_date": "Mode 2: End date in YYYY-MM-DD format",
}

# -- 翻译 tag
I18N_TAGS = {
    "日期查询 Date": "Date",
    "假日 Holiday": "Holiday",
    "工作日 Workday": "Workday",
    "节气 Solar Term": "Solar Term",
}

# -- 中文 → 英文 description 映射（按 description 原文精确匹配）
DESC_ZH_TO_EN = {
    # AlmanacDetail
    "宜": "Auspicious activities",
    "忌": "Inauspicious activities",
    "冲天干": "Clashing Heavenly Stem",
    "冲地支": "Clashing Earthly Branch",
    "冲生肖": "Clashing Chinese Zodiac",
    "冲描述，如 (丁酉)鸡": "Clash description, e.g. (Dingyou) Rooster",
    "煞方": "Sha direction (inauspicious direction)",
    "胎神占方": "Fetal God position",
    "五行纳音": "Five Elements Nayin",
    "彭祖百忌": "Pengzu's taboos",
    "吉神": "Auspicious deities",
    "凶煞": "Inauspicious spirits",
    "建除十二值星": "Zhi Xing (one of the 12 Build-Remove stars)",
    "值日天神": "Day deity",
    "天神类型": "Deity type (Yellow Path / Dark Path)",
    "财神方位": "Wealth God direction",
    "喜神方位": "Happiness God direction",
    "福神方位": "Fortune God direction",
    "阳贵方位": "Yang Noble direction",
    "阴贵方位": "Yin Noble direction",
    "六曜": "Liu Yao (six luminaries)",
    "七十二候": "72 Pentads",
    "二十八星宿": "28 Mansions",
    "星宿吉凶": "Mansion luck (auspicious/inauspicious)",
    # GanZhiDetail
    "干支，如 乙巳": "Gan-Zhi, e.g. Yi-Si",
    "天干，如 乙": "Heavenly Stem, e.g. Yi",
    "地支，如 巳": "Earthly Branch, e.g. Si",
    "纳音，如 佛灯火": "Nayin, e.g. Fo Deng Huo (Buddha Lamp Fire)",
    # XingzuoDetail
    "星座中文名，如 天秤座": "Constellation name in Chinese, e.g. 天秤座",
    "星座英文名，如 Libra": "Constellation name in English, e.g. Libra",
    "日期范围，如 9.23-10.23": "Date range, e.g. 9.23-10.23",
    "元素，如 风象": "Element, e.g. Air",
    "守护星，如 金星": "Ruling planet, e.g. Venus",
    # DateInfoResponse
    "公历年": "Gregorian year",
    "公历月": "Gregorian month",
    "公历日": "Gregorian day",
    "农历年": "Lunar year",
    "农历月": "Lunar month",
    "农历日": "Lunar day",
    "农历月中文，如 八月": "Lunar month in Chinese, e.g. 八月",
    "农历日中文，如 初九": "Lunar day in Chinese, e.g. 初九",
    "农历日期中文，如 乙巳年八月初九": "Lunar date in Chinese, e.g. 乙巳年八月初九",
    "生肖，如 蛇": "Chinese zodiac animal, e.g. Snake",
    "生肖 emoji": "Zodiac emoji",
    "年柱干支": "Year pillar Gan-Zhi",
    "月柱干支": "Month pillar Gan-Zhi",
    "日柱干支": "Day pillar Gan-Zhi",
    "黄历信息": "Tung Shing almanac info",
    "前一节气": "Previous solar term",
    "后一节气": "Next solar term",
    "当天节气": "Current solar term (null if not a solar term day)",
    # SolarTermItem
    "节气名称，如 小寒": "Solar term name, e.g. 小寒",
    "节气日期，如 2025-01-05": "Solar term date, e.g. 2025-01-05",
    "是否为「节」": "Whether it is a 'Jie' (major term)",
    # HolidayInfo
    "日期，YYYY-MM-DD": "Date in YYYY-MM-DD format",
    "是否为法定假日": "Whether it is a public holiday",
    "是否为工作日（调休上班日也算工作日）": "Whether it is a working day (adjusted workdays count)",
    "假日名称或'工作日'": "Holiday name or description",
    # HolidayListResponse
    "假日总数": "Total number of holidays",
    "查询年份": "Query year",
    "查询月份（全年查询时为 null）": "Query month (null for full year)",
    "假日列表": "Holiday list",
    # HolidayListItem
    "假日名称": "Holiday name",
    # WorkdayCheckResponse
    "查询日期": "Query date",
    "是否为工作日": "Whether it is a working day",
    "原因说明": "Reason description",
    # WorkdayCalcResponse
    "起始日期": "Start date",
    "结束日期（add 模式为 result_date）": "End date (result_date in add mode)",
    "工作日数量": "Number of working days",
    "总天数（count 模式）": "Total days (count mode)",
    # SolarTermListResponse
    "节气列表，按日期排序": "Solar terms sorted by date",
    # ApiResponse
    "状态码，200=成功": "Status code, 200=success",
    "响应消息": "Response message",
    "响应数据": "Response data",
    "Pinyin field, available in all languages": "Pinyin field, available in all languages",
    "Pinyin list, available in all languages": "Pinyin list, available in all languages",
}


# -- Schema title/description 翻译
TITLE_ZH_TO_EN = {
    "黄历详细信息": "Tung Shing Almanac Details",
    "天干地支详细信息（年月日柱）": "Gan-Zhi (Heavenly Stems & Earthly Branches) Details",
    "星座详细信息": "Constellation Details",
    "日期综合查询响应（合并 5 个旧接口）": "Comprehensive Date Query Response",
    "单个节气": "Solar Term Item",
    "工作日判断响应": "Workday Check Response",
    "工作日计算响应（合并 add + count）": "Workday Calculation Response",
    "节气列表响应": "Solar Term List Response",
    "当前节气信息响应": "Current Solar Term Response",
    "单日假日信息响应": "Holiday Info Response",
    "假日列表项": "Holiday List Item",
    "假日列表响应": "Holiday List Response",
}


def translate_schema(obj):
    """递归翻译 schema 对象中的 title / description"""
    if isinstance(obj, dict):
        # 翻译 title
        if "title" in obj and isinstance(obj["title"], str):
            t = TITLE_ZH_TO_EN.get(obj["title"])
            if t:
                obj["title"] = t
        # 翻译 description
        if "description" in obj and isinstance(obj["description"], str):
            d = DESC_ZH_TO_EN.get(obj["description"])
            if d:
                obj["description"] = d
        for v in obj.values():
            translate_schema(v)
    elif isinstance(obj, list):
        for item in obj:
            translate_schema(item)


# -- 翻译 paths
for path, methods in en_schema["paths"].items():
    for method, detail in methods.items():
        if path in I18N_PATHS:
            detail["summary"] = I18N_PATHS[path]["summary"]
            detail["description"] = I18N_PATHS[path]["description"]
        # 翻译 tag
        detail["tags"] = [
            I18N_TAGS.get(t, t) for t in detail.get("tags", [])
        ]
        # 翻译参数
        for param in detail.get("parameters", []):
            pname = param.get("name", "")
            if pname in I18N_PARAMS:
                param["description"] = I18N_PARAMS[pname]

# -- 翻译 components/schemas
translate_schema(en_schema.get("components", {}))

with open("public-china-holiday-en.json", "w", encoding="utf-8") as f:
    json.dump(en_schema, f, ensure_ascii=False, indent=2)
print("[OK] public-china-holiday-en.json")

# -- 输出统计
zh_paths = list(zh_schema["paths"].keys())
en_paths = list(en_schema["paths"].keys())
zh_schemas = list(zh_schema.get("components", {}).get("schemas", {}).keys())
print(f"\n接口数: {len(zh_paths)}  |  Schema数: {len(zh_schemas)}")
print(f"接口: {zh_paths}")
