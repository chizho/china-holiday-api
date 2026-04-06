"""
全局异常处理模块
定义业务异常类和统一异常处理器
所有路由层抛出的异常都会被拦截并转换为标准 JSON 响应
"""
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.response import fail

logger = logging.getLogger(__name__)


class BizException(Exception):
    """业务异常基类，路由层抛出后由 biz_exception_handler 统一处理"""

    def __init__(self, code: int = 400, message: str = "业务异常"):
        self.code = code
        self.message = message


class NotFoundException(BizException):
    """资源未找到异常"""

    def __init__(self, message: str = "资源不存在"):
        super().__init__(code=404, message=message)


class ParamException(BizException):
    """参数校验异常"""

    def __init__(self, message: str = "参数错误"):
        super().__init__(code=422, message=message)


async def biz_exception_handler(request: Request, exc: BizException) -> JSONResponse:
    """业务异常处理器"""
    return fail(code=exc.code, message=exc.message)


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """未捕获异常兜底处理器，记录日志但不暴露内部细节"""
    logger.error(f"未捕获异常 [{request.url}]: {exc}", exc_info=True)
    return fail(code=500, message="内部服务异常")


def register_exception_handlers(app: FastAPI) -> None:
    """
    注册全局异常处理器到 FastAPI 应用

    Args:
        app: FastAPI 应用实例
    """
    app.add_exception_handler(BizException, biz_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
