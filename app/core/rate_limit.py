"""
全局限流器
统一 SlowAPI Limiter 实例，所有路由文件共享同一个限流状态和异常处理器

限流策略：
- 生产环境：按 X-RapidAPI-Key（每个订阅者独立计数）
- 开发环境：按客户端 IP（本地调试无 RapidAPI header）
"""
from fastapi import Request

from slowapi import Limiter


def _rate_limit_key(request: Request) -> str:
    """优先按 RapidAPI Key 限流，回退到客户端 IP"""
    api_key = request.headers.get("X-RapidAPI-Key")
    if api_key:
        return api_key
    # 开发环境回退到 IP
    return request.client.host if request.client else "unknown"


limiter = Limiter(key_func=_rate_limit_key, default_limits=["120/minute"])
