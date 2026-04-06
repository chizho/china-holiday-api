"""
中国日期工具包数据模型
整合后的响应模型：日期综合查询、工作日计算、节气
"""
from typing import Optional

from pydantic import BaseModel, Field


# ============================================================
# 日期综合查询（合并：农历 + 生肖 + 星座 + 天干地支 + 黄历）
# ============================================================

class GanZhiDetail(BaseModel):
    """天干地支详细信息（年月日柱）"""
    ganzhi: str = Field(description="干支，如 乙巳")
    gan: str = Field(description="天干，如 乙")
    zhi: str = Field(description="地支，如 巳")
    nayin: str = Field(default="", description="纳音，如 佛灯火")


class XingzuoDetail(BaseModel):
    """星座详细信息"""
    name: str = Field(description="星座中文名，如 天秤座")
    name_en: str = Field(description="星座英文名，如 Libra")
    date_range: str = Field(description="日期范围，如 9.23-10.23")
    element: str = Field(description="元素，如 风象")
    ruler: str = Field(description="守护星，如 金星")


class AlmanacDetail(BaseModel):
    """黄历详细信息"""
    # -- 宜忌
    yi: list[str] = Field(default_factory=list, description="宜")
    ji: list[str] = Field(default_factory=list, description="忌")
    # -- 冲煞
    chong_gan: str = Field(default="", description="冲天干")
    chong_zhi: str = Field(default="", description="冲地支")
    chong_shengxiao: str = Field(default="", description="冲生肖")
    chong_desc: str = Field(default="", description="冲描述，如 (丁酉)鸡")
    sha: str = Field(default="", description="煞方")
    # -- 胎神
    taishen: str = Field(default="", description="胎神占方")
    # -- 五行纳音
    wuxing_nayin: str = Field(default="", description="五行纳音")
    # -- 彭祖百忌
    pengzu: str = Field(default="", description="彭祖百忌")
    # -- 吉神凶煞
    jishen: list[str] = Field(default_factory=list, description="吉神")
    xiongsha: list[str] = Field(default_factory=list, description="凶煞")
    # -- 值星
    zhixing: str = Field(default="", description="建除十二值星")
    # -- 天神
    tianshen: str = Field(default="", description="值日天神")
    tianshen_type: str = Field(default="", description="天神类型")
    # -- 方位
    position_cai: str = Field(default="", description="财神方位")
    position_xi: str = Field(default="", description="喜神方位")
    position_fu: str = Field(default="", description="福神方位")
    position_yanggui: str = Field(default="", description="阳贵方位")
    position_yingui: str = Field(default="", description="阴贵方位")
    # -- 其他
    liuyao: str = Field(default="", description="六曜")
    wuhou: str = Field(default="", description="七十二候")
    xiu: str = Field(default="", description="二十八星宿")
    xiu_luck: str = Field(default="", description="星宿吉凶")


class SolarTermItem(BaseModel):
    """单个节气"""
    name: str = Field(description="节气名称，如 小寒")
    date: str = Field(description="节气日期，如 2025-01-05")
    is_jie: bool = Field(description="是否为「节」")


class DateInfoResponse(BaseModel):
    """日期综合查询响应（合并 5 个旧接口）"""
    # -- 公历
    solar_year: int = Field(description="公历年")
    solar_month: int = Field(description="公历月")
    solar_day: int = Field(description="公历日")
    # -- 农历
    lunar_year: int = Field(description="农历年")
    lunar_month: int = Field(description="农历月")
    lunar_day: int = Field(description="农历日")
    lunar_month_cn: str = Field(description="农历月中文，如 八月")
    lunar_day_cn: str = Field(description="农历日中文，如 初九")
    lunar_date_cn: str = Field(description="农历日期中文，如 乙巳年八月初九")
    # -- 生肖
    shengxiao: str = Field(description="生肖，如 蛇")
    shengxiao_emoji: str = Field(default="", description="生肖 emoji")
    # -- 星座
    xingzuo: XingzuoDetail = Field(description="星座详细信息")
    # -- 天干地支
    year_ganzhi: GanZhiDetail = Field(description="年柱干支")
    month_ganzhi: GanZhiDetail = Field(description="月柱干支")
    day_ganzhi: GanZhiDetail = Field(description="日柱干支")
    # -- 黄历
    almanac: AlmanacDetail = Field(description="黄历信息")
    # -- 节气
    solar_term_prev: Optional[SolarTermItem] = Field(default=None, description="前一节气")
    solar_term_next: Optional[SolarTermItem] = Field(default=None, description="后一节气")
    solar_term_current: Optional[SolarTermItem] = Field(default=None, description="当天节气")


# ============================================================
# 工作日模块
# ============================================================

class WorkdayCheckResponse(BaseModel):
    """工作日判断响应"""
    date: str = Field(description="查询日期")
    is_workday: bool = Field(description="是否为工作日")
    reason: str = Field(default="", description="原因说明")


class WorkdayCalcResponse(BaseModel):
    """工作日计算响应（合并 add + count）"""
    start_date: str = Field(description="起始日期")
    end_date: Optional[str] = Field(default=None, description="结束日期（add 模式为 result_date）")
    workdays: int = Field(description="工作日数量")
    total_days: Optional[int] = Field(default=None, description="总天数（count 模式）")


# ============================================================
# 节气模块
# ============================================================

class SolarTermListResponse(BaseModel):
    """节气列表响应"""
    year: int = Field(description="年份")
    terms: list[SolarTermItem] = Field(description="节气列表，按日期排序")


class SolarTermCurrentResponse(BaseModel):
    """当前节气信息响应"""
    date: str = Field(description="查询日期")
    prev: Optional[SolarTermItem] = Field(default=None, description="前一节气")
    next: Optional[SolarTermItem] = Field(default=None, description="后一节气")
    current: Optional[SolarTermItem] = Field(default=None, description="当天节气")
