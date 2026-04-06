"""
统一响应模块
定义 API 返回的标准格式：{"code": int, "message": str, "data": T}

设计说明：
- ApiResponse[T] 是泛型包装，code/message/data 三段式
- success()/fail() 快捷函数直接返回 JSONResponse
- 路由层 response_model 使用 ApiResponse[T]，确保 OpenAPI 文档与实际响应一致
"""
from typing import Any, Optional, TypeVar, Generic

from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应格式"""
    code: int = Field(default=200, description="状态码，200=成功")
    message: str = Field(default="success", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")


def success(data: Any = None, message: str = "success") -> JSONResponse:
    """
    成功响应，HTTP 状态码固定 200

    Args:
        data: 响应数据，任意类型
        message: 响应消息
    """
    return JSONResponse(
        status_code=200,
        content={"code": 200, "message": message, "data": data},
    )


def fail(message: str = "error", code: int = 400) -> JSONResponse:
    """
    失败响应，HTTP 状态码映射：400→400, 401→401, 403→403, 404→404, 422→422, 500→500, 其他→400

    Args:
        message: 错误消息
        code: 业务错误码
    """
    http_status = {400: 400, 401: 401, 403: 403, 404: 404, 422: 422, 500: 500}.get(code, 400)
    return JSONResponse(
        status_code=http_status,
        content={"code": code, "message": message, "data": None},
    )
