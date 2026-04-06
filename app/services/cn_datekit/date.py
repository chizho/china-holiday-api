"""
日期综合查询模块
一次调用返回完整中国历法信息：农历 + 生肖 + 星座 + 天干地支 + 黄历 + 节气
依赖：lunar_python 库
"""
from lunar_python import Solar

from app.services.cn_datekit.zodiac import get_shengxiao, get_xingzuo
from app.services.cn_datekit.solar_term import _jq_to_dict


def get_date_info(year: int, month: int, day: int) -> dict:
    """
    日期综合查询（合并原 5 个接口：solar-to-lunar / shengxiao / xingzuo / ganzhi / almanac + solar-term/current）

    Args:
        year: 公历年
        month: 公历月
        day: 公历日

    Returns:
        完整日期信息字典，字段与 DateInfoResponse 模型对应
    """
    s = Solar.fromYmd(year, month, day)  # 创建公历对象
    l = s.getLunar()  # 转农历
    bazi = l.getEightChar()  # 八字（含年月日干支、纳音）

    # -- 生肖（复用 zodiac 模块，取 emoji）
    sx = get_shengxiao(year)

    # -- 星座（复用 zodiac 模块，取详细信息）
    xz = get_xingzuo(year, month, day)

    # -- 节气（复用 solar_term 模块）
    prev_jq = l.getPrevJieQi()
    next_jq = l.getNextJieQi()
    current_jq = l.getCurrentJieQi()

    return {
        # -- 公历
        "solar_year": year,
        "solar_month": month,
        "solar_day": day,
        # -- 农历
        "lunar_year": l.getYear(),
        "lunar_month": l.getMonth(),
        "lunar_day": l.getDay(),
        "lunar_month_cn": l.getMonthInChinese(),
        "lunar_day_cn": l.getDayInChinese(),
        "lunar_date_cn": l.toString(),
        # -- 生肖
        "shengxiao": sx["shengxiao"],
        "shengxiao_emoji": sx["emoji"],
        # -- 星座
        "xingzuo": {
            "name": xz["xingzuo"],
            "name_en": xz["xingzuo_en"],
            "date_range": xz["date_range"],
            "element": xz["element"],
            "ruler": xz["ruler"],
        },
        # -- 天干地支（年月日柱）
        "year_ganzhi": _bazi_to_ganzhi(bazi, "Year"),
        "month_ganzhi": _bazi_to_ganzhi(bazi, "Month"),
        "day_ganzhi": _bazi_to_ganzhi(bazi, "Day"),
        # -- 黄历
        "almanac": {
            "yi": l.getDayYi(),
            "ji": l.getDayJi(),
            "chong_gan": l.getChongGan(),
            "chong_zhi": l.getChong(),
            "chong_shengxiao": l.getChongShengXiao(),
            "chong_desc": l.getChongDesc(),
            "sha": l.getSha(),
            "taishen": l.getDayPositionTai(),
            "wuxing_nayin": l.getDayNaYin(),
            "pengzu": f"{l.getPengZuGan()} {l.getPengZuZhi()}",
            "jishen": l.getDayJiShen(),
            "xiongsha": l.getDayXiongSha(),
            "zhixing": l.getZhiXing(),
            "tianshen": l.getDayTianShen(),
            "tianshen_type": l.getDayTianShenType(),
            "position_cai": l.getDayPositionCaiDesc(),
            "position_xi": l.getDayPositionXiDesc(),
            "position_fu": l.getDayPositionFuDesc(),
            "position_yanggui": l.getDayPositionYangGuiDesc(),
            "position_yingui": l.getDayPositionYinGuiDesc(),
            "liuyao": l.getLiuYao(),
            "wuhou": l.getWuHou(),
            "xiu": l.getXiu(),
            "xiu_luck": l.getXiuLuck(),
        },
        # -- 节气
        "solar_term_prev": _jq_to_dict(prev_jq) if prev_jq else None,
        "solar_term_next": _jq_to_dict(next_jq) if next_jq else None,
        "solar_term_current": _jq_to_dict(current_jq) if current_jq else None,
    }


def _bazi_to_ganzhi(bazi, pillar: str) -> dict:
    """
    从八字对象提取干支详情

    Args:
        bazi: EightChar 对象
        pillar: 柱名（Year/Month/Day）

    Returns:
        干支详情字典
    """
    get_ganzhi = getattr(bazi, f"get{pillar}")  # getYear / getMonth / getDay
    get_nayin = getattr(bazi, f"get{pillar}NaYin")  # getYearNaYin / getDayNaYin
    gz = get_ganzhi()

    return {
        "ganzhi": gz,       # 干支(乙巳)
        "gan": gz[0],       # 天干(乙)
        "zhi": gz[1],       # 地支(巳)
        "nayin": get_nayin() if hasattr(bazi, f"{pillar.lower()}NaYin") else get_nayin(),  # 纳音
    }
