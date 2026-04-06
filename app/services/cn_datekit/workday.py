"""
工作日模块
提供工作日判断、工作日推算、工作日计数功能
工作日定义：非周末 且 非法定假日 且 非调休假日，或调休上班日为工作日
"""
from datetime import date, timedelta

from app.services.holiday_service import get_holiday_info


def check_workday(year: int, month: int, day: int) -> dict:
    """
    判断指定日期是否为工作日

    Args:
        year: 公历年
        month: 公历月
        day: 公历日

    Returns:
        工作日判断结果，字段与 WorkdayCheckResponse 模型对应
    """
    d = date(year, month, day)
    weekday = d.weekday()  # 0=周一, 6=周日

    # -- 从假日服务获取当日信息
    info = get_holiday_info(d)
    is_holiday = info.get("is_holiday", False)  # 是否为法定假日
    is_replaced = info.get("is_replaced", False)  # 是否为调休上班日

    # -- 判断逻辑：法定假日或周末且非调休上班日 → 非工作日
    is_weekend = weekday >= 5  # 周六周日
    is_workday = is_replaced or (not is_holiday and not is_weekend)

    # -- 生成原因说明
    if is_replaced:
        reason = "调休上班"
    elif is_holiday:
        reason = f"法定假日-{info.get('name', '')}"
    elif is_weekend:
        reason = "周末"
    else:
        reason = "工作日"

    return {
        "date": f"{year}-{month:02d}-{day:02d}",  # 查询日期
        "is_workday": is_workday,  # 是否为工作日
        "reason": reason,  # 原因说明
    }


def add_workdays(year: int, month: int, day: int, workdays: int) -> dict:
    """
    从指定日期开始，增加/减少指定工作日数，返回目标日期

    Args:
        year: 起始公历年
        month: 起始公历月
        day: 起始公历日
        workdays: 要增加的工作日数量（正数向后推算，负数向前推算）

    Returns:
        推算结果，字段与 WorkdayAddResponse 模型对应
    """
    d = date(year, month, day)
    step = 1 if workdays >= 0 else -1  # 推算方向(正数向后/负数向前)
    remaining = abs(workdays)  # 剩余工作日数

    while remaining > 0:
        d += timedelta(days=step)  # 移动一天
        if _is_workday(d):  # 如果是工作日
            remaining -= 1  # 消耗一个工作日

    return {
        "start_date": f"{year}-{month:02d}-{day:02d}",  # 起始日期
        "workdays": workdays,  # 增加的工作日天数
        "result_date": d.isoformat(),  # 推算结果日期
    }


def count_workdays(year: int, month: int, day: int, end_year: int, end_month: int, end_day: int) -> dict:
    """
    计算两个日期之间的工作日数量

    Args:
        year: 起始公历年
        month: 起始公历月
        day: 起始公历日
        end_year: 结束公历年
        end_month: 结束公历月
        end_day: 结束公历日

    Returns:
        工作日计数结果，字段与 WorkdayCountResponse 模型对应
    """
    d = date(year, month, day)
    end_d = date(end_year, end_month, end_day)

    # -- 确保起始 <= 结束
    if d > end_d:
        d, end_d = end_d, d

    count = 0  # 工作日计数器
    total = (end_d - d).days + 1  # 总天数(含首尾)
    current = d

    while current <= end_d:
        if _is_workday(current):  # 如果是工作日
            count += 1
        current += timedelta(days=1)

    return {
        "start_date": f"{year}-{month:02d}-{day:02d}",  # 起始日期
        "end_date": f"{end_year}-{end_month:02d}-{end_day:02d}",  # 结束日期
        "workdays": count,  # 工作日数量
        "total_days": total,  # 总天数
    }


def _is_workday(d: date) -> bool:
    """
    判断单个日期是否为工作日（内部辅助函数）

    Args:
        d: 日期对象

    Returns:
        True=工作日, False=非工作日
    """
    weekday = d.weekday()  # 0=周一, 6=周日
    info = get_holiday_info(d)  # 获取假日信息
    is_holiday = info.get("is_holiday", False)  # 是否为法定假日
    is_replaced = info.get("is_replaced", False)  # 是否为调休上班日
    is_weekend = weekday >= 5  # 周六周日

    return is_replaced or (not is_holiday and not is_weekend)
