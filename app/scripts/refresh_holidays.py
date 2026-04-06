"""
假日数据缓存刷新脚本

可手动运行，也可配合系统计划任务 / CI 定时执行。

用法：
    python -m app.scripts.refresh_holidays            # 刷新当前年和下一年
    python -m app.scripts.refresh_holidays 2025 2026   # 刷新指定年份
"""

import sys
import logging
from datetime import date

from app.services.holiday_data import refresh_cache

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    # 默认刷新当前年和下一年
    if len(sys.argv) > 1:
        years = [int(y) for y in sys.argv[1:]]
    else:
        current_year = date.today().year
        years = [current_year, current_year + 1]

    logger.info(f"开始刷新假日数据: {years}")
    for year in years:
        ok = refresh_cache(year)
        if ok:
            logger.info(f"  {year} 年 刷新成功")
        else:
            logger.error(f"  {year} 年 刷新失败")
    logger.info("刷新完成")


if __name__ == "__main__":
    main()
