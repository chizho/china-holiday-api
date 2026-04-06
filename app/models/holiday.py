from pydantic import BaseModel, Field
from typing import Optional


# ============================================================
# 响应模型（用于 response_model）
# ============================================================

class HolidayInfo(BaseModel):
    """单日假日信息响应"""
    date: str = Field(..., description="日期，YYYY-MM-DD")
    is_holiday: bool = Field(..., description="是否为法定假日")
    is_workday: bool = Field(..., description="是否为工作日（调休上班日也算工作日）")
    name: str = Field(..., description="假日名称或'工作日'")


class HolidayListItem(BaseModel):
    """假日列表项"""
    date: str = Field(..., description="日期，YYYY-MM-DD")
    name: str = Field(..., description="假日名称")


class HolidayListResponse(BaseModel):
    """假日列表响应"""
    total: int = Field(..., description="假日总数")
    year: int = Field(..., description="查询年份")
    month: Optional[int] = Field(None, description="查询月份（全年查询时为 null）")
    holidays: list[HolidayListItem] = Field(..., description="假日列表")
