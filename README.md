# China Public Holiday & Multilingual Calendar API

> China Public Holiday & Multilingual Calendar API — Provides query and calculation services for Chinese mainland public holidays, workdays, lunar calendar, Chinese zodiac, Western zodiac, Heavenly Stems & Earthly Branches (Gan-Zhi), traditional almanac (Huangli), and 24 Solar Terms. Supports 8 languages.

**Live URL:** `https://china-holiday-api.vercel.app`

**Supported Languages:** `zh` (Chinese) | `en` (English) | `ja` (Japanese) | `ko` (Korean) | `vi` (Vietnamese) | `es` (Spanish) | `fr` (French) | `de` (German)

**Data Source:** Official notices from the General Office of the State Council of China, automatically fetched and updated.

---

## Features

- **Public Holidays** — Query specific-date holiday info or annual holiday lists (2018–2026), including makeup workdays
- **Workday Calculator** — Check if a date is a workday, or calculate target dates / count workdays between two dates
- **Lunar Calendar** — Full lunar date conversion with month/day Chinese names
- **Chinese Zodiac** — Zodiac animal, emoji, and compatibility info
- **Western Zodiac** — Constellation name (CN/EN), date range, element, ruling planet
- **Gan-Zhi (干支)** — Year/Month/Day pillars with Heavenly Stems, Earthly Branches, and Five Elements Nayin
- **Traditional Almanac (黄历)** — Yi/Ji (auspicious/inauspicious activities), Chong/Sha, Tai Shen, Peng Zu Bai Ji, Ji Shen, Xiong Sha, Zhi Xing, Tian Shen, positions (Cai/Xi/Fu/Yang Gui/Yin Gui), Liu Yao, Wu Hou, and 28 Mansions
- **24 Solar Terms** — Full year list and current-term query with Jie/Qi distinction
- **8-Language i18n** — Consistent field schema across all languages; `*_py` pinyin reference fields for deep cultural terms

---

## Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/your-username/china-holiday-api.git
cd china-holiday-api
pip install -r requirements.txt
```

### Run Locally

```bash
python run.py
```

The server starts at `http://localhost:8080`.

### Configuration

Copy `.env.example` to `.env` and configure:

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_PORT` | Server port | `8080` |
| `DEBUG` | Debug mode (skips auth when true) | `false` |
| `RAPIDAPI_PROXY_SECRET` | RapidAPI proxy secret for auth | — |
| `ADMIN_TOKEN` | Admin token for refresh endpoint | — |
| `RATE_LIMIT` | Requests per minute per key | `120` |
| `CACHE_TTL` | Holiday data cache TTL in seconds | `86400` (24h) |

---

## API Overview

All business endpoints require `X-RapidAPI-Key` header. Health check is unauthenticated.

| # | Method | Endpoint | Description | Auth |
|---|--------|----------|-------------|------|
| 1 | GET | `/health` | Health check | No |
| 2 | GET | `/public-china-holiday/date` | Comprehensive date query (lunar, zodiac, gan-zhi, almanac, solar terms) | Yes |
| 3 | GET | `/public-china-holiday/holiday/query` | Query holiday info for a specific date | Yes |
| 4 | GET | `/public-china-holiday/holiday/list` | Get annual holiday list | Yes |
| 5 | POST | `/public-china-holiday/holiday/refresh` | Refresh holiday cache (admin only) | Yes |
| 6 | GET | `/public-china-holiday/workday` | Check if a date is a workday | Yes |
| 7 | GET | `/public-china-holiday/workday/calculate` | Calculate workdays or target date | Yes |
| 8 | GET | `/public-china-holiday/solar-term/list` | Get 24 solar terms for a year | Yes |
| 9 | GET | `/public-china-holiday/solar-term/current` | Get current solar term info | Yes |

> Full API documentation with request/response examples: [API.md](API.md)

---

## Usage Examples

### Check if a date is a workday

```bash
curl -H "X-RapidAPI-Key: YOUR_KEY" \
  "https://china-holiday-api.vercel.app/public-china-holiday/workday?date=2025-10-01"
```

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

### Get full date info with almanac (English)

```bash
curl -H "X-RapidAPI-Key: YOUR_KEY" \
  "https://china-holiday-api.vercel.app/public-china-holiday/date?date=2025-10-01&lang=en"
```

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
    "shengxiao": "Snake",
    "shengxiao_py": "She",
    "shengxiao_emoji": "🐍",
    "xingzuo": {
      "name": "Libra",
      "name_en": "Libra",
      "date_range": "9.23-10.23",
      "element": "Air",
      "ruler": "Venus"
    },
    "year_ganzhi": {
      "ganzhi": "Yi Si",
      "ganzhi_py": "Yi Si",
      "gan": "Yi",
      "gan_py": "Yi",
      "zhi": "Si",
      "zhi_py": "Si",
      "nayin": "Fu Deng Huo",
      "nayin_py": "Fu Deng Huo"
    },
    "almanac": {
      "yi": ["Ji Si", "Chu Xing", "Guan Ji", "Jia Qu"],
      "yi_py": ["Ji Si", "Chu Xing", "Guan Ji", "Jia Qu"],
      "ji": ["Kai Shi", "Dong Tu", "Po Tu"],
      "ji_py": ["Kai Shi", "Dong Tu", "Po Tu"],
      "chong_desc": "(Xin Wei)Goat",
      "chong_desc_py": "(Xin Wei) Yang",
      "sha": "East",
      "sha_py": "Dong"
    }
  }
}
```

### Calculate workdays

```bash
# Forward: 5 workdays from 2025-09-28
curl -H "X-RapidAPI-Key: YOUR_KEY" \
  "https://china-holiday-api.vercel.app/public-china-holiday/workday/calculate?start_date=2025-09-28&workdays=5"
```

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

---

## Multilingual Support

All business endpoints accept a `lang` query parameter:

| Code | Language | Coverage |
|------|----------|----------|
| `zh` | Chinese | Original Chinese output with `*_py` pinyin reference |
| `en` | English | Common terms translated; deep cultural terms use pinyin |
| `ja` | Japanese | Common terms translated; deep cultural terms prefer JP dictionary, fallback to pinyin |
| `ko` | Korean | Common terms translated; deep cultural terms prefer KO dictionary, fallback to pinyin |
| `vi` | Vietnamese | Common terms translated; deep cultural terms prefer VI dictionary, fallback to pinyin |
| `es` | Spanish | Common terms translated; deep cultural terms use pinyin |
| `fr` | French | Common terms translated; deep cultural terms use pinyin |
| `de` | German | Common terms translated; deep cultural terms use pinyin |

### Translation Strategy

- **L1 — General text**: Direct translation (holiday names, zodiac, constellation elements, solar terms)
- **L2 — East Asian cultural terms**: Dictionary-based translation for ja/ko/vi (almanac yi/ji, jishen, xiongsha, zhixing, liuyao, tianshen)
- **L3 — Deep cultural terms**: Main field outputs translated/pinyin text; `*_py` field provides pinyin reference for all languages
- **Schema consistency**: The same endpoint returns identical field sets regardless of `lang` parameter

---

## Project Structure

```
├── api/index.py              # Vercel entry point
├── app/
│   ├── api/v1/               # Route handlers (holiday, date, workday, solar_term)
│   ├── common/               # Shared utilities (validators)
│   ├── core/                 # Config, exceptions, logging, response helpers
│   ├── models/               # Pydantic request/response models
│   ├── services/
│   │   ├── cn_datekit/       # Business logic (holiday, lunar, zodiac, almanac, workday, solar_term)
│   │   └── i18n/             # Multilingual translation (locale dictionary + engine)
│   ├── data/holidays/        # Local holiday JSON cache (gitignored)
│   └── main.py               # FastAPI app factory
├── run.py                    # Local development runner
├── vercel.json               # Vercel deployment config
├── requirements.txt          # Python dependencies
├── API.md                    # Full API documentation
└── README.md                 # This file
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| ASGI Server | Uvicorn |
| Validation | Pydantic v2 |
| Lunar Calendar | [lunar_python](https://github.com/6tail/lunar-python) |
| Pinyin | pypinyin |
| Rate Limiting | slowapi |
| HTTP Client | httpx |
| Deployment | Vercel (Serverless) |
| Platform | RapidAPI |

---

## Deployment

### Vercel (Production)

The project is configured for Vercel serverless deployment:

```bash
vercel deploy --prod
```

The `api/index.py` entry point exposes the FastAPI app. All requests are proxied through `vercel.json` routes.

### Environment Variables (Vercel)

Set these in the Vercel project settings:

- `RAPIDAPI_PROXY_SECRET`
- `ADMIN_TOKEN`
- `DEBUG=false`
- `RATE_LIMIT=120`

---

## License

MIT
