"""
工作日接口路由
合并：check（判断）+ calculate（推算/计数）
"""
import logging
from typing import Optional

from fastapi import APIRouter, Query, Request

from app.common.validators import MAX_DATE_SPAN_DAYS, MAX_WORKDAYS, parse_date, validate_lang
from app.core.rate_limit import limiter
from app.core.response import ApiResponse, fail, success
from app.models.cn_datekit import WorkdayCheckResponse, WorkdayCalcResponse
from app.services.cn_datekit.workday import check_workday, add_workdays, count_workdays
from app.services.i18n import translate_result

router = APIRouter(prefix="/workday", tags=["工作日 Workday"])
logger = logging.getLogger(__name__)


@router.get(
    "",
    response_model=ApiResponse[WorkdayCheckResponse],
    summary="判断是否为工作日",
    description="输入日期，返回是否为工作日及原因（如法定假日、周末、调休上班等）。支持 lang 参数切换输出语言。",
)
async def check(
    request: Request,
    date: str = Query(..., description="公历日期，格式 YYYY-MM-DD，如 2025-10-01"),
    lang: str = Query(default="zh", description="输出语言: zh/en/ja/ko/vi/es/fr/de"),
):
    """判断是否为工作日"""
    d = parse_date(date)
    lang = validate_lang(lang)
    try:
        result = check_workday(d.year, d.month, d.day)
        return success(data=translate_result(result, lang))
    except FileNotFoundError as e:
        return fail(message=str(e), code=404)
    except Exception as e:
        logger.error(f"工作日判断失败 [{date}]: {e}", exc_info=True)
        return fail(message="工作日判断失败，请检查日期参数", code=500)


@router.get(
    "/calculate",
    response_model=ApiResponse[WorkdayCalcResponse],
    summary="工作日计算",
    description="两种模式：① 传入 workdays 推算目标日期 ② 传入 end_date 计算工作日数量。支持 lang 参数切换输出语言。",
)
async def calculate(
    request: Request,
    start_date: str = Query(..., description="起始日期，格式 YYYY-MM-DD"),
    workdays: Optional[int] = Query(default=None, description="推算模式：要增加的工作日天数（正数=未来，负数=过去）"),
    end_date: Optional[str] = Query(default=None, description="计数模式：结束日期，格式 YYYY-MM-DD"),
    lang: str = Query(default="zh", description="输出语言: zh/en/ja/ko/vi/es/fr/de"),
):
    """工作日计算（推算目标日期 或 计算工作日数量）"""
    d = parse_date(start_date)

    # -- 推算模式：传入 workdays
    if workdays is not None:
        if abs(workdays) > MAX_WORKDAYS:
            return fail(message=f"workdays 参数不能超过 {MAX_WORKDAYS}", code=400)
        try:
            result = add_workdays(d.year, d.month, d.day, workdays)
            return success(data={
                "start_date": result["start_date"],
                "end_date": result["result_date"],
                "workdays": result["workdays"],
            })
        except FileNotFoundError as e:
            return fail(message=str(e), code=404)
        except Exception as e:
            logger.error(f"工作日推算失败 [{start_date}, workdays={workdays}]: {e}", exc_info=True)
            return fail(message="工作日推算失败，请检查参数", code=500)

    # -- 计数模式：传入 end_date
    if end_date is not None:
        ed = parse_date(end_date)
        span = abs((ed - d).days)
        if span > MAX_DATE_SPAN_DAYS:
            return fail(message=f"日期跨度不能超过 {MAX_DATE_SPAN_DAYS} 天（约100年）", code=400)
        try:
            result = count_workdays(d.year, d.month, d.day, ed.year, ed.month, ed.day)
            return success(data={
                "start_date": result["start_date"],
                "end_date": result["end_date"],
                "workdays": result["workdays"],
                "total_days": result["total_days"],
            })
        except FileNotFoundError as e:
            return fail(message=str(e), code=404)
        except Exception as e:
            logger.error(f"工作日计数失败 [{start_date} ~ {end_date}]: {e}", exc_info=True)
            return fail(message="工作日计数失败，请检查参数", code=500)

    return fail(message="请提供 workdays（推算模式）或 end_date（计数模式）", code=400)
