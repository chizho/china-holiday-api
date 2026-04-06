"""
日期综合查询路由
合并原 5 个接口：lunar/solar-to-lunar + zodiac/shengxiao + zodiac/xingzuo + lunar/ganzhi + almanac/daily + solar-term/current
"""
import logging

from fastapi import APIRouter, Query, Request

from app.common.validators import parse_date, validate_lang
from app.core.rate_limit import limiter
from app.core.response import ApiResponse, fail, success
from app.models.cn_datekit import DateInfoResponse
from app.services.cn_datekit.date import get_date_info
from app.services.i18n import translate_result

router = APIRouter(prefix="/date", tags=["日期查询 Date"])
logger = logging.getLogger(__name__)


@router.get(
    "",
    response_model=ApiResponse[DateInfoResponse],
    summary="日期综合查询",
    description="输入公历日期，一次性返回农历、生肖、星座、天干地支、黄历、节气等完整中国历法信息。支持 lang 参数切换输出语言。",
)
async def date_info(
    request: Request,
    date: str = Query(..., description="公历日期，格式 YYYY-MM-DD，如 2025-10-01"),
    lang: str = Query(default="zh", description="输出语言: zh/en/ja/ko/vi/es/fr/de"),
):
    """日期综合查询（合并：农历转换 + 生肖 + 星座 + 天干地支 + 黄历 + 节气）"""
    d = parse_date(date)
    lang = validate_lang(lang)
    try:
        result = get_date_info(d.year, d.month, d.day)
        return success(data=translate_result(result, lang))
    except FileNotFoundError as e:
        return fail(message=str(e), code=404)
    except Exception as e:
        logger.error(f"日期查询失败 [{date}]: {e}", exc_info=True)
        return fail(message="日期查询失败，请检查日期参数", code=500)
