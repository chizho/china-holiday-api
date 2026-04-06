"""
假日服务模块
提供假日查询、假日列表、假日信息获取等业务逻辑
数据层委托给 holiday_data 模块
"""
from datetime import date
from typing import Optional

from app.services.holiday_data import get_all_holidays, refresh_cache


def get_holiday(date_str: str) -> dict:
    """
    查询单日假日信息（字符串版本，供路由层使用）

    Args:
        date_str: 日期字符串，格式 YYYY-MM-DD

    Returns:
        假日信息字典，字段与 HolidayInfo 模型对应
    """
    try:
        target_date = date.fromisoformat(date_str)
    except ValueError:
        return {
            "date": date_str,
            "is_holiday": False,
            "is_workday": True,
            "name": "工作日",
            "valid": False,
        }

    return get_holiday_info(target_date)


def get_holiday_info(d: date) -> dict:
    """
    查询单日假日信息（date 对象版本，供 workday 模块使用）

    Args:
        d: 日期对象

    Returns:
        {"date": str, "is_holiday": bool, "is_workday": bool, "name": str,
         "is_replaced": bool, "valid": bool}
    """
    date_str = d.isoformat()  # 格式化为 YYYY-MM-DD
    year = d.year

    # -- 加载该年度假日数据
    holidays = get_all_holidays(year)
    info = holidays.get(date_str)

    if info and info.get("is_holiday"):
        # -- 当天是法定假日
        return {
            "date": date_str,               # 日期
            "is_holiday": True,             # 是否为法定假日
            "is_workday": False,            # 是否为工作日
            "name": info["name"],           # 假日名称(国庆节/春节/...)
            "is_replaced": False,           # 是否为调休上班日
            "valid": True,                  # 数据是否有效
        }

    # -- 检查是否为调休上班日（非假日但在假日数据中 → 说明是调休补班）
    is_replaced = False
    if info and not info.get("is_holiday"):
        is_replaced = True  # 出现在假日数据中但标记为非假日 → 调休上班日

    return {
        "date": date_str,                   # 日期
        "is_holiday": False,                # 是否为法定假日
        "is_workday": not is_replaced,      # 是否为工作日（调休日为True）
        "name": "调休上班" if is_replaced else "工作日",  # 名称
        "is_replaced": is_replaced,         # 是否为调休上班日
        "valid": True,                      # 数据是否有效
    }


def list_holidays(year: int, month: Optional[int] = None) -> dict:
    """
    查询指定年份的假日列表

    Args:
        year: 年份
        month: 月份（可选），不传则返回全年

    Returns:
        假日列表，字段与 HolidayListResponse 模型对应
    """
    holidays = get_all_holidays(year)  # 加载年度数据

    # -- 过滤放假日（排除调休上班日）
    results = []
    for d_str, info in holidays.items():
        if info.get("is_holiday"):
            results.append({
                "date": d_str,          # 日期
                "name": info["name"],   # 假日名称
            })

    # -- 按日期排序
    results.sort(key=lambda x: x["date"])

    # -- 月份过滤（如果指定）
    if month is not None:
        results = [item for item in results if item["date"][5:7] == f"{month:02d}"]

    return {
        "total": len(results),  # 假日总数
        "year": year,           # 查询年份
        "month": month,         # 查询月份(全年为None)
        "holidays": results,    # 假日列表
    }


def refresh_data(year: Optional[int] = None) -> None:
    """
    刷新假日缓存数据

    Args:
        year: 指定年份（可选），不传则刷新当前年+下一年
    """
    import datetime
    if year is None:
        current = datetime.date.today().year
        years = [current, current + 1]
    else:
        years = [year]

    for y in years:
        refresh_cache(y)  # 逐年份刷新
