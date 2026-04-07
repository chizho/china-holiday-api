"""
国际化翻译模块
支持语言：zh(中文) / en(英文) / ja(日语) / ko(韩语) / vi(越南语) / es(西班牙语) / fr(法语) / de(德语)
翻译策略：
  L1 通用文本：假日名称、生肖、星座、节气、工作日、方位 → 词典翻译
  L2 东亚文化：黄历宜忌、吉神凶煞、值星、六曜 → 优先词典翻译
  L3 深文化兜底：主字段按目标语言输出，深文化术语缺失翻译时回退拼音，并统一补充 *_py 拼音字段
"""
from copy import deepcopy
import re

from pypinyin import lazy_pinyin

from app.services.i18n.locale import SUPPORTED_LANGS, TRANSLATIONS

CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")


# ---------------------------------------------------------------
# 基础工具
# ---------------------------------------------------------------

def has_chinese(value: str) -> bool:
    """判断字符串是否包含中文字符"""
    return bool(value) and bool(CHINESE_RE.search(value))



def to_pinyin(value: str) -> str:
    """将中文文本转为无声调拼音，非中文内容原样保留"""
    if not value:
        return value

    parts: list[str] = []
    for chunk in re.split(r"([（）()\[\]{}\-_/,:;，。！？、\s]+)", value):
        if not chunk:
            continue
        if has_chinese(chunk):
            parts.append(" ".join(item.capitalize() for item in lazy_pinyin(chunk)))
        else:
            parts.append(chunk)
    return "".join(parts).strip()



def sanitize_non_zh_text(value: str) -> str:
    """确保非中文语言主字段不含汉字，若仍含汉字则统一转拼音"""
    if not value:
        return value
    return to_pinyin(value) if has_chinese(value) else value



def t(key: str, lang: str = "zh") -> str:

    """
    单个文本翻译

    Args:
        key: 中文原文
        lang: 目标语言代码

    Returns:
        翻译后的文本，未找到则返回原文
    """
    if lang == "zh":
        return key

    lang_data = TRANSLATIONS.get(lang, {})
    return lang_data.get(key, key)



def translate_or_pinyin(value: str, lang: str = "zh") -> str:
    """优先走词典翻译，若结果仍含汉字则继续转拼音兜底"""
    if not value or lang == "zh":
        return value

    translated = t(value, lang)
    if translated != value:
        return sanitize_non_zh_text(translated)
    return to_pinyin(value) if has_chinese(value) else value




def t_list(keys: list[str], lang: str = "zh") -> list[str]:
    """批量翻译列表，未命中词典时回退拼音"""
    if lang == "zh":
        return keys
    return [translate_or_pinyin(k, lang) for k in keys]


def _set_translated_str(obj: dict, field: str, lang: str, *, use_pinyin_fallback: bool = True) -> None:
    """翻译字符串字段，并为所有语言统一补充 *_py 拼音字段"""
    value = obj.get(field)
    if not isinstance(value, str):
        obj[f"{field}_py"] = ""
        return

    obj[f"{field}_py"] = to_pinyin(value) if has_chinese(value) else value

    if not value or lang == "zh":
        return

    if use_pinyin_fallback:
        obj[field] = translate_or_pinyin(value, lang)
    else:
        obj[field] = sanitize_non_zh_text(t(value, lang))



def _set_translated_list(obj: dict, field: str, lang: str, *, use_pinyin_fallback: bool = True) -> None:
    """翻译列表字段，并为所有语言统一补充 *_py 拼音字段"""
    values = obj.get(field)
    if not isinstance(values, list):
        obj[f"{field}_py"] = []
        return

    obj[f"{field}_py"] = [to_pinyin(item) if isinstance(item, str) and has_chinese(item) else item for item in values]

    if not values or lang == "zh":
        return

    if use_pinyin_fallback:
        obj[field] = [translate_or_pinyin(item, lang) if isinstance(item, str) else item for item in values]
    else:
        obj[field] = [sanitize_non_zh_text(t(item, lang)) if isinstance(item, str) else item for item in values]




def _translate_xiu(value: str, lang: str) -> str:
    """星宿字段避免命中值星同名词条；zh 保持中文，其余语言统一走拼音"""
    if not value or lang == "zh":
        return value
    return to_pinyin(value) if has_chinese(value) else value



def _translate_chong_desc(value: str, lang: str) -> str:
    """翻译冲描述，如 (丁酉)鸡 → (Ding You)Rooster"""
    if not value or lang == "zh":
        return value

    match = re.match(r"^\(([^)]+)\)(.+)$", value)
    if not match:
        return translate_or_pinyin(value, lang)

    ganzhi, shengxiao = match.groups()
    return f"({to_pinyin(ganzhi)}){translate_or_pinyin(shengxiao, lang)}"


# ================================================================
# 各数据类型的翻译实现
# ================================================================

def translate_result(data: dict, lang: str = "zh") -> dict:
    """
    翻译接口返回结果（通用入口，路由层统一调用）

    根据 data 内容自动识别数据类型并翻译对应字段：
      - date: 日期综合查询（含农历、生肖、星座、干支、黄历、节气）
      - holiday: 假日查询
      - holiday_list: 假日列表
      - workday_check: 工作日判断
      - workday_calc: 工作日计算
      - solar_term_list: 节气列表
      - solar_term_current: 当前节气

    Args:
        data: service 层返回的原始字典
        lang: 目标语言代码

    Returns:
        翻译后的字典（新对象，不修改原数据）
    """
    if "almanac" in data:
        return _translate_date_info(data, lang)
    if "is_holiday" in data:
        return _translate_holiday_info(data, lang)
    if "holidays" in data:
        return _translate_holiday_list(data, lang)
    if "is_workday" in data and "reason" in data:
        return _translate_workday_check(data, lang)
    if "workdays" in data and "terms" not in data:
        return _translate_workday_calc(data, lang)
    if "terms" in data:
        return _translate_solar_term_list(data, lang)
    if "prev" in data and "next" in data:
        return _translate_solar_term_current(data, lang)
    return data



def _translate_date_info(data: dict, lang: str) -> dict:
    """翻译日期综合查询结果"""
    result = deepcopy(data)

    # -- 生肖
    raw_shengxiao = result.get("shengxiao", "")
    result["shengxiao_py"] = to_pinyin(raw_shengxiao) if has_chinese(raw_shengxiao) else raw_shengxiao
    result["shengxiao"] = translate_or_pinyin(raw_shengxiao, lang)

    # -- 星座
    if isinstance(result.get("xingzuo"), dict):
        xz = result["xingzuo"]
        for xf in ("name", "element", "ruler"):
            raw = xz.get(xf, "")
            xz[f"{xf}_py"] = to_pinyin(raw) if has_chinese(raw) else raw
            xz[xf] = translate_or_pinyin(raw, lang)

    # -- 天干地支（所有语言统一补充 *_py）
    for key in ("year_ganzhi", "month_ganzhi", "day_ganzhi"):
        gz = result.get(key)
        if isinstance(gz, dict):
            _set_translated_str(gz, "ganzhi", lang)
            _set_translated_str(gz, "gan", lang)
            _set_translated_str(gz, "zhi", lang)
            _set_translated_str(gz, "nayin", lang)

    # -- 黄历
    if isinstance(result.get("almanac"), dict):
        alm = result["almanac"]
        _set_translated_list(alm, "yi", lang)
        _set_translated_list(alm, "ji", lang)
        _set_translated_str(alm, "chong_gan", lang)
        _set_translated_str(alm, "chong_zhi", lang)
        raw_chong_shengxiao = alm.get("chong_shengxiao", "")
        alm["chong_shengxiao_py"] = to_pinyin(raw_chong_shengxiao) if has_chinese(raw_chong_shengxiao) else raw_chong_shengxiao
        alm["chong_shengxiao"] = translate_or_pinyin(raw_chong_shengxiao, lang)
        raw_chong_desc = alm.get("chong_desc", "")
        alm["chong_desc_py"] = to_pinyin(raw_chong_desc) if has_chinese(raw_chong_desc) else raw_chong_desc
        alm["chong_desc"] = _translate_chong_desc(raw_chong_desc, lang)
        _set_translated_str(alm, "sha", lang, use_pinyin_fallback=False)
        _set_translated_str(alm, "taishen", lang)
        _set_translated_str(alm, "wuxing_nayin", lang)
        _set_translated_str(alm, "pengzu", lang)
        _set_translated_list(alm, "jishen", lang)
        _set_translated_list(alm, "xiongsha", lang)
        _set_translated_str(alm, "zhixing", lang, use_pinyin_fallback=False)
        _set_translated_str(alm, "tianshen", lang)
        _set_translated_str(alm, "tianshen_type", lang, use_pinyin_fallback=False)
        _translate_positions(alm, lang)
        _set_translated_str(alm, "liuyao", lang)
        _set_translated_str(alm, "wuhou", lang)
        xiu_value = alm.get("xiu", "")
        alm["xiu_py"] = to_pinyin(xiu_value) if has_chinese(xiu_value) else xiu_value
        alm["xiu"] = _translate_xiu(xiu_value, lang)
        _set_translated_str(alm, "xiu_luck", lang, use_pinyin_fallback=False)

    # -- 节气
    for jq_key in ("solar_term_prev", "solar_term_next", "solar_term_current"):
        jq = result.get(jq_key)
        if jq and isinstance(jq, dict):
            result[jq_key] = _translate_solar_term_item(jq, lang)

    return result



def _translate_positions(alm: dict, lang: str) -> dict:
    """翻译方位字段（关键词替换）"""
    if lang == "zh":
        return alm

    pos_map = {
        "财神方位": t("财神方位", lang),
        "喜神方位": t("喜神方位", lang),
        "福神方位": t("福神方位", lang),
        "阳贵方位": t("阳贵方位", lang),
        "阴贵方位": t("阴贵方位", lang),
        "正东": {"en": "Due East", "ja": "正東", "ko": "정동", "vi": "Chính Đông", "es": "Este", "fr": "Est", "de": "Ost"}.get(lang, "正东"),
        "正南": {"en": "Due South", "ja": "正南", "ko": "정남", "vi": "Chính Nam", "es": "Sur", "fr": "Sud", "de": "Süd"}.get(lang, "正南"),
        "正西": {"en": "Due West", "ja": "正西", "ko": "정서", "vi": "Chính Tây", "es": "Oeste", "fr": "Ouest", "de": "West"}.get(lang, "正西"),
        "正北": {"en": "Due North", "ja": "正北", "ko": "정북", "vi": "Chính Bắc", "es": "Norte", "fr": "Nord", "de": "Nord"}.get(lang, "正北"),
        "东北": {"en": "Northeast", "ja": "北東", "ko": "북동", "vi": "Đông Bắc", "es": "Noreste", "fr": "Nord-Est", "de": "Nordost"}.get(lang, "东北"),
        "东南": {"en": "Southeast", "ja": "南東", "ko": "남동", "vi": "Đông Nam", "es": "Sureste", "fr": "Sud-Est", "de": "Südost"}.get(lang, "东南"),
        "西北": {"en": "Northwest", "ja": "北西", "ko": "북서", "vi": "Tây Bắc", "es": "Noroeste", "fr": "Nord-Ouest", "de": "Nordwest"}.get(lang, "西北"),
        "西南": {"en": "Southwest", "ja": "南西", "ko": "남서", "vi": "Tây Nam", "es": "Suroeste", "fr": "Sud-Ouest", "de": "Südwest"}.get(lang, "西南"),
    }

    for field in ("position_cai", "position_xi", "position_fu", "position_yanggui", "position_yingui"):
        val = alm.get(field, "")
        if not val:
            continue
        for zh, translated in pos_map.items():
            val = val.replace(zh, translated)
        alm[field] = sanitize_non_zh_text(val)

    return alm



def _translate_solar_term_item(jq: dict, lang: str) -> dict:
    """翻译单个节气"""
    return {
        "name": translate_or_pinyin(jq.get("name", ""), lang),
        "date": jq.get("date", ""),
        "is_jie": jq.get("is_jie", False),
    }




def _translate_holiday_info(data: dict, lang: str) -> dict:
    """翻译单日假日信息"""
    name = data.get("name", "")
    if "、" in name:
        sep = "、" if lang == "zh" else ", "
        translated_name = sep.join(t(n.strip(), lang) for n in name.split("、"))
    else:
        translated_name = t(name, lang)
    return {**data, "name": translated_name}



def _translate_holiday_list(data: dict, lang: str) -> dict:
    """翻译假日列表"""
    holidays = []
    for h in data.get("holidays", []):
        name = h.get("name", "")
        if "、" in name:
            sep = "、" if lang == "zh" else ", "
            translated_name = sep.join(t(n.strip(), lang) for n in name.split("、"))
        else:
            translated_name = t(name, lang)
        holidays.append({"date": h["date"], "name": translated_name})
    return {**data, "holidays": holidays}



def _translate_workday_check(data: dict, lang: str) -> dict:
    """翻译工作日判断结果"""
    reason = data.get("reason", "")
    translated_reason = reason
    if "法定假日-" in translated_reason:
        prefix = t("法定假日", lang)
        holiday_part = translated_reason.split("法定假日-", 1)[1]
        names = [n.strip() for n in holiday_part.split("、")]
        sep = "、" if lang == "zh" else ", "
        translated_names = [t(n, lang) for n in names]
        translated_reason = f"{prefix}-{sep.join(translated_names)}"
    else:
        for zh_key in ("调休上班", "周末", "工作日"):
            translated_reason = translated_reason.replace(zh_key, t(zh_key, lang))

    return {**data, "reason": translated_reason}



def _translate_workday_calc(data: dict, lang: str) -> dict:
    """工作日计算结果无文本字段，直接返回"""
    return data



def _translate_solar_term_list(data: dict, lang: str) -> dict:
    """翻译节气列表"""
    terms = [_translate_solar_term_item(jq, lang) for jq in data.get("terms", [])]
    return {**data, "terms": terms}



def _translate_solar_term_current(data: dict, lang: str) -> dict:
    """翻译当前节气信息"""
    result = deepcopy(data)
    for key in ("prev", "next", "current"):
        jq = result.get(key)
        if jq and isinstance(jq, dict):
            result[key] = _translate_solar_term_item(jq, lang)
    return result
