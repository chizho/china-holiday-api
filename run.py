"""
本地开发启动脚本
启动方式：python run.py
端口配置：.env 文件中的 PORT 参数，默认 8080
"""
import uvicorn

from app.main import create_app
from app.core.config import settings

# Vercel 要求顶级暴露 app 对象，避免扫描报错
app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,  # 开发环境自动重载
        log_level="info",
    )
