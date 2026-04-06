"""
假日接口路由
提供中国法定假日查询、假日列表、数据刷新等接口
"""
import logging

from fastapi import APIRouter, Query, Request

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.common.validators import check_year, parse_date, validate_lang
from app.core.config import settings
from app.core.response import ApiResponse, fail, success
from app.models.holiday import HolidayInfo, HolidayListResponse
from app.services.holiday_service import get_holiday, list_holidays, refresh_data
from app.services.i18n import translate_result

router = APIRouter(prefix="/holiday", tags=["假日 Holiday"])
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
logger = logging.getLogger(__name__)

# 内部管理密钥（仅用于保护 /refresh 接口，防止生产环境误开放）
ADMIN_TOKEN = "admin-holiday-refresh"


@router.get(
    "/query",
    response_model=ApiResponse[HolidayInfo],
    summary="查询指定日期的假日信息",
    description="输入日期，返回是否为法定假日、假日名称、是否调休等信息。支持 lang 参数切换输出语言。",
)
@limiter.limit("60/minute")
async def query_holiday(
    request: Request,
    date_str: str = Query(..., alias="date", description="查询日期，格式 YYYY-MM-DD，如 2025-10-01"),
    lang: str = Query(default="zh", description="输出语言: zh/en/ja/ko/vi/es/fr/de"),
):
    """查询指定日期的假日信息"""
    d = parse_date(date_str)
    lang = validate_lang(lang)
    try:
        info = get_holiday(date_str)
    except FileNotFoundError as e:
        return fail(message=str(e), code=404)
    return success(data=translate_result(info, lang))


@router.get(
    "/list",
    response_model=ApiResponse[HolidayListResponse],
    summary="获取指定年份的假日列表",
    description="返回该年度所有法定假日及调休安排。支持 lang 参数切换输出语言。",
)
@limiter.limit("60/minute")
async def list_holidays_api(
    request: Request,
    year: int = Query(..., description="年份，如 2025"),
    lang: str = Query(default="zh", description="输出语言: zh/en/ja/ko/vi/es/fr/de"),
):
    """获取指定年份的假日列表"""
    check_year(year)
    lang = validate_lang(lang)
    try:
        result = list_holidays(year)
    except FileNotFoundError as e:
        return fail(message=str(e), code=404)
    return success(data=translate_result(result, lang))


@router.post(
    "/refresh",
    response_model=ApiResponse[dict],
    summary="刷新假日缓存数据（仅管理环境）",
    description="从远程数据源重新拉取假日数据，需同时满足：DEBUG=true 且携带 admin_token 参数",
)
async def refresh_holidays(
    admin_token: str = Query(..., description="管理令牌"),
):
    """从远程数据源重新拉取假日数据"""
    if not settings.DEBUG:
        return fail(message="该接口仅限开发环境使用", code=403)
    if admin_token != ADMIN_TOKEN:
        return fail(message="管理令牌无效", code=403)
    refresh_data()
    return success(data={"refreshed": True}, message="假日数据刷新成功")
