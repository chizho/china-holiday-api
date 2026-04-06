# 项目结构

```
project_api/
├── app/
│   ├── api/                          # 路由层
│   │   ├── __init__.py
│   │   ├── deps.py                   # RapidAPI 鉴权依赖
│   │   └── v1/                       # v1 版本接口
│   │       ├── __init__.py
│   │       ├── date.py               # 日期综合查询（农历+生肖+星座+干支+黄历+节气）
│   │       ├── holiday.py            # 假日查询（单日查询+年度列表+数据刷新）
│   │       ├── workday.py            # 工作日计算（判断+推算+计数）
│   │       └── solar_term.py         # 节气查询（年度列表+当前节气）
│   ├── common/                       # 公共层
│   │   ├── __init__.py
│   │   └── validators.py             # 入参校验（日期解析、年份范围、参数上限）
│   ├── core/                         # 核心层
│   │   ├── __init__.py
│   │   ├── config.py                 # 应用配置（pydantic-settings）
│   │   ├── response.py               # 统一响应（success/fail + HTTP状态码映射）
│   │   ├── exceptions.py             # 全局异常处理
│   │   └── logging.py                # 日志配置
│   ├── data/                         # 数据目录（.gitignore 排除）
│   │   └── holidays/                 # 假日缓存 JSON（2018-2026）
│   ├── models/                       # 数据模型
│   │   ├── __init__.py
│   │   ├── cn_datekit.py             # 日期/工作日/节气响应模型
│   │   └── holiday.py                # 假日响应模型
│   ├── scripts/                      # 运维脚本
│   │   ├── __init__.py
│   │   ├── __main__.py               # python -m app.scripts 入口
│   │   └── refresh_holidays.py       # 假日数据刷新脚本
│   ├── services/                     # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── holiday_data.py           # 假日数据源（CDN拉取+本地缓存+TTL过期）
│   │   ├── holiday_service.py        # 假日业务逻辑
│   │   └── cn_datekit/               # 中国日历工具包
│   │       ├── __init__.py
│   │       ├── almanac.py            # 黄历（宜忌、冲煞、方位等）
│   │       ├── date.py               # 日期综合查询
│   │       ├── lunar.py              # 农历转换
│   │       ├── solar_term.py         # 二十四节气
│   │       ├── workday.py            # 工作日计算引擎
│   │       └── zodiac.py             # 生肖星座
│   ├── main.py                       # 应用入口（create_app 工厂模式）
│   └── __init__.py
│
├── _test_all.py                      # 全量接口测试（9个接口）
├── API.md                            # 接口文档
├── Procfile                          # 云平台部署配置
├── requirements.txt                  # Python 依赖
├── run.py                            # 本地启动入口
└── .env.example                      # 环境变量模板
```

## 技术栈

- **框架**：FastAPI + Uvicorn
- **校验**：Pydantic / pydantic-settings
- **HTTP 客户端**：httpx
- **限流**：slowapi
- **农历/节气**：lunar_python

## 接口概览

| # | 方法 | 路径 | 说明 |
|---|------|------|------|
| 1 | GET | `/health` | 健康检查 |
| 2 | GET | `/public-china-holiday/date` | 日期综合查询 |
| 3 | GET | `/public-china-holiday/holiday/query` | 查询指定日期假日 |
| 4 | GET | `/public-china-holiday/holiday/list` | 年度假日列表 |
| 5 | GET | `/public-china-holiday/workday` | 判断工作日 |
| 6 | GET | `/public-china-holiday/workday/calculate` | 工作日计算 |
| 7 | GET | `/public-china-holiday/solar-term/list` | 节气列表 |
| 8 | GET | `/public-china-holiday/solar-term/current` | 当前节气 |

## 假日数据

- 数据源：[NateScarlet/holiday-cn](https://github.com/NateScarlet/holiday-cn)（GitHub，每日自动抓取国务院公告）
- CDN：jsDelivr（国内可访问）
- 本地缓存：`app/data/holidays/{year}.json`，24小时 TTL 自动过期刷新
- 覆盖范围：2018-2026
