"""
应用配置模块
从 .env 文件自动读取配置项，支持 pydantic-settings 类型校验
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置，从 .env 文件自动读取"""

    # 应用基础
    APP_NAME: str = "China Date Toolkit API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # 服务配置
    HOST: str = "0.0.0.0"
    PORT: int = 8080

    # API 路由前缀
    API_PREFIX: str = "/public-china-holiday"

    # RapidAPI 鉴权（部署时在环境变量配置，本地开发留空即跳过验证）
    RAPIDAPI_PROXY_SECRET: str = ""

    # 管理接口密钥（保护 /refresh 等管理端点，部署时在环境变量配置）
    ADMIN_TOKEN: str = ""

    # 请求限流（每 Key/IP 每分钟请求次数）
    RATE_LIMIT: str = "120/minute"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """获取全局配置单例"""
    return Settings()


# 全局配置实例，方便直接导入使用
settings = get_settings()
