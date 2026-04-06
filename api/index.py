"""
Vercel Serverless Function 入口

Vercel Python 运行时自动识别 api/ 目录下的入口文件，
要求暴露名为 app 的顶级 ASGI 对象。
"""
from app.main import create_app

app = create_app()
