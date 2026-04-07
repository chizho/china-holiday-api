# China Public Holiday & Multilingual Calendar API

> 中国公共假期及多语言日历 API — 提供中国大陆节假日、工作日、农历、生肖、星座、干支、黄历、二十四节气的查询与计算服务，支持 8 种语言输出。

**Base URL:** `https://china-holiday-api.vercel.app`

**支持语言:** `zh`(中文) | `en`(英文) | `ja`(日语) | `ko`(韩语) | `vi`(越南语) | `es`(西班牙语) | `fr`(法语) | `de`(德语)

**数据来源:** 国务院办公厅每年发布的《部分节假日安排通知》，自动抓取更新。

---

## 目录

- [通用说明](#通用说明)
  - [鉴权方式](#鉴权方式)
  - [统一响应格式](#统一响应格式)
  - [多语言支持](#多语言支持)
  - [错误码说明](#错误码说明)
  - [日期格式](#日期格式)
  - [速率限制](#速率限制)
- [接口清单](#接口清单)
- [接口详情](#接口详情)
  - [1. 健康检查](#1-健康检查)
  - [2. 日期综合查询](#2-日期综合查询)
  - [3. 查询指定日期假日信息](#3-查询指定日期假日信息)
  - [4. 获取年度假日列表](#4-获取年度假日列表)
  - [5. 刷新假日缓存（管理员）](#5-刷新假日缓存管理员)
  - [6. 判断是否为工作日](#6-判断是否为工作日)
  - [7. 工作日计算](#7-工作日计算)
  - [8. 二十四节气列表](#8-二十四节气列表)
  - [9. 查询当前节气信息](#9-查询当前节气信息)
- [错误响应示例](#错误响应示例)

---

## 通用说明

### 鉴权方式

所有业务接口需在请求头携带 `X-RapidAPI-Key` 进行鉴权：

```
X-RapidAPI-Key: YOUR_API_KEY
```

> API Key 通过 RapidAPI 订阅获取。健康检查接口（`/health`）无需鉴权，可用于服务可用性监控。

### 统一响应格式

所有接口统一返回以下 JSON 结构：

```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | int | 业务状态码，200 表示成功 |
| `message` | string | 状态描述 |
| `data` | object/null | 响应数据，失败时为 null |

### 多语言支持

所有业务接口均支持 `lang` Query 参数，用于切换响应数据的语言：

| 参数 | 位置 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `lang` | query | string | 否 | `zh` | 输出语言代码（zh=中文, en=英文, ja=日语, ko=韩语, vi=越南语, es=西班牙语, fr=法语, de=德语） |

**支持的语言代码：**

| 代码 | 语言 | 覆盖范围 |
|------|------|---------|
| `zh` | 中文 | 全字段翻译 |
| `en` | 英文 | 假日名称、生肖、星座、节气、工作日、方位等 |
| `ja` | 日语 | 假日名称、生肖、星座、节气、黄历宜忌、吉神凶煞、值星等 |
| `ko` | 韩语 | 假日名称、生肖、星座、节气、黄历宜忌、吉神凶煞、值星等 |
| `vi` | 越南语 | 假日名称、生肖、星座、节气、黄历宜忌、吉神凶煞、值星等 |
| `es` | 西班牙语 | 假日名称、生肖、星座、节气、工作日等 |
| `fr` | 法语 | 假日名称、生肖、星座、节气、工作日等 |
| `de` | 德语 | 假日名称、生肖、星座、节气、工作日等 |

> **翻译策略：** L1 通用文本（所有语言）+ L2 东亚文化特有词汇（ja/ko/vi）+ L3 不翻译（干支、纳音、彭祖百忌等中国传统术语）。

### 错误码说明

| HTTP 状态码 | 业务 code | 说明 |
|-------------|----------|------|
| 200 | 200 | 请求成功 |
| 400 | 400 | 参数错误（格式错误、缺失必填参数、超出范围等） |
| 401 | 401 | 未提供 `X-RapidAPI-Key` 请求头或 API Key 无效 |
| 403 | 403 | 无权限（管理员接口非管理员调用、接口仅限开发环境） |
| 404 | 404 | 资源不存在（国务院尚未发布该年份假日数据等） |
| 422 | 422 | 请求参数校验失败 |
| 500 | 500 | 服务器内部错误 |

### 日期格式

所有日期参数和返回值统一使用 `YYYY-MM-DD` 格式（ISO 8601），例如 `2025-10-01`。

### 速率限制

默认限制：每个 API Key 每分钟 120 次请求。超出限制将返回 `429 Too Many Requests`。

---

## 接口清单

| # | 方法 | 路径 | 说明 | 鉴权 |
|---|------|------|------|------|
| 1 | GET | `/health` | 健康检查 | 否 |
| 2 | GET | `/public-china-holiday/date` | 日期综合查询 | 是 |
| 3 | GET | `/public-china-holiday/holiday/query` | 查询指定日期假日信息 | 是 |
| 4 | GET | `/public-china-holiday/holiday/list` | 获取年度假日列表 | 是 |
| 5 | POST | `/public-china-holiday/holiday/refresh` | 刷新假日缓存 | 是 |
| 6 | GET | `/public-china-holiday/workday` | 判断是否为工作日 | 是 |
| 7 | GET | `/public-china-holiday/workday/calculate` | 工作日计算 | 是 |
| 8 | GET | `/public-china-holiday/solar-term/list` | 二十四节气列表 | 是 |
| 9 | GET | `/public-china-holiday/solar-term/current` | 查询当前节气信息 | 是 |

---

## 接口详情

### 1. 健康检查

用于服务可用性监控和 RapidAPI 健康探针，无需鉴权。

**请求**

```
GET /health
```

**参数**

无

**成功响应**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "status": "ok",
    "version": "1.0.0"
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `data.status` | string | 服务状态，固定为 `"ok"` |
| `data.version` | string | API 版本号 |

---

### 2. 日期综合查询

输入公历日期，一次性返回农历、生肖、星座、天干地支、黄历、节气等完整中国历法信息。**支持多语言输出。**

**请求**

```
GET /public-china-holiday/date?date=2025-10-01&lang=en
```

**参数**

| 参数 | 位置 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `date` | query | string | 是 | — | 公历日期，格式 `YYYY-MM-DD` |
| `lang` | query | string | 否 | `zh` | 输出语言：zh/en/ja/ko/vi/es/fr/de（默认 zh） |

**成功响应**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "solar_year": 2025,
    "solar_month": 10,
    "solar_day": 1,
    "lunar_year": 2025,
    "lunar_month": 8,
    "lunar_day": 9,
    "lunar_month_cn": "八月",
    "lunar_day_cn": "初九",
    "lunar_date_cn": "乙巳年八月初九",
    "shengxiao": "蛇",
    "shengxiao_emoji": "🐍",
    "xingzuo": {
      "name": "天秤座",
      "name_en": "Libra",
      "date_range": "9.23-10.23",
      "element": "风象",
      "ruler": "金星"
    },
    "year_ganzhi": {
      "ganzhi": "乙巳",
      "gan": "乙",
      "zhi": "巳",
      "nayin": "佛灯火"
    },
    "month_ganzhi": {
      "ganzhi": "乙酉",
      "gan": "乙",
      "zhi": "酉",
      "nayin": "泉中水"
    },
    "day_ganzhi": {
      "ganzhi": "丁丑",
      "gan": "丁",
      "zhi": "丑",
      "nayin": "涧下水"
    },
    "almanac": {
      "yi": ["祭祀", "出行", "冠笄", "嫁娶"],
      "ji": ["开市", "动土", "破土"],
      "chong_gan": "辛",
      "chong_zhi": "未",
      "chong_shengxiao": "羊",
      "chong_desc": "(辛未)羊",
      "sha": "东",
      "taishen": "占门碓外东南",
      "wuxing_nayin": "天河水",
      "pengzu": "丁不剃头头必生疮，丑不冠带主不还乡",
      "jishen": ["天德", "月德", "天恩"],
      "xiongsha": ["月破", "大耗"],
      "zhixing": "建",
      "tianshen": "玄武",
      "tianshen_type": "黑道",
      "position_cai": "正东",
      "position_xi": "西南",
      "position_fu": "西北",
      "position_yanggui": "正北",
      "position_yingui": "东南",
      "liuyao": "先胜",
      "wuhou": "鸿雁来宾",
      "xiu": "室",
      "xiu_luck": "吉"
    },
    "solar_term_prev": {
      "name": "秋分",
      "date": "2025-09-23",
      "is_jie": true
    },
    "solar_term_next": {
      "name": "寒露",
      "date": "2025-10-08",
      "is_jie": false
    },
    "solar_term_current": null
  }
}
```

**响应字段说明**

| 字段路径 | 类型 | 说明 |
|---------|------|------|
| `solar_year/month/day` | int | 公历年月日 |
| `lunar_year/month/day` | int | 农历年月日（数字）。闰月编码：`lunar_month` = 月份 + 10（如闰八月 = 18）。显示用 `lunar_month_cn` |
| `lunar_month_cn` | string | 农历月中文名（如"八月"、"闰四月"） |
| `lunar_day_cn` | string | 农历日中文名（如"初一"、"十五"） |
| `lunar_date_cn` | string | 完整农历日期（如"乙巳年八月初九"） |
| `shengxiao` | string | 生肖名称 |
| `shengxiao_emoji` | string | 生肖 emoji |
| `xingzuo` | object | 星座详细信息 |
| `xingzuo.name` | string | 星座中文名 |
| `xingzuo.name_en` | string | 星座英文名 |
| `xingzuo.date_range` | string | 日期范围 |
| `xingzuo.element` | string | 元素（风象/火象/土象/水象） |
| `xingzuo.ruler` | string | 守护星 |
| `year_ganzhi/month_ganzhi/day_ganzhi` | object | 年柱/月柱/日柱干支 |
| `ganzhi` | string | 干支组合 |
| `gan` | string | 天干 |
| `zhi` | string | 地支 |
| `nayin` | string | 纳音（五行纳音） |
| `almanac` | object | 黄历信息 |
| `almanac.yi` | string[] | 宜 |
| `almanac.ji` | string[] | 忌 |
| `almanac.chong_desc` | string | 冲描述 |
| `almanac.sha` | string | 煞方 |
| `almanac.taishen` | string | 胎神占方 |
| `almanac.wuxing_nayin` | string | 五行纳音 |
| `almanac.pengzu` | string | 彭祖百忌 |
| `almanac.jishen` | string[] | 吉神宜趋 |
| `almanac.xiongsha` | string[] | 凶煞宜忌 |
| `almanac.zhixing` | string | 建除十二值星 |
| `almanac.tianshen` | string | 值日天神 |
| `almanac.tianshen_type` | string | 天神类型（黑道/黄道） |
| `almanac.position_cai/xi/fu` | string | 财神/喜神/福神方位 |
| `almanac.position_yanggui/yingui` | string | 阳贵/阴贵方位 |
| `almanac.liuyao` | string | 六曜 |
| `almanac.wuhou` | string | 七十二候 |
| `almanac.xiu` | string | 二十八星宿 |
| `almanac.xiu_luck` | string | 星宿吉凶 |
| `solar_term_prev/next/current` | object/null | 前一/后一/当天节气 |
| `solar_term_*.name` | string | 节气名称 |
| `solar_term_*.date` | string | 节气日期 |
| `solar_term_*.is_jie` | bool | 是否为「节」（false 则为「气」） |

---

### 3. 查询指定日期假日信息

输入日期，返回是否为法定假日、假日名称、是否为调休工作日等信息。**支持多语言输出。**

**请求**

```
GET /public-china-holiday/holiday/query?date=2025-10-01&lang=en
```

**参数**

| 参数 | 位置 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `date` | query | string | 是 | — | 查询日期，格式 `YYYY-MM-DD` |
| `lang` | query | string | 否 | `zh` | 输出语言：zh/en/ja/ko/vi/es/fr/de（默认 zh） |

**成功响应**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "date": "2025-10-01",
    "is_holiday": true,
    "is_workday": false,
    "name": "国庆节、中秋节"
  }
}
```

**响应字段说明**

| 字段 | 类型 | 说明 |
|------|------|------|
| `date` | string | 查询日期 |
| `is_holiday` | bool | 是否为法定假日 |
| `is_workday` | bool | 是否为工作日（调休上班日返回 true） |
| `name` | string | 假日名称，非假日时为空或"工作日" |

---

### 4. 获取年度假日列表

返回指定年份所有法定假日及调休安排的完整列表。**支持多语言输出。**

**请求**

```
GET /public-china-holiday/holiday/list?year=2025&lang=en
```

**参数**

| 参数 | 位置 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `year` | query | int | 是 | — | 年份，范围 1900-2100，如 `2025` |
| `lang` | query | string | 否 | `zh` | 输出语言：zh/en/ja/ko/vi/es/fr/de（默认 zh） |

**成功响应**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 28,
    "year": 2025,
    "month": null,
    "holidays": [
      {
        "date": "2025-01-01",
        "name": "元旦"
      },
      {
        "date": "2025-01-28",
        "name": "春节"
      },
      {
        "date": "2025-10-01",
        "name": "国庆节、中秋节"
      }
    ]
  }
}
```

**响应字段说明**

| 字段 | 类型 | 说明 |
|------|------|------|
| `total` | int | 假日总天数 |
| `year` | int | 查询年份 |
| `month` | int/null | 查询月份（全年查询时为 null） |
| `holidays` | array | 假日列表，按日期升序排列 |
| `holidays[].date` | string | 假日日期 |
| `holidays[].name` | string | 假日名称（多个假日用顿号分隔） |

---

### 5. 刷新假日缓存（管理员）

⚠️ **仅管理员使用，不对外公开。** 从远程数据源（GitHub CDN）重新拉取假日数据并更新缓存。需要同时提供：
1. `X-RapidAPI-Key` 请求头（RapidAPI 订阅密钥）
2. `admin_token` 查询参数（环境变量 `ADMIN_TOKEN` 配置的管理员凭证）

**请求**

```
POST /public-china-holiday/holiday/refresh?admin_token=YOUR_ADMIN_TOKEN
```

**参数**

| 参数 | 位置 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `admin_token` | query | string | 是 | — | 管理员令牌 |

**成功响应**

```json
{
  "code": 200,
  "message": "假日数据刷新成功",
  "data": {
    "refreshed": true
  }
}
```

**错误响应**

```json
{
  "code": 403,
  "message": "该接口仅限开发环境使用",
  "data": null
}
```

```json
{
  "code": 403,
  "message": "管理令牌无效",
  "data": null
}
```

---

### 6. 判断是否为工作日

输入日期，返回是否为工作日及原因。自动识别法定假日、调休上班日、正常周末等。**支持多语言输出。**

**请求**

```
GET /public-china-holiday/workday?date=2025-10-01&lang=en
```

**参数**

| 参数 | 位置 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `date` | query | string | 是 | — | 公历日期，格式 `YYYY-MM-DD` |
| `lang` | query | string | 否 | `zh` | 输出语言：zh/en/ja/ko/vi/es/fr/de（默认 zh） |

**成功响应（假日）**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "date": "2025-10-01",
    "is_workday": false,
    "reason": "国庆节、中秋节"
  }
}
```

**成功响应（调休上班日）**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "date": "2025-09-28",
    "is_workday": true,
    "reason": "调休上班"
  }
}
```

**成功响应（正常周末）**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "date": "2025-10-04",
    "is_workday": false,
    "reason": "周末"
  }
}
```

**响应字段说明**

| 字段 | 类型 | 说明 |
|------|------|------|
| `date` | string | 查询日期 |
| `is_workday` | bool | 是否为工作日 |
| `reason` | string | 原因说明（假日名称/调休上班/周末/正常工作日） |

---

### 7. 工作日计算

支持两种互斥的计算模式（**必须二选一**）：
- **推算模式**（提供 `workdays`）：从起始日期推算 N 个工作日后的目标日期
- **计数模式**（提供 `end_date`）：计算两个日期之间的工作日数量

**支持多语言输出。**

**请求（推算模式）**

```
GET /public-china-holiday/workday/calculate?start_date=2025-09-28&workdays=5&lang=en
```

**请求（计数模式）**

```
GET /public-china-holiday/workday/calculate?start_date=2025-10-01&end_date=2025-10-31&lang=en
```

**参数**

| 参数 | 位置 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `start_date` | query | string | 是 | — | 起始日期，格式 `YYYY-MM-DD` |
| `workdays` | query | int | 否* | — | 推算模式：工作日天数（正数=未来，负数=过去），范围 ±10000。示例：`5` |
| `end_date` | query | string | 否* | — | 计数模式：结束日期，格式 `YYYY-MM-DD`，与 start_date 跨度不超过 36500 天。示例：`2025-10-31` |
| `lang` | query | string | 否 | `zh` | 输出语言：zh=en/ja/ko/vi/es/fr/de（默认 zh） |

> ⚠️ `workdays` 和 `end_date` **必须二选一**，不可同时提供。

**成功响应（推算模式）**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "start_date": "2025-09-28",
    "end_date": "2025-10-10",
    "workdays": 5
  }
}
```

**成功响应（计数模式）**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "start_date": "2025-10-01",
    "end_date": "2025-10-31",
    "workdays": 18,
    "total_days": 31
  }
}
```

**响应字段说明**

| 字段 | 类型 | 说明 |
|------|------|------|
| `start_date` | string | 起始日期 |
| `end_date` | string | 推算模式=目标日期，计数模式=结束日期 |
| `workdays` | int | 工作日数量 |
| `total_days` | int/null | 总天数（仅计数模式返回） |

---

### 8. 二十四节气列表

返回指定年份全部 24 个节气的名称、日期及类型。**支持多语言输出。**

**请求**

```
GET /public-china-holiday/solar-term/list?year=2025&lang=en
```

**参数**

| 参数 | 位置 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `year` | query | int | 是 | — | 年份，范围 1900-2100，如 `2025` |
| `lang` | query | string | 否 | `zh` | 输出语言：zh/en/ja/ko/vi/es/fr/de（默认 zh） |

**成功响应（节气列表）**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "year": 2025,
    "terms": [
      {
        "name": "小寒",
        "date": "2025-01-05",
        "is_jie": false
      },
      {
        "name": "大寒",
        "date": "2025-01-20",
        "is_jie": true
      },
      {
        "name": "立春",
        "date": "2025-02-03",
        "is_jie": false
      }
    ]
  }
}
```

**响应字段说明**

| 字段 | 类型 | 说明 |
|------|------|------|
| `year` | int | 查询年份 |
| `terms` | array | 节气列表，按日期升序排列（共 24 项） |
| `terms[].name` | string | 节气名称 |
| `terms[].date` | string | 节气公历日期 |
| `terms[].is_jie` | bool | 是否为「节」（true=节，false=气） |

---

### 9. 查询当前节气信息

返回指定日期所在的前一节气、后一节气，以及当天是否为节气。**支持多语言输出。**

**请求**

```
GET /public-china-holiday/solar-term/current?date=2025-10-08&lang=en
```

**参数**

| 参数 | 位置 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|------|--------|------|
| `date` | query | string | 是 | — | 公历日期，格式 `YYYY-MM-DD` |
| `lang` | query | string | 否 | `zh` | 输出语言：zh/en/ja/ko/vi/es/fr/de（默认 zh） |

**成功响应（非节气日）**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "date": "2025-10-05",
    "prev": {
      "name": "秋分",
      "date": "2025-09-23",
      "is_jie": true
    },
    "next": {
      "name": "寒露",
      "date": "2025-10-08",
      "is_jie": false
    },
    "current": null
  }
}
```

**成功响应（节气日）**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "date": "2025-10-08",
    "prev": {
      "name": "秋分",
      "date": "2025-09-23",
      "is_jie": true
    },
    "next": {
      "name": "霜降",
      "date": "2025-10-23",
      "is_jie": true
    },
    "current": {
      "name": "寒露",
      "date": "2025-10-08",
      "is_jie": false
    }
  }
}
```

**响应字段说明**

| 字段 | 类型 | 说明 |
|------|------|------|
| `date` | string | 查询日期 |
| `prev` | object/null | 前一节气（当天为首个节气时为 null） |
| `next` | object/null | 后一节气（当天为末个节气时为 null） |
| `current` | object/null | 当天节气（非节气日为 null） |

---

## 错误响应示例

### 参数格式错误 (400)

```json
// 请求: GET /public-china-holiday/date?date=2025/10/01
{
  "code": 400,
  "message": "日期格式错误，请使用 YYYY-MM-DD 格式，当前值: 2025/10/01",
  "data": null
}
```

### 年份超出范围 (400)

```json
// 请求: GET /public-china-holiday/holiday/list?year=1800
{
  "code": 400,
  "message": "年份必须在 1900-2100 之间，当前值: 1800",
  "data": null
}
```

### 不支持的语言 (400)

```json
// 请求: GET /public-china-holiday/holiday/list?year=2025&lang=xxx
{
  "code": 400,
  "message": "不支持的语言代码: xxx，支持: de, en, es, fr, ja, ko, vi, zh",
  "data": null
}
```

### 缺少必填参数 (422)

```json
// 请求: GET /public-china-holiday/date
{
  "detail": [
    {
      "loc": ["query", "date"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 数据暂未发布 (404)

```json
// 请求: GET /public-china-holiday/holiday/list?year=2030
{
  "code": 404,
  "message": "2030年假日数据暂未发布",
  "data": null
}
```

### API Key 无效 (401)

```json
{
  "code": 401,
  "message": "未提供鉴权凭证",
  "data": null
}
```

> 未携带 `X-RapidAPI-Key` 请求头，或 API Key 已失效/过期。请前往 RapidAPI 订阅获取有效密钥。

---

## 多语言示例

### 中文（默认）

```
GET /public-china-holiday/holiday/list?year=2025
```

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 28,
    "year": 2025,
    "month": null,
    "holidays": [
      {"date": "2025-01-01", "name": "元旦"},
      {"date": "2025-01-28", "name": "春节"},
      {"date": "2025-05-01", "name": "劳动节"}
    ]
  }
}
```

### 英文

```
GET /public-china-holiday/holiday/list?year=2025&lang=en
```

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 28,
    "year": 2025,
    "month": null,
    "holidays": [
      {"date": "2025-01-01", "name": "New Year's Day"},
      {"date": "2025-01-28", "name": "Spring Festival"},
      {"date": "2025-05-01", "name": "Labor Day"}
    ]
  }
}
```

### 日语

```
GET /public-china-holiday/holiday/list?year=2025&lang=ja
```

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 28,
    "year": 2025,
    "month": null,
    "holidays": [
      {"date": "2025-01-01", "name": "元旦"},
      {"date": "2025-01-28", "name": "春節"},
      {"date": "2025-05-01", "name": "労働節"}
    ]
  }
}
```

---

*文档版本：1.1.0 | 最后更新：2026-04-07 | 审查修订：补充 required 定义、lang 全称描述、参数 example、响应码细化、闰月编码说明*
