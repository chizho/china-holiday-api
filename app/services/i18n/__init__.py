"""
国际化翻译模块
支持语言：zh(中文) / en(英文) / ja(日语) / ko(韩语) / vi(越南语) / es(西班牙语) / fr(法语) / de(德语)
翻译策略：
  L1 通用文本：假日名称、生肖、星座、节气、工作日描述 → 所有语言翻译
  L2 东亚文化：黄历宜忌、吉神凶煞、值星、六曜 → ja/ko/vi 翻译
  L3 不翻译：干支、纳音、冲煞、彭祖百忌、胎神、星宿等 → 保留原文
"""
from app.services.i18n.locale import SUPPORTED_LANGS, TRANSLATIONS


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


def t_list(keys: list[str], lang: str = "zh") -> list[str]:
    """批量翻译列表"""
    if lang == "zh":
        return keys
    return [t(k, lang) for k in keys]


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
    if lang == "zh":
        return data

    # -- 自动识别数据类型并分发
    if "almanac" in data:
        return _translate_date_info(data, lang)
    elif "is_holiday" in data:
        return _translate_holiday_info(data, lang)
    elif "holidays" in data:
        return _translate_holiday_list(data, lang)
    elif "is_workday" in data and "reason" in data:
        return _translate_workday_check(data, lang)
    elif "workdays" in data and "terms" not in data:
        return _translate_workday_calc(data, lang)
    elif "terms" in data:
        return _translate_solar_term_list(data, lang)
    elif "prev" in data and "next" in data:
        return _translate_solar_term_current(data, lang)
    return data


# ================================================================
# 各数据类型的翻译实现
# ================================================================

def _translate_date_info(data: dict, lang: str) -> dict:
    """翻译日期综合查询结果"""
    result = dict(data)

    # -- 生肖
    result["shengxiao"] = t(data.get("shengxiao", ""), lang)

    # -- 星座（已有 name_en，其他元素/守护星需要翻译）
    if "xingzuo" in result and isinstance(result["xingzuo"], dict):
        xz = dict(result["xingzuo"])
        xz["element"] = t(xz.get("element", ""), lang)
        xz["ruler"] = t(xz.get("ruler", ""), lang)
        result["xingzuo"] = xz

    # -- 黄历
    if "almanac" in result and isinstance(result["almanac"], dict):
        alm = dict(result["almanac"])
        alm["yi"] = t_list(alm.get("yi", []), lang)
        alm["ji"] = t_list(alm.get("ji", []), lang)
        alm["sha"] = t(alm.get("sha", ""), lang)
        alm["zhixing"] = t(alm.get("zhixing", ""), lang)
        alm["tianshen_type"] = t(alm.get("tianshen_type", ""), lang)
        # -- 方位：翻译关键词
        _translate_positions(alm, lang)
        # L3 不翻译: chong_*, taishen, wuxing_nayin, pengzu, jishen, xiongsha, tianshen, liuyao, wuhou, xiu, xiu_luck
        result["almanac"] = alm

    # -- 节气
    for jq_key in ("solar_term_prev", "solar_term_next", "solar_term_current"):
        jq = result.get(jq_key)
        if jq and isinstance(jq, dict):
            result[jq_key] = _translate_solar_term_item(jq, lang)

    return result


def _translate_positions(alm: dict, lang: str) -> dict:
    """翻译方位字段（关键词替换）"""
    pos_map = {
        "财神方位": t("财神方位", lang),
        "喜神方位": t("喜神方位", lang),
        "福神方位": t("福神方位", lang),
        "阳贵方位": t("阳贵方位", lang),
        "阴贵方位": t("阴贵方位", lang),
        "正东": {"en": "Due East",  "ja": "正東",   "ko": "정동",   "vi": "Chính Đông",  "es": "Este",  "fr": "Est",   "de": "Ost"}.get(lang, "正东"),
        "正南": {"en": "Due South", "ja": "正南",   "ko": "정남",   "vi": "Chính Nam",  "es": "Sur",   "fr": "Sud",   "de": "Süd"}.get(lang, "正南"),
        "正西": {"en": "Due West",  "ja": "正西",   "ko": "정서",   "vi": "Chính Tây",  "es": "Oeste", "fr": "Ouest", "de": "West"}.get(lang, "正西"),
        "正北": {"en": "Due North", "ja": "正北",   "ko": "정북",   "vi": "Chính Bắc",  "es": "Norte", "fr": "Nord",  "de": "Nord"}.get(lang, "正北"),
        "东北": {"en": "Northeast", "ja": "北東",   "ko": "북동",   "vi": "Đông Bắc",   "es": "Noreste","fr": "Nord-Est","de": "Nordost"}.get(lang, "东北"),
        "东南": {"en": "Southeast", "ja": "南東",   "ko": "남동",   "vi": "Đông Nam",   "es": "Sureste","fr": "Sud-Est","de": "Südost"}.get(lang, "东南"),
        "西北": {"en": "Northwest", "ja": "北西",   "ko": "북서",   "vi": "Tây Bắc",    "es": "Noroeste","fr": "Nord-Ouest","de": "Nordwest"}.get(lang, "西北"),
        "西南": {"en": "Southwest", "ja": "南西",   "ko": "남서",   "vi": "Tây Nam",    "es": "Suroeste","fr": "Sud-Ouest","de": "Südwest"}.get(lang, "西南"),
    }

    for field in ("position_cai", "position_xi", "position_fu", "position_yanggui", "position_yingui"):
        val = alm.get(field, "")
        if not val:
            continue
        for zh, translated in pos_map.items():
            val = val.replace(zh, translated)
        alm[field] = val

    return alm


def _translate_solar_term_item(jq: dict, lang: str) -> dict:
    """翻译单个节气"""
    return {
        "name": t(jq.get("name", ""), lang),
        "date": jq.get("date", ""),
        "is_jie": jq.get("is_jie", False),
    }


def _translate_holiday_info(data: dict, lang: str) -> dict:
    """翻译单日假日信息"""
    name = data.get("name", "")
    # 支持顿号分隔的复合假日名（如"国庆节、中秋节"）
    if "、" in name:
        sep = ", " if lang == "en" else "、"
        translated_name = sep.join(t(n.strip(), lang) for n in name.split("、"))
    else:
        translated_name = t(name, lang)
    return {**data, "name": translated_name}


def _translate_holiday_list(data: dict, lang: str) -> dict:
    """翻译假日列表"""
    holidays = []
    for h in data.get("holidays", []):
        name = h.get("name", "")
        # 支持顿号分隔的复合假日名
        if "、" in name:
            sep = ", " if lang == "en" else "、"
            translated_name = sep.join(t(n.strip(), lang) for n in name.split("、"))
        else:
            translated_name = t(name, lang)
        holidays.append({"date": h["date"], "name": translated_name})
    return {**data, "holidays": holidays}


def _translate_workday_check(data: dict, lang: str) -> dict:
    """翻译工作日判断结果"""
    reason = data.get("reason", "")
    # 替换 reason 中的中文关键词（先处理复合词再处理单词）
    translated_reason = reason
    # 复合词："法定假日-XXX" → 翻译 "法定假日" + "-" + 翻译每个假日名
    if "法定假日-" in translated_reason:
        prefix = t("法定假日", lang)
        holiday_part = translated_reason.split("法定假日-", 1)[1]
        # 假日名可能是顿号分隔的多个（如"国庆节、中秋节"）
        names = [n.strip() for n in holiday_part.split("、")]
        sep = "," if lang == "en" else "、"
        translated_names = [t(n, lang) for n in names]
        translated_reason = f"{prefix}-{sep.join(translated_names)}"
    else:
        # 单词替换
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
    result = dict(data)
    for key in ("prev", "next", "current"):
        jq = result.get(key)
        if jq and isinstance(jq, dict):
            result[key] = _translate_solar_term_item(jq, lang)
    return result
