"""
生肖星座模块
提供生肖查询、星座查询功能
依赖：lunar_python 库
"""

# -- 十二生肖顺序表（鼠开始）
SHENGXIAO_LIST = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

# -- 十二生肖 emoji 映射
SHENGXIAO_EMOJI = {
    "鼠": "🐭", "牛": "🐮", "虎": "🐯", "兔": "🐰",
    "龙": "🐲", "蛇": "🐍", "马": "🐴", "羊": "🐑",
    "猴": "🐵", "鸡": "🐔", "狗": "🐶", "猪": "🐷",
}

# -- 星座数据表：名称、英文名、日期范围、元素、守护星
XINGZUO_TABLE = [
    {"name": "白羊座", "en": "Aries", "start": (3, 21), "end": (4, 19), "element": "火象", "ruler": "火星"},
    {"name": "金牛座", "en": "Taurus", "start": (4, 20), "end": (5, 20), "element": "土象", "ruler": "金星"},
    {"name": "双子座", "en": "Gemini", "start": (5, 21), "end": (6, 21), "element": "风象", "ruler": "水星"},
    {"name": "巨蟹座", "en": "Cancer", "start": (6, 22), "end": (7, 22), "element": "水象", "ruler": "月亮"},
    {"name": "狮子座", "en": "Leo", "start": (7, 23), "end": (8, 22), "element": "火象", "ruler": "太阳"},
    {"name": "处女座", "en": "Virgo", "start": (8, 23), "end": (9, 22), "element": "土象", "ruler": "水星"},
    {"name": "天秤座", "en": "Libra", "start": (9, 23), "end": (10, 23), "element": "风象", "ruler": "金星"},
    {"name": "天蝎座", "en": "Scorpio", "start": (10, 24), "end": (11, 22), "element": "水象", "ruler": "冥王星"},
    {"name": "射手座", "en": "Sagittarius", "start": (11, 23), "end": (12, 21), "element": "火象", "ruler": "木星"},
    {"name": "摩羯座", "en": "Capricorn", "start": (12, 22), "end": (1, 19), "element": "土象", "ruler": "土星"},
    {"name": "水瓶座", "en": "Aquarius", "start": (1, 20), "end": (2, 18), "element": "风象", "ruler": "天王星"},
    {"name": "双鱼座", "en": "Pisces", "start": (2, 19), "end": (3, 20), "element": "水象", "ruler": "海王星"},
]


def get_shengxiao(year: int) -> dict:
    """
    生肖查询

    Args:
        year: 年份

    Returns:
        生肖信息字典，字段与 ShengxiaoResponse 模型对应
    """
    idx = (year - 4) % 12  # 生肖索引 = (年份-4) % 12（鼠从4年开始）
    name = SHENGXIAO_LIST[idx]  # 生肖名称

    return {
        "year": year,                          # 查询年份
        "shengxiao": name,                     # 生肖名称(蛇/马/羊/...)
        "emoji": SHENGXIAO_EMOJI.get(name, ""),  # 生肖 emoji
    }


def get_xingzuo(year: int, month: int, day: int) -> dict:
    """
    星座查询

    Args:
        year: 公历年
        month: 公历月
        day: 公历日

    Returns:
        星座信息字典，字段与 XingzuoResponse 模型对应
    """
    # -- 遍历星座表匹配日期范围
    for xz in XINGZUO_TABLE:
        start_m, start_d = xz["start"]  # 星座起始月/日
        end_m, end_d = xz["end"]  # 星座结束月/日

        if start_m <= end_m:
            # 不跨年星座：直接比较月日
            if (start_m, start_d) <= (month, day) <= (end_m, end_d):
                return _build_xingzuo(xz)
        else:
            # 跨年星座（摩羯座 12.22-1.19）：分段判断
            if (month, day) >= (start_m, start_d) or (month, day) <= (end_m, end_d):
                return _build_xingzuo(xz)

    return {"xingzuo": "未知", "xingzuo_en": "Unknown", "date_range": "", "element": "", "ruler": ""}


def _build_xingzuo(xz: dict) -> dict:
    """构建星座返回字典"""
    return {
        "xingzuo": xz["name"],            # 星座中文名(天秤座)
        "xingzuo_en": xz["en"],           # 星座英文名(Libra)
        "date_range": f"{xz['start'][0]}.{xz['start'][1]}-{xz['end'][0]}.{xz['end'][1]}",  # 日期范围(9.23-10.23)
        "element": xz["element"],         # 元素/属性(风象)
        "ruler": xz["ruler"],             # 守护星(金星)
    }
