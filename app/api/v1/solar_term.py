"""
节气接口路由
提供节气列表查询、当前节气查询等接口
"""
import logging

from fastapi import APIRouter, Query, Request

from app.common.validators import check_year, parse_date, validate_lang
from app.core.rate_limit import limiter
from app.core.response import ApiResponse, fail, success
from app.models.cn_datekit import SolarTermListResponse, SolarTermCurrentResponse
from app.services.cn_datekit.solar_term import get_solar_terms, get_current_solar_term
from app.services.i18n import translate_result

router = APIRouter(prefix="/solar-term", tags=["节气 Solar Term"])
logger = logging.getLogger(__name__)


@router.get(
    "/list",
    response_model=ApiResponse[SolarTermListResponse],
    summary="获取指定年份的二十四节气列表",
    description="返回该年度全部 24 个节气的名称、日期、是否为「节」（而非「气」）。支持 lang 参数切换输出语言。",
)
async def list_solar_terms(
    request: Request,
    year: int = Query(..., description="年份，如 2025"),
    lang: str = Query(default="zh", description="输出语言: zh/en/ja/ko/vi/es/fr/de"),
):
    """获取指定年份的二十四节气列表"""
    check_year(year)
    lang = validate_lang(lang)
    try:
        result = get_solar_terms(year)
        return success(data=translate_result(result, lang))
    except FileNotFoundError as e:
        return fail(message=str(e), code=404)
    except Exception as e:
        logger.error(f"节气列表查询失败 [year={year}]: {e}", exc_info=True)
        return fail(message="节气列表查询失败，请检查年份参数", code=500)


@router.get(
    "/current",
    response_model=ApiResponse[SolarTermCurrentResponse],
    summary="查询指定日期的当前节气信息",
    description="返回指定日期所在的前一节气、后一节气、当天是否为节气。支持 lang 参数切换输出语言。",
)
async def current_solar_term(
    request: Request,
    date: str = Query(..., description="公历日期，格式 YYYY-MM-DD，如 2025-10-08"),
    lang: str = Query(default="zh", description="输出语言: zh/en/ja/ko/vi/es/fr/de"),
):
    """查询指定日期的当前节气信息"""
    d = parse_date(date)
    lang = validate_lang(lang)
    try:
        result = get_current_solar_term(d.year, d.month, d.day)
        return success(data=translate_result(result, lang))
    except FileNotFoundError as e:
        return fail(message=str(e), code=404)
    except Exception as e:
        logger.error(f"当前节气查询失败 [{date}]: {e}", exc_info=True)
        return fail(message="当前节气查询失败，请检查日期参数", code=500)
