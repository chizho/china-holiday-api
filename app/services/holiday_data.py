"""
中国法定假日数据管理

数据来源：https://github.com/NateScarlet/holiday-cn
- 每日自动抓取国务院公告
- CDN JSON 格式，按年份存储

缓存策略：
- 本地开发：文件缓存到 app/data/holidays/ 目录
- Serverless（Vercel 等）：内存缓存（文件系统只读）
"""

import json
import logging
import os
import time
from pathlib import Path
from datetime import date
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

# CDN 地址（jsDelivr 国内可访问）
CDN_BASE = "https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master"

# 本地缓存目录（仅本地开发使用）
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "holidays"

# 缓存过期时间（秒），默认 24 小时
CACHE_TTL = 24 * 60 * 60

# 判断是否为 Serverless 环境（Vercel / AWS Lambda 等）
IS_SERVERLESS = bool(os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))

# 内存缓存（Serverless 环境使用）
_memory_cache: dict[str, dict] = {}
_memory_ts: dict[str, float] = {}


def _fetch_remote(year: int) -> dict:
    """从 CDN 获取指定年份的假日数据"""
    url = f"{CDN_BASE}/{year}.json"
    resp = httpx.get(url, timeout=10)
    if resp.status_code == 404:
        raise FileNotFoundError(f"{year}年假日数据暂未发布")
    resp.raise_for_status()
    return resp.json()


def load_year_data(year: int, use_cache: bool = True) -> dict:
    """
    加载指定年份的假日原始数据

    Serverless 环境：内存缓存
    本地开发环境：文件缓存（app/data/holidays/）

    Args:
        year: 年份
        use_cache: 是否使用缓存，False 则强制从 CDN 拉取

    Returns:
        {"year": int, "papers": [...], "days": [{"name": str, "date": str, "isOffDay": bool}, ...]}
    """
    key = str(year)

    # ---- Serverless 环境：内存缓存 ----
    if IS_SERVERLESS:
        if use_cache and key in _memory_cache:
            age = time.time() - _memory_ts[key]
            if age < CACHE_TTL:
                logger.info(f"[memory] 命中缓存: {year}")
                return _memory_cache[key]
            logger.info(f"[memory] 缓存已过期({age/3600:.1f}h)，重新拉取")

        logger.info(f"从 CDN 拉取 {year} 年假日数据")
        data = _fetch_remote(year)

        _memory_cache[key] = data
        _memory_ts[key] = time.time()
        logger.info(f"[memory] 已缓存: {year}")
        return data

    # ---- 本地开发环境：文件缓存 ----
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    local = DATA_DIR / f"{year}.json"

    if use_cache and local.exists():
        age = time.time() - local.stat().st_mtime
        if age < CACHE_TTL:
            logger.info(f"[file] 读取本地缓存: {local}")
            with open(local, "r", encoding="utf-8") as f:
                return json.load(f)
        logger.info(f"[file] 本地缓存已过期({age/3600:.1f}h)，重新拉取")

    logger.info(f"从 CDN 拉取 {year} 年假日数据")
    data = _fetch_remote(year)

    with open(local, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"[file] 已缓存到本地: {local}")

    return data


def get_all_holidays(year: int, use_cache: bool = True) -> dict[str, dict]:
    """
    获取指定年份全部假日数据（放假 + 调休上班），返回 dict 便于查询

    Returns:
        {"2025-01-01": {"name": "元旦", "is_holiday": True, "is_off_day": True}, ...}
    """
    raw = load_year_data(year, use_cache=use_cache)
    result = {}
    for day in raw.get("days", []):
        result[day["date"]] = {
            "name": day["name"],
            "is_holiday": day["isOffDay"],
            "is_off_day": day["isOffDay"],
        }
    return result


def refresh_cache(year: int) -> bool:
    """
    强制刷新指定年份的缓存

    Serverless 环境：清除内存缓存
    本地开发环境：从 CDN 重新拉取并写入文件

    Returns:
        是否刷新成功
    """
    try:
        data = _fetch_remote(year)
        key = str(year)

        if IS_SERVERLESS:
            _memory_cache[key] = data
            _memory_ts[key] = time.time()
            logger.info(f"[memory] 已刷新 {year} 年假日缓存")
        else:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            local = DATA_DIR / f"{year}.json"
            with open(local, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"[file] 已刷新 {year} 年假日缓存: {local}")

        return True
    except Exception as e:
        logger.error(f"刷新 {year} 年假日缓存失败: {e}")
        return False
