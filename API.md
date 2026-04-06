# China Date Toolkit API

> 中国日期工具包接口服务 — 提供法定假日、农历、生肖、星座、天干地支、黄历、工作日、二十四节气等查询

## 基本信息

| 项目 | 说明 |
|------|------|
| Base URL | `https://your-domain.onrender.com` |
| 协议 | HTTPS |
| 响应格式 | JSON |
| 字符编码 | UTF-8 |
| 鉴权方式 | Header `X-RapidAPI-Proxy-Secret`（生产环境） |
| 文档地址 | `/docs`（Swagger UI）、`/redoc`（ReDoc） |

## 统一响应格式

所有接口返回统一的 JSON 结构：

```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 业务状态码。200=成功，400=参数错误，401=鉴权失败，403=权限不足，500=服务异常 |
| message | string | 状态描述 |
| data | object/null | 业务数据 |

## 鉴权

生产环境下，所有 `/public-china-holiday/*` 接口需在请求头携带：

```
X-RapidAPI-Proxy-Secret: <你在 RapidAPI 后台配置的密钥>
```

未携带或密钥不匹配时返回：

```json
{"code": 401, "message": "鉴权凭证无效", "data": null}
```

> `/health`、`/docs`、`/redoc` 无需鉴权。

---

## 多语言支持

所有业务接口（除健康检查和刷新）支持 `lang` 参数切换输出语言：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| lang | string | 否 | zh | 输出语言代码 |

**支持语言：**

| 代码 | 语言 | 代码 | 语言 |
|------|------|------|------|
| zh | 中文（默认） | vi | 越南语 |
| en | English | es | Español |
| ja | 日本語 | fr | Français |
| ko | 한국어 | de | Deutsch |

**翻译策略（分层）：**

| 层级 | 翻译范围 | 适用语言 | 示例 |
|------|---------|---------|------|
| L1 通用 | 假日名称、生肖、星座、节气、工作日描述、煞方、方位 | 全部 8 种 | 蛇→Snake, 秋分→Autumnal Equinox |
| L2 东亚文化 | 黄历宜忌、吉神凶煞、值星、六曜、天神 | ja/ko/vi | 祭祀→祭祀(ja), 越南语→Tế tự |
| L3 不翻译 | 干支、纳音、冲煞、彭祖百忌、胎神、星宿 | 保留原文 | 乙巳、佛灯火 |

> L2 层级在 en/es/fr/de 下保留中文原文，因为这些概念在非汉字文化圈无对应翻译。

**请求示例：**

```
GET /public-china-holiday/date?date=2025-10-01&lang=en
GET /public-china-holiday/holiday/query?date=2025-10-01&lang=ja
GET /public-china-holiday/workday?date=2025-10-01&lang=ko
```

**错误示例：** 不支持的语言代码返回 400 错误。

```
GET /public-china-holiday/date?date=2025-10-01&lang=xx
→ {"code": 400, "message": "不支持的语言代码: xx，支持: de, en, es, fr, ja, ko, vi, zh"}
```

---

## 接口清单

### 1. 健康检查

| 项目 | 说明 |
|------|------|
| 路径 | `GET /health` |
| 鉴权 | 无 |
| 说明 | 服务健康探针，用于 RapidAPI / 云平台健康检查 |

**请求示例**

```
GET /health
```

**响应示例**

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

---

### 2. 日期综合查询

| 项目 | 说明 |
|------|------|
| 路径 | `GET /public-china-holiday/date` |
| 鉴权 | 是 |
| 说明 | 输入公历日期，一次性返回农历、生肖、星座、天干地支、黄历、节气等完整中国历法信息 |

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 是 | 公历日期，格式 YYYY-MM-DD |
| lang | string | 否 | 输出语言：zh/en/ja/ko/vi/es/fr/de，默认 zh |

**请求示例**

```
GET /public-china-holiday/date?date=2025-10-01
GET /public-china-holiday/date?date=2025-10-01&lang=en
```

**响应字段（data）**

| 字段 | 类型 | 说明 |
|------|------|------|
| solar_year | int | 公历年 |
| solar_month | int | 公历月 |
| solar_day | int | 公历日 |
| lunar_year | int | 农历年 |
| lunar_month | int | 农历月 |
| lunar_day | int | 农历日 |
| lunar_month_cn | string | 农历月中文，如 八月 |
| lunar_day_cn | string | 农历日中文，如 初九 |
| lunar_date_cn | string | 农历日期中文，如 乙巳年八月初九 |
| shengxiao | string | 生肖，如 蛇 |
| shengxiao_emoji | string | 生肖 emoji |
| xingzuo | object | 星座详细信息 |
| xingzuo.name | string | 星座中文名，如 天秤座 |
| xingzuo.name_en | string | 星座英文名，如 Libra |
| xingzuo.date_range | string | 日期范围，如 9.23-10.23 |
| xingzuo.element | string | 元素，如 风象 |
| xingzuo.ruler | string | 守护星，如 金星 |
| year_ganzhi | object | 年柱干支 |
| month_ganzhi | object | 月柱干支 |
| day_ganzhi | object | 日柱干支 |
| *.ganzhi | string | 干支，如 乙巳 |
| *.gan | string | 天干，如 乙 |
| *.zhi | string | 地支，如 巳 |
| *.nayin | string | 纳音，如 佛灯火 |
| almanac | object | 黄历信息 |
| almanac.yi | string[] | 宜 |
| almanac.ji | string[] | 忌 |
| almanac.chong_gan | string | 冲天干 |
| almanac.chong_zhi | string | 冲地支 |
| almanac.chong_shengxiao | string | 冲生肖 |
| almanac.chong_desc | string | 冲描述，如 (丁酉)鸡 |
| almanac.sha | string | 煞方 |
| almanac.taishen | string | 胎神占方 |
| almanac.wuxing_nayin | string | 五行纳音 |
| almanac.pengzu | string | 彭祖百忌 |
| almanac.jishen | string[] | 吉神 |
| almanac.xiongsha | string[] | 凶煞 |
| almanac.zhixing | string | 建除十二值星 |
| almanac.tianshen | string | 值日天神 |
| almanac.tianshen_type | string | 天神类型 |
| almanac.position_cai | string | 财神方位 |
| almanac.position_xi | string | 喜神方位 |
| almanac.position_fu | string | 福神方位 |
| almanac.position_yanggui | string | 阳贵方位 |
| almanac.position_yingui | string | 阴贵方位 |
| almanac.liuyao | string | 六曜 |
| almanac.wuhou | string | 七十二候 |
| almanac.xiu | string | 二十八星宿 |
| almanac.xiu_luck | string | 星宿吉凶 |
| solar_term_prev | object/null | 前一节气（名称、日期、是否为节） |
| solar_term_next | object/null | 后一节气 |
| solar_term_current | object/null | 当天节气（非节气日为 null） |

**响应示例**

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
    "year_ganzhi": {"ganzhi": "乙巳", "gan": "乙", "zhi": "巳", "nayin": "佛灯火"},
    "month_ganzhi": {"ganzhi": "乙酉", "gan": "乙", "zhi": "酉", "nayin": "泉中水"},
    "day_ganzhi": {"ganzhi": "庚辰", "gan": "庚", "zhi": "辰", "nayin": "白蜡金"},
    "almanac": {
      "yi": ["祭祀", "出行"],
      "ji": ["开市", "安葬"],
      "chong_gan": "壬",
      "chong_zhi": "戌",
      "chong_shengxiao": "狗",
      "chong_desc": "(壬戌)狗",
      "sha": "南",
      "taishen": "占门碓外东南",
      "wuxing_nayin": "白蜡金",
      "pengzu": "庚不经络织机虚张，辰不哭泣必主重丧",
      "jishen": ["天恩", "母仓"],
      "xiongsha": ["天罡", "劫煞"],
      "zhixing": "定",
      "tianshen": "玉堂",
      "tianshen_type": "吉神",
      "position_cai": "正东",
      "position_xi": "西北",
      "position_fu": "西南",
      "position_yanggui": "正南",
      "position_yingui": "东南",
      "liuyao": "先胜",
      "wuhou": "鸿雁来宾",
      "xiu": "角",
      "xiu_luck": "吉"
    },
    "solar_term_prev": {"name": "秋分", "date": "2025-09-23", "is_jie": true},
    "solar_term_next": {"name": "寒露", "date": "2025-10-08", "is_jie": false},
    "solar_term_current": null
  }
}
```

---

### 3. 查询指定日期假日信息

| 项目 | 说明 |
|------|------|
| 路径 | `GET /public-china-holiday/holiday/query` |
| 鉴权 | 是 |
| 说明 | 查询指定日期是否为法定假日、假日名称、是否调休上班等 |

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 是 | 日期，格式 YYYY-MM-DD |
| lang | string | 否 | 输出语言：zh/en/ja/ko/vi/es/fr/de，默认 zh |

**请求示例**

```
GET /public-china-holiday/holiday/query?date=2025-10-01
GET /public-china-holiday/holiday/query?date=2025-10-01&lang=ja
```

**响应字段（data）**

| 字段 | 类型 | 说明 |
|------|------|------|
| date | string | 日期，YYYY-MM-DD |
| is_holiday | bool | 是否为法定假日 |
| is_workday | bool | 是否为工作日（调休上班日也算工作日） |
| name | string | 假日名称或空（工作日） |

**响应示例**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "date": "2025-10-01",
    "is_holiday": true,
    "is_workday": false,
    "name": "国庆节"
  }
}
```

---

### 4. 获取年度假日列表

| 项目 | 说明 |
|------|------|
| 路径 | `GET /public-china-holiday/holiday/list` |
| 鉴权 | 是 |
| 说明 | 返回指定年份所有法定假日及调休安排 |

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| year | int | 是 | 年份，范围 1949-2100 |
| lang | string | 否 | 输出语言：zh/en/ja/ko/vi/es/fr/de，默认 zh |

**请求示例**

```
GET /public-china-holiday/holiday/list?year=2025
GET /public-china-holiday/holiday/list?year=2025&lang=en
```

**响应字段（data）**

| 字段 | 类型 | 说明 |
|------|------|------|
| total | int | 假日总数 |
| year | int | 查询年份 |
| month | int/null | 查询月份（全年查询时为 null） |
| holidays | array | 假日列表 |
| holidays[].date | string | 日期，YYYY-MM-DD |
| holidays[].name | string | 假日名称 |

**响应示例**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 14,
    "year": 2025,
    "month": null,
    "holidays": [
      {"date": "2025-01-01", "name": "元旦"},
      {"date": "2025-01-28", "name": "春节"},
      {"date": "2025-01-29", "name": "春节"},
      {"date": "2025-10-01", "name": "国庆节"},
      {"date": "2025-10-02", "name": "国庆节"},
      {"date": "2025-10-03", "name": "国庆节"}
    ]
  }
}
```

---

### 5. 判断是否为工作日

| 项目 | 说明 |
|------|------|
| 路径 | `GET /public-china-holiday/workday` |
| 鉴权 | 是 |
| 说明 | 判断指定日期是否为工作日，返回原因（法定假日/周末/调休上班等） |

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 是 | 公历日期，格式 YYYY-MM-DD |
| lang | string | 否 | 输出语言：zh/en/ja/ko/vi/es/fr/de，默认 zh |

**请求示例**

```
GET /public-china-holiday/workday?date=2025-10-01
GET /public-china-holiday/workday?date=2025-10-01&lang=en
```

**响应字段（data）**

| 字段 | 类型 | 说明 |
|------|------|------|
| date | string | 查询日期 |
| is_workday | bool | 是否为工作日 |
| reason | string | 原因说明 |

**响应示例**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "date": "2025-10-01",
    "is_workday": false,
    "reason": "法定假日：国庆节"
  }
}
```

---

### 6. 工作日计算

| 项目 | 说明 |
|------|------|
| 路径 | `GET /public-china-holiday/workday/calculate` |
| 鉴权 | 是 |
| 说明 | 两种模式：① 推算目标日期（传入 workdays）② 计算工作日数量（传入结束日期） |

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| start_date | string | 是 | 起始日期，格式 YYYY-MM-DD |
| workdays | int | 条件 | 推算模式：要增加的工作日天数（正数=未来，负数=过去） |
| end_date | string | 条件 | 计数模式：结束日期，格式 YYYY-MM-DD |
| lang | string | 否 | 输出语言：zh/en/ja/ko/vi/es/fr/de，默认 zh |

> `workdays` 和 `end_date` 二选一。

**推算模式请求示例**

```
GET /public-china-holiday/workday/calculate?start_date=2025-10-08&workdays=10
```

**推算模式响应示例**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "start_date": "2025-10-08",
    "end_date": "2025-10-22",
    "workdays": 10,
    "total_days": null
  }
}
```

**计数模式请求示例**

```
GET /public-china-holiday/workday/calculate?start_date=2025-10-01&end_date=2025-10-31
```

**计数模式响应示例**

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

---

### 7. 二十四节气列表

| 项目 | 说明 |
|------|------|
| 路径 | `GET /public-china-holiday/solar-term/list` |
| 鉴权 | 是 |
| 说明 | 返回指定年份全部 24 个节气（名称、日期、是否为「节」） |

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| year | int | 是 | 年份 |
| lang | string | 否 | 输出语言：zh/en/ja/ko/vi/es/fr/de，默认 zh |

**请求示例**

```
GET /public-china-holiday/solar-term/list?year=2025
GET /public-china-holiday/solar-term/list?year=2025&lang=de
```

**响应字段（data）**

| 字段 | 类型 | 说明 |
|------|------|------|
| year | int | 查询年份 |
| terms | array | 节气列表，按日期排序 |
| terms[].name | string | 节气名称，如 小寒 |
| terms[].date | string | 节气日期，YYYY-MM-DD |
| terms[].is_jie | bool | 是否为「节」（false 为「气」） |

**响应示例**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "year": 2025,
    "terms": [
      {"name": "小寒", "date": "2025-01-05", "is_jie": true},
      {"name": "大寒", "date": "2025-01-20", "is_jie": false},
      {"name": "立春", "date": "2025-02-03", "is_jie": true}
    ]
  }
}
```

---

### 8. 查询当前节气信息

| 项目 | 说明 |
|------|------|
| 路径 | `GET /public-china-holiday/solar-term/current` |
| 鉴权 | 是 |
| 说明 | 返回指定日期的前一节气、后一节气，以及当天是否为节气 |

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| date | string | 是 | 公历日期，格式 YYYY-MM-DD |
| lang | string | 否 | 输出语言：zh/en/ja/ko/vi/es/fr/de，默认 zh |

**请求示例**

```
GET /public-china-holiday/solar-term/current?date=2025-10-08
GET /public-china-holiday/solar-term/current?date=2025-10-08&lang=fr
```

**响应字段（data）**

| 字段 | 类型 | 说明 |
|------|------|------|
| date | string | 查询日期 |
| prev | object/null | 前一节气 |
| next | object/null | 后一节气 |
| current | object/null | 当天节气（非节气日为 null） |

**响应示例**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "date": "2025-10-08",
    "prev": {"name": "秋分", "date": "2025-09-23", "is_jie": true},
    "next": {"name": "霜降", "date": "2025-10-23", "is_jie": false},
    "current": {"name": "寒露", "date": "2025-10-08", "is_jie": false}
  }
}
```

---

## 接口总览表

| # | 方法 | 路径 | 说明 | 鉴权 |
|---|------|------|------|------|
| 1 | GET | `/health` | 健康检查 | 否 |
| 2 | GET | `/public-china-holiday/date` | 日期综合查询（农历+生肖+星座+干支+黄历+节气） | 是 |
| 3 | GET | `/public-china-holiday/holiday/query` | 查询指定日期假日信息 | 是 |
| 4 | GET | `/public-china-holiday/holiday/list` | 获取年度假日列表 | 是 |
| 5 | GET | `/public-china-holiday/workday` | 判断是否为工作日 | 是 |
| 6 | GET | `/public-china-holiday/workday/calculate` | 工作日计算（推算/计数） | 是 |
| 7 | GET | `/public-china-holiday/solar-term/list` | 二十四节气列表 | 是 |
| 8 | GET | `/public-china-holiday/solar-term/current` | 查询当前节气信息 | 是 |

## 错误码

| code | message | 说明 |
|------|---------|------|
| 200 | success | 请求成功 |
| 400 | 参数错误信息 | 请求参数校验失败（如无效的语言代码） |
| 401 | 鉴权凭证无效 | 缺少或错误的 X-RapidAPI-Proxy-Secret |
| 403 | 权限不足 | 如非开发环境调用刷新接口 |
| 404 | 资源不存在 | 如查询的年份假日数据尚未发布 |
| 422 | 参数校验失败 | 请求参数格式不合法（如日期格式错误） |
| 500 | 服务异常信息 | 服务端内部错误 |
