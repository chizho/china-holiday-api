"""
本地开发启动脚本
启动方式：python run.py
端口配置：.env 文件中的 PORT 参数，默认 8080
"""
import uvicorn

from app.core.config import settings


if __name__ == "__main__":
    uvicorn.run(
        "app.main:create_app",
        factory=True,  # 使用工厂模式加载应用
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,  # 开发环境自动重载
        log_level="info",
    )
