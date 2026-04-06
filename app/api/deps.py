"""
RapidAPI 鉴权依赖
验证请求是否来自 RapidAPI 网关（通过 X-RapidAPI-Proxy-Secret）

鉴权策略：
- 开发环境：RAPIDAPI_PROXY_SECRET 为空时跳过验证
- 生产环境：必须携带正确的 X-RapidAPI-Proxy-Secret
- /health 和 /docs 等系统路径不受鉴权保护
"""
from fastapi import Request, Depends
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.response import fail


async def verify_rapidapi_request(request: Request) -> JSONResponse | None:
    """
    验证请求来源是否为 RapidAPI 网关

    RapidAPI 网关转发请求时会自动注入 X-RapidAPI-Proxy-Secret header。
    后端验证该值是否与配置的 RAPIDAPI_PROXY_SECRET 一致，防止绕过网关直连。

    Returns:
        None: 验证通过，继续执行路由
        JSONResponse: 验证失败，返回错误响应（HTTP 200 + code:401）
    """
    secret = settings.RAPIDAPI_PROXY_SECRET

    # 未配置密钥 = 开发模式，跳过验证
    if not secret:
        return None

    proxy_secret = request.headers.get("X-RapidAPI-Proxy-Secret")

    if not proxy_secret:
        return fail(message="未提供鉴权凭证", code=401)

    if proxy_secret != secret:
        return fail(message="鉴权凭证无效", code=401)

    return None
