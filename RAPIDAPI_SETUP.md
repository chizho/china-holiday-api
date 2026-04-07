# RapidAPI 上架配置

## 一、API 基本信息

| 配置项 | 内容 |
|--------|------|
| **API 名称** | China Public Holiday & Multilingual Calendar API |
| **简短描述** | China public holidays, lunar calendar, Chinese zodiac, almanac, solar terms & workday calculator with 8-language support |
| **详细描述** | 见下方 |
| **分类** | Data, Finance |
| **关键词** | 见下方 |
| **标签** | 见下方 |
| **Base URL** | `https://china-holiday-api.vercel.app` |
| **协议** | HTTPS (REST) |
| **认证方式** | API Key (X-RapidAPI-Key Header) |

---

## 二、简短描述（Short Description）

> China public holidays, lunar calendar, Chinese zodiac, almanac, solar terms & workday calculator with 8-language support

---

## 三、详细描述（Long Description）

```markdown
# China Public Holiday & Multilingual Calendar API

A comprehensive Chinese calendar API providing **official public holidays**, **lunar calendar conversion**, **Chinese zodiac**, **constellations**, **Heavenly Stems & Earthly Branches**, **Chinese Almanac (Huangli)**, **24 Solar Terms**, and **workday calculations** — all with **8-language multilingual output**.

## ✨ Key Features

### 🇨🇳 Official Public Holidays
- Auto-updated from State Council announcements
- Full coverage: New Year, Spring Festival, Qingming, Labor Day, Dragon Boat, Mid-Autumn, National Day
- Adjusted workday detection (调休)
- Historical data from 2018, yearly updates

### 🌙 Lunar Calendar
- Gregorian ↔ Lunar date conversion
- Full Chinese date representation (干支纪年 + 农历月日)
- Year/Month/Day Heavenly Stems & Earthly Branches with Nayin (五行纳音)

### 🐍 Chinese Zodiac & Western Constellations
- Chinese zodiac animal with emoji
- Western constellation with element, ruling planet, and date range

### 📜 Chinese Almanac (黄历)
- Yi (宜) and Ji (忌) activities
- Clash (冲煞), Fetal God (胎神), Pengzu taboos (彭祖百忌)
- Auspicious deities (吉神) and inauspicious spirits (凶煞)
- 12 Star phases (建除十二值星), Day Guardian Deity
- Wealth/Happiness/Fortune/Noble God directions
- Six Yao (六曜), 72 Pentads (七十二候), 28 Mansions (二十八星宿)

### 🌱 24 Solar Terms
- Complete annual solar term list with Jie (节) / Qi (气) classification
- Current term query with prev/next term lookup

### 💼 Workday Calculator
- Check if a date is a workday (auto-detects holidays, weekends, adjusted days)
- Predict target date after N workdays
- Count workdays between two dates

### 🌍 8-Language Support
All business endpoints support the `lang` parameter:
- `zh` (Chinese), `en` (English), `ja` (Japanese), `ko` (Korean)
- `vi` (Vietnamese), `es` (Spanish), `fr` (French), `de` (German)

## 📊 API Endpoints (9 Total)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check (no auth) |
| GET | `/public-china-holiday/date` | Comprehensive date query |
| GET | `/public-china-holiday/holiday/query` | Holiday info for a date |
| GET | `/public-china-holiday/holiday/list` | Annual holiday list |
| GET | `/public-china-holiday/workday` | Workday check |
| GET | `/public-china-holiday/workday/calculate` | Workday calculation |
| GET | `/public-china-holiday/solar-term/list` | 24 Solar Terms list |
| GET | `/public-china-holiday/solar-term/current` | Current solar term info |

## 🔑 Authentication
All business endpoints require `X-RapidAPI-Key` header. Health check endpoint is unauthenticated for monitoring.

## 🌐 Base URL
`https://china-holiday-api.vercel.app`

## 📦 Response Format
```json
{
  "code": 200,
  "message": "success",
  "data": { ... }
}
```

## ⚡ Use Cases
- **App Development**: Holiday-aware date pickers, Chinese calendar widgets
- **HR/Payroll Systems**: Automatic workday/holiday detection for scheduling
- **E-commerce**: Promotional planning around Chinese holidays
- **Logistics**: Delivery date calculation excluding holidays
- **Education**: Chinese culture and calendar learning tools
- **Finance**: Trading day calculations for Chinese markets
```

---

## 四、关键词（Keywords）

```
china, holiday, calendar, lunar, chinese, public holiday, workday, solar term, zodiac, almanac, huangli, gregorian, date, API, rest, multilingual, i18n, spring festival, mid-autumn, national day, schedule, business day
```

---

## 五、标签（Tags）

```
China, Holiday, Calendar, Lunar Calendar, Public Holiday, Workday, Solar Terms, Zodiac, Almanac, Date API, Chinese Calendar, Multilingual, REST API, Data
```

---

## 六、定价方案（Pricing Plans）

### Plan 1: Free（免费）

| 配置项 | 值 |
|--------|-----|
| 名称 | Free |
| 价格 | $0 / 月 |
| 请求上限 | 100 次/月 |
| 速率限制 | 10 次/分钟 |
| 适用人群 | 个人开发者试用、评估 |

### Plan 2: Basic（基础版）

| 配置项 | 值 |
|--------|-----|
| 名称 | Basic |
| 价格 | $4.99 / 月 |
| 请求上限 | 5,000 次/月 |
| 速率限制 | 30 次/分钟 |
| 适用人群 | 小型应用、个人项目 |

### Plan 3: Pro（专业版）

| 配置项 | 值 |
|--------|-----|
| 名称 | Pro |
| 价格 | $14.99 / 月 |
| 请求上限 | 50,000 次/月 |
| 速率限制 | 120 次/分钟 |
| 适用人群 | 中型企业、生产级应用 |

### Plan 4: Enterprise（旗舰版）

| 配置项 | 值 |
|--------|-----|
| 名称 | Enterprise |
| 价格 | $49.99 / 月 |
| 请求上限 | 无限制 |
| 速率限制 | 300 次/分钟 |
| 适用人群 | 大型企业、高并发场景 |

---

## 七、RapidAPI Hub 填写指南

### 步骤 1: 创建新 API

1. 登录 https://rapidapi.com/hub
2. 点击 "My APIs" → "Add New API"
3. 选择 "New API"

### 步骤 2: 填写基础信息

| 字段 | 填写内容 |
|------|---------|
| API Name | `China Public Holiday & Multilingual Calendar API` |
| Short Description | 复制上方「简短描述」 |
| Long Description | 复制上方「详细描述」中的 Markdown |
| Category | `Data` |
| Website | `https://github.com/chizho/china-holiday-api`（如果公开仓库） |

### 步骤 3: 配置 Base URL

| 字段 | 值 |
|------|-----|
| Base URL | `https://china-holiday-api.vercel.app` |

### 步骤 4: 导入 OpenAPI 规范

1. 在 API 管理页面选择 "Import OpenAPI"
2. 上传项目根目录的 `openapi.json` 文件
3. 确认导入后，所有接口会自动生成

### 步骤 5: 配置认证

1. 进入 "Security" 标签
2. 选择 "API Key"
3. Header Name: `X-RapidAPI-Key`
4. 勾选所有业务接口（不勾选 `/health`）

### 步骤 6: 设置定价

1. 进入 "Pricing" 标签
2. 添加 4 个 Plan（Free / Basic / Pro / Enterprise）
3. 填写上方表格中的价格和限制

### 步骤 7: 配置关键词和标签

1. 在 "Settings" 中填入关键词和标签
2. 选择 Secondary Category: `Finance`

### 步骤 8: 测试 & 发布

1. 使用 RapidAPI 测试工具验证所有 9 个接口
2. 确认多语言参数 `lang` 正常工作
3. 提交审核

---

## 八、审核注意事项

1. **无违规内容**：API 仅提供日历和假日数据，不涉及任何敏感内容
2. **数据来源合规**：假日数据来自国务院公开发布的公告
3. **响应稳定**：Vercel 部署，全球 CDN 加速
4. **文档完整**：OpenAPI 规范 + 详细描述 + 多语言示例
5. **健康检查端点**：`/health` 无需认证，方便 RapidAPI 巡检
6. **错误处理完善**：所有接口有规范的错误码和错误消息
