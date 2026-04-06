"""
公共校验模块
提供跨模块复用的日期校验、参数校验等通用函数
"""
from datetime import date as date_type

from app.core.exceptions import ParamException
from app.services.i18n.locale import SUPPORTED_LANGS


# 年份允许范围（中国历法 + 节气合理区间）
YEAR_MIN = 1900
YEAR_MAX = 2100

# 支持的语言列表
SUPPORTED_LANGS_SET = set(SUPPORTED_LANGS)

# 工作日推算天数上限（约 40 年，防止 DoS）
MAX_WORKDAYS = 10000

# 工作日计数日期跨度上限（约 100 年）
MAX_DATE_SPAN_DAYS = 36500


def check_year(year: int) -> None:
    """
    校验年份参数合法性，不合法则抛出 ParamException(400)

    Args:
        year: 年份，范围 1900-2100
    """
    if not (YEAR_MIN <= year <= YEAR_MAX):
        raise ParamException(f"年份必须在 {YEAR_MIN}-{YEAR_MAX} 之间，当前值: {year}")


def parse_date(date_str: str) -> date_type:
    """
    解析 YYYY-MM-DD 格式日期字符串，返回 datetime.date 对象

    同时校验年份范围 1900-2100。

    Args:
        date_str: 日期字符串，格式 YYYY-MM-DD

    Returns:
        datetime.date 对象

    Raises:
        ParamException: 格式错误或日期不存在或年份超出范围时
    """
    try:
        d = date_type.fromisoformat(date_str)
    except ValueError:
        raise ParamException(f"日期格式错误，请使用 YYYY-MM-DD 格式，当前值: {date_str}")
    # 校验年份范围
    if not (YEAR_MIN <= d.year <= YEAR_MAX):
        raise ParamException(f"年份必须在 {YEAR_MIN}-{YEAR_MAX} 之间，当前值: {d.year}")
    return d


def validate_lang(lang: str | None) -> str:
    """
    校验并规范化语言参数

    Args:
        lang: 语言代码，如 en/ja/ko，为空则默认 zh

    Returns:
        规范化后的语言代码

    Raises:
        ParamException: 不支持的语言代码
    """
    if not lang:
        return "zh"
    lang = lang.lower().strip()
    if lang not in SUPPORTED_LANGS_SET:
        raise ParamException(f"不支持的语言代码: {lang}，支持: {', '.join(sorted(SUPPORTED_LANGS))}")
    return lang
