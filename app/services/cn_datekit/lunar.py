"""
农历转换模块
提供公历转农历、农历转公历、天干地支查询功能
依赖：lunar_python 库
"""
from lunar_python import Solar, Lunar


def get_solar_to_lunar(year: int, month: int, day: int) -> dict:
    """
    公历转农历

    Args:
        year: 公历年
        month: 公历月
        day: 公历日

    Returns:
        农历日期及附带信息字典，字段与 LunarConvertResponse 模型对应
    """
    s = Solar.fromYmd(year, month, day)  # 创建公历对象
    l = s.getLunar()  # 转农历

    return {
        # -- 公历部分
        "solar_year": year,                        # 公历年
        "solar_month": month,                      # 公历月
        "solar_day": day,                          # 公历日
        # -- 农历部分
        "lunar_year": l.getYear(),                 # 农历年
        "lunar_month": l.getMonth(),               # 农历月
        "lunar_day": l.getDay(),                   # 农历日
        "lunar_month_cn": l.getMonthInChinese(),   # 农历月中文(正月/二月/...)
        "lunar_day_cn": l.getDayInChinese(),       # 农历日中文(初一/十五/...)
        # -- 附带信息
        "shengxiao": l.getYearShengXiao(),         # 生肖(鼠/牛/虎/...)
        "xingzuo": s.getXingZuo(),         # 星座(白羊座/金牛座/...)
        "year_ganzhi": l.getYearInGanZhi(),        # 年干支(甲子/乙丑/...)
        "month_ganzhi": l.getMonthInGanZhi(),      # 月干支
        "day_ganzhi": l.getDayInGanZhi(),          # 日干支
    }


def get_lunar_to_solar(lunar_year: int, lunar_month: int, lunar_day: int) -> dict:
    """
    农历转公历

    Args:
        lunar_year: 农历年
        lunar_month: 农历月
        lunar_day: 农历日

    Returns:
        公历日期及附带信息字典，字段与 LunarConvertResponse 模型对应
    """
    l = Lunar.fromYmd(lunar_year, lunar_month, lunar_day)  # 创建农历对象
    s = l.getSolar()  # 转公历

    return {
        # -- 公历部分
        "solar_year": s.getYear(),                    # 公历年
        "solar_month": s.getMonth(),                  # 公历月
        "solar_day": s.getDay(),                      # 公历日
        # -- 农历部分
        "lunar_year": lunar_year,                     # 农历年
        "lunar_month": lunar_month,                   # 农历月
        "lunar_day": lunar_day,                       # 农历日
        "lunar_month_cn": l.getMonthInChinese(),      # 农历月中文
        "lunar_day_cn": l.getDayInChinese(),          # 农历日中文
        # -- 附带信息
        "shengxiao": l.getYearShengXiao(),            # 生肖
        "xingzuo": s.getXingZuo(),                    # 星座
        "year_ganzhi": l.getYearInGanZhi(),           # 年干支
        "month_ganzhi": l.getMonthInGanZhi(),         # 月干支
        "day_ganzhi": l.getDayInGanZhi(),             # 日干支
    }


def get_ganzhi(year: int, month: int, day: int) -> dict:
    """
    天干地支查询（年月日干支 + 五行纳音）

    Args:
        year: 公历年
        month: 公历月
        day: 公历日

    Returns:
        天干地支详细信息字典，字段与 GanZhiResponse 模型对应
    """
    s = Solar.fromYmd(year, month, day)  # 创建公历对象
    l = s.getLunar()  # 转农历

    # -- 八字对象
    bazi = l.getEightChar()  # 获取八字对象（含年月日干支、纳音等）

    return {
        # -- 年柱
        "year_ganzhi": bazi.getYear(),           # 年干支(乙巳)
        "year_gan": bazi.getYear()[0],           # 年天干(乙)
        "year_zhi": bazi.getYear()[1],           # 年地支(巳)
        "year_wuxing": bazi.getYear(),           # 年五行(干支标识)
        "year_nayin": bazi.getYearNaYin(),       # 年纳音(佛灯火)
        # -- 月柱
        "month_ganzhi": bazi.getMonth(),         # 月干支
        "month_gan": bazi.getMonth()[0],         # 月天干
        "month_zhi": bazi.getMonth()[1],         # 月地支
        # -- 日柱
        "day_ganzhi": bazi.getDay(),             # 日干支
        "day_gan": bazi.getDay()[0],             # 日天干
        "day_zhi": bazi.getDay()[1],             # 日地支
        "day_wuxing": bazi.getDay(),             # 日五行(干支标识)
        "day_nayin": bazi.getDayNaYin(),         # 日纳音
    }
