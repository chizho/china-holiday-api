"""
Vercel Serverless Function 入口

Vercel Python 运行时自动识别 api/ 目录下的入口文件，
要求暴露名为 app 的顶级 ASGI 对象。
"""
from app.main import create_app

app = create_app()

# Vercel 兼容 handler
from starlette.requests import Request
from starlette.responses import Response


async def handler(request: Request) -> Response:
    """Vercel Serverless 调用入口"""
    return await app(request.scope, request.receive, request._send)
