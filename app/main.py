"""
FastAPI 应用入口
China Date Toolkit API — 中国日期工具包接口服务

功能模块（4 个路由）：
- 日期查询（农历 + 生肖 + 星座 + 天干地支 + 黄历 + 节气）
- 假日查询（法定假日、调休安排）
- 工作日计算（判断、推算、计数）
- 节气查询（二十四节气列表）

部署：
- 本地启动：python run.py
- 云平台部署：Procfile 配置的 uvicorn --factory 命令
"""
import logging

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.api.deps import verify_rapidapi_request
from app.api.v1 import date, holiday, workday, solar_term
from app.core.config import settings
from app.core.exceptions import register_exception_handlers

logger = logging.getLogger(__name__)

# -- 请求限流器（全局默认）
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT])


def create_app() -> FastAPI:
    """
    创建 FastAPI 应用实例（工厂模式）

    适合云平台部署（Render/Railway/Fly.io 等）使用 --factory 参数加载
    """
    # -- 初始化日志
    from app.core.logging import setup_logging
    setup_logging()

    # -- 创建应用（生产环境关闭 Swagger/OpenAPI 文档）
    app = FastAPI(
        title="China Date Toolkit API",
        description="中国日期工具包接口服务，提供法定假日、农历、生肖、黄历、工作日、节气等查询",
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
    )

    # -- 限流器挂载
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # -- CORS 中间件（跨域支持，allow_credentials=False 避免 * + credentials 冲突）
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # -- 注册全局异常处理器
    register_exception_handlers(app)

    # -- 注册健康检查接口（RapidAPI / 云平台健康探针，无需鉴权）
    @app.get("/health", tags=["系统 System"])
    @limiter.exempt
    async def health_check(request: Request):
        """健康检查接口，返回服务运行状态"""
        from app.core.response import success
        return success(data={"status": "ok", "version": "1.0.0"})

    # -- 注册业务路由（全局鉴权依赖：生产环境验证 RapidAPI Proxy Secret）
    deps = [Depends(verify_rapidapi_request)]
    app.include_router(date.router, prefix=settings.API_PREFIX, dependencies=deps)
    app.include_router(holiday.router, prefix=settings.API_PREFIX, dependencies=deps)
    app.include_router(workday.router, prefix=settings.API_PREFIX, dependencies=deps)
    app.include_router(solar_term.router, prefix=settings.API_PREFIX, dependencies=deps)

    logger.info("China Date Toolkit API 启动完成")
    return app
