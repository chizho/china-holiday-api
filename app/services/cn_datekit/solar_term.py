"""
节气模块
提供二十四节气列表查询、当前节气查询功能
依赖：lunar_python 库
注意：getJieQiTable/getPrevJieQi/getNextJieQi/getCurrentJieQi 都在 Lunar 对象上
"""
from lunar_python import Solar


def get_solar_terms(year: int) -> dict:
    """
    获取指定年份的二十四节气列表

    Args:
        year: 年份

    Returns:
        节气列表，字段与 SolarTermListResponse 模型对应
    """
    s = Solar.fromYmd(year, 1, 1)  # 创建该年1月1日公历对象
    l = s.getLunar()  # 转农历
    table = l.getJieQiTable()  # 获取节气表（key=节气名, value=Solar对象）

    terms = []
    for name, solar in sorted(table.items(), key=lambda x: x[1].toYmd()):  # 按日期排序
        # 过滤：只保留当年范围内的节气（排除跨年的前一年12月和后一年1月的节气）
        term_year = solar.getYear()
        if term_year != year:
            continue
        terms.append({
            "name": name,  # 节气名称(小寒/大寒/立春/...)
            "date": solar.toYmd(),  # 节气日期(2025-01-05)
            "is_jie": "节" in name or any(  # 是否为「节」(而非「气」)
                k in name for k in ["立", "夏", "秋", "冬", "分", "至"]
            ),
        })

    return {
        "year": year,  # 查询年份
        "terms": terms,  # 节气列表(24条)
    }


def get_current_solar_term(year: int, month: int, day: int) -> dict:
    """
    获取指定日期前后的节气信息

    Args:
        year: 公历年
        month: 公历月
        day: 公历日

    Returns:
        前一节气、后一节气、当天节气信息，字段与 SolarTermCurrentResponse 模型对应
    """
    s = Solar.fromYmd(year, month, day)  # 创建公历对象
    l = s.getLunar()  # 转农历

    prev_jq = l.getPrevJieQi()  # 前一节气(JieQi对象)
    next_jq = l.getNextJieQi()  # 后一节气(JieQi对象)
    current_jq = l.getCurrentJieQi()  # 当天节气(当天非节气则为None)

    return {
        "date": f"{year}-{month:02d}-{day:02d}",  # 查询日期
        "current": _jq_to_dict(current_jq) if current_jq else None,  # 当天节气
        "prev": _jq_to_dict(prev_jq) if prev_jq else None,  # 前一节气
        "next": _jq_to_dict(next_jq) if next_jq else None,  # 后一节气
    }


def _jq_to_dict(jieqi) -> dict:
    """
    将 JieQi 对象转为标准字典

    Args:
        jieqi: lunar_python 的 JieQi 对象

    Returns:
        节气字典，字段与 SolarTermItem 模型对应
    """
    solar = jieqi.getSolar()  # 获取节气对应的公历日期
    return {
        "name": jieqi.getName(),  # 节气名称
        "date": f"{solar.getYear()}-{solar.getMonth():02d}-{solar.getDay():02d}",  # 节气日期
        "is_jie": jieqi.isJie(),  # 是否为「节」(True) 或「气」(False)
    }
