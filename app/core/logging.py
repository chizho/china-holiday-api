"""
日志配置模块
统一日志格式和级别，生产/开发环境区分
"""
import logging
import sys

from app.core.config import settings


def setup_logging() -> None:
    """
    配置全局日志

    - 开发环境: DEBUG 级别，彩色输出到控制台
    - 生产环境: INFO 级别，JSON 格式输出
    """
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    # -- 日志格式
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # -- 控制台处理器
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # -- 根日志器配置
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # -- 避免重复添加 handler
    if not root_logger.handlers:
        root_logger.addHandler(handler)

    # -- 第三方库日志级别控制
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
