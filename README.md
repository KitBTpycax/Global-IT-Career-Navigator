# Global IT Career Navigator

An intelligent, multi-axis **Decision Support System (DSS)** for selecting the optimal IT career specialisation. The system matches a user's five-axis preference vector against a curated database of career tracks using **Weighted Euclidean Distance**, renders live radar visualisations, and surfaces real-time job market data.

Built with **Django 5+**, Chart.js 4.4.1, Tailwind CSS, and Vanilla JavaScript.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Mathematical Model](#mathematical-model)
4. [Setup & Installation](#setup--installation)
5. [Environment Variables](#environment-variables)
6. [Database Seeding](#database-seeding)
7. [Running Tests](#running-tests)
8. [API Reference](#api-reference)
9. [Technology Stack](#technology-stack)

---

## Project Overview

**Global IT Career Navigator** solves one concrete problem: given a user's five numerical preferences (learning intensity, financial ambition, visual vs. systems thinking, company culture, and stress tolerance), surface the most suitable IT career tracks, ranked by mathematical proximity.

Key capabilities:

- Five interactive sliders (scale 1–10), each mapping to one DSS axis.
- Real-time radar chart updated on every slider move (no page reload).
- Top-3 recommendations with personalised matching reasons and salary ranges.
- Five regional salary markets: Global, USA, Europe, UK, Ukraine.
- Live job market feed via a public API (Remotive) with a 6-hour TTL cache and graceful fallback to reference benchmarks.
- Full detail page per track: radar overlay (user vs. track), salary matrix, roadmap, pros/cons, tech stack.

---

## Architecture

```
webchik/
├── core/                                  # Django project configuration
│   ├── settings.py                        # Settings loaded from environment / .env
│   ├── urls.py                            # Root URL router
│   ├── wsgi.py
│   └── asgi.py
│
├── navigator/                             # Main application
│   ├── models.py                          # CareerTrack, MarketCache (JSONField)
│   ├── services.py                        # DSS engine + market cache service
│   ├── views.py                           # Page views + /api/match/ endpoint
│   ├── urls.py                            # App URL patterns
│   ├── tests.py                           # Comprehensive test suite
│   ├── templatetags/
│   │   └── navigator_tags.py              # Custom template filters (get_item)
│   └── management/commands/
│       └── seed_db.py                     # Data seeding command
│
├── static/
│   ├── css/style.css                      # Custom sliders, glassmorphism, animations
│   └── js/app.js                          # Radar charts, slider logic, fetch + CSRF
│
├── templates/
│   ├── base.html                          # Base layout (Tailwind, Chart.js CDN)
│   ├── index.html                         # Landing page: sliders, radar, top-3
│   └── results.html                       # Career track detail page
│
├── .env.example                           # Environment template
├── requirements.txt
└── manage.py
```

### Key design decisions

| Decision | Rationale |
|---|---|
| `json_script` filter for all float data in templates | `LANGUAGE_CODE = 'uk'` causes Django to render `5.5` as `5,5` inside raw `<script>` tags, breaking JS. `json_script` uses Python `json.dumps()`, which always produces dot-notation floats. |
| `@ensure_csrf_cookie` on HTML views | Guarantees the `csrftoken` cookie is always set, so the JavaScript `fetch` can read and attach `X-CSRFToken`. |
| No `@csrf_exempt` on `/api/match/` | All state-changing POST requests are CSRF-protected. |
| 6-hour TTL on `MarketCache` | Avoids hammering the external API on every page load while keeping market data reasonably fresh. |
| `update_or_create` only on cache miss or stale data | No DB writes on normal cached GET requests. |

---

## Mathematical Model

### Weighted Euclidean Distance

Each career track and each user preference vector lives in a five-dimensional space $\mathbb{R}^5$ where every axis is clamped to $[1, 10]$.

**Distance:**

$$d(u, t) = \sqrt{\sum_{i=1}^{5} w_i \cdot (u_i - t_i)^2}$$

**Match ratio:**

$$\text{match} = \max\!\left(0,\; 1 - \frac{d(u,t)}{d_{\max}}\right)$$

where $d_{\max} = \sqrt{\sum_i w_i \cdot (10 - 1)^2} = \sqrt{5} \cdot 9 \approx 20.12$ (all weights currently equal 1.0).

**Match percentage:**

$$\text{match\%} = \text{round}(\text{match} \times 100,\; 1)$$

Tracks are sorted strictly by `raw_distance` ascending (closest = best match = rank 1).

### The five axes

| # | Key | 1 (low) | 10 (high) |
|---|-----|---------|-----------|
| 1 | `learning_curve` | Easy entry, quick start | Deep CS, algorithms, maths |
| 2 | `financial_vector` | Stable mid-range salary | Maximum Senior cap, global market |
| 3 | `architecture_visual` | Low-level / server-side | UI/UX, visual interfaces |
| 4 | `company_scale` | Big enterprise, rigid processes | Startups, full autonomy |
| 5 | `stress_wlb` | Balanced schedule, low stress | High challenge, on-call, fast pace |

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/Global-IT-Career-Navigator.git
cd Global-IT-Career-Navigator

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
copy .env.example .env
# Edit .env as needed (see Environment Variables below)

# 5. Apply database migrations
python manage.py migrate

# 6. Seed the database with 10 career tracks
python manage.py seed_db

# 7. Start the development server
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

---

## Environment Variables

Copy `.env.example` to `.env` and adjust the values:

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `django-insecure-...` | Django secret key. **Change in production.** |
| `DEBUG` | `True` | Set to `False` in production. |
| `ALLOWED_HOSTS` | `*` | Comma-separated list of allowed hostnames. |
| `EXTERNAL_MARKET_API_URL` | Remotive API URL | Public jobs feed endpoint. |

---

## Database Seeding

```bash
python manage.py seed_db
```

This command is idempotent — running it multiple times is safe. It creates or updates:

- **10 `CareerTrack` objects** with balanced radar profiles spread across the full $[1.5, 9.8]$ range on all five axes.
- **5 `MarketCache` objects** with reference benchmarks for each supported region.

Tracks currently seeded:

| Track | Category |
|---|---|
| Python Backend Engineer | Backend & Cloud |
| Frontend / UI Engineer | Frontend & Design |
| DevOps & Cloud Infrastructure | DevOps & Cloud |
| AI / ML Engineer | AI & Data Science |
| Data Engineer & Analytics | AI & Data Science |
| Cybersecurity Engineer | Security |
| QA Automation Engineer | QA & Testing |
| Mobile Developer (iOS/Android) | Mobile |
| Fullstack Web Developer | Fullstack |
| Embedded & Systems Engineer | Low-Level & Systems |

---

## Running Tests

```bash
python manage.py test
```

The test suite (`navigator/tests.py`) covers:

| Area | Test cases |
|---|---|
| **DSS Math** | Closest track ranks first, perfect match = 100%, sorted by distance, 0–100% range, `?learn=0` clamped to 1.0 |
| **Input validation** | `[]` body → 400, `"string"` body → 400, invalid JSON → 400, non-dict `sliders` → 400, non-numeric slider value → 400, GET request → 405 |
| **CSRF protection** | POST without `X-CSRFToken` → 403 |
| **Market cache TTL** | API called once on cold start, skipped within TTL, called again when stale (>6h), no extra DB writes on cache hits |
| **`json_script` float safety** | `detail-track-data` contains valid JSON with dot-decimal floats even under `LANGUAGE_CODE='uk'` |
| **Views** | Index 200, detail 200/404, region filter, `initial-sliders-data` present, null user_vector when no query params |

---

## API Reference

### `POST /api/match/`

Returns ranked career tracks for the given user vector.

**Request headers:**

```
Content-Type: application/json
X-CSRFToken: <token from csrftoken cookie>
```

**Request body:**

```json
{
  "sliders": {
    "learning_curve": 7.0,
    "financial_vector": 8.5,
    "architecture_visual": 2.0,
    "company_scale": 5.0,
    "stress_wlb": 6.0
  },
  "region": "usa"
}
```

**Success response `200`:**

```json
{
  "status": "success",
  "region": "usa",
  "currency_symbol": "$",
  "top_matches": [ /* top 3 tracks */ ],
  "all_matches":  [ /* all 10 tracks sorted by proximity */ ],
  "trends": { /* market data for the region */ }
}
```

**Error responses:**

| Status | Cause |
|---|---|
| `400` | Malformed JSON, body is a list/scalar, `sliders` is not an object, non-numeric slider value |
| `403` | Missing or invalid CSRF token |
| `405` | Non-POST request |

---

### `GET /api/trends/`

Returns market analytics for a region.

**Query parameters:** `region` (default: `global`)

**Response `200`:**

```json
{
  "status": "success",
  "region": "europe",
  "trends": {
    "active_vacancies": "85,000+",
    "demand_index": 88,
    "remote_share": "71%",
    "avg_growth": "+12.8%",
    "hot_skill": "Data Governance, Rust & Microservices",
    "market_sentiment": "...",
    "is_live": false,
    "feed_source": "Regional Reference Benchmark",
    "feed_status": "Reference Baseline"
  },
  "meta": { "name": "Europe (ЄС та Швейцарія)", "currency": "EUR", "symbol": "€" }
}
```

---

### `GET /career/<slug>/`

Detail page for a specific career track. Optionally accepts query parameters to overlay the user's vector on the track radar:

| Param | Axis |
|---|---|
| `learn` | `learning_curve` |
| `fin` | `financial_vector` |
| `arch` | `architecture_visual` |
| `scale` | `company_scale` |
| `stress` | `stress_wlb` |

All params are clamped to `[1.0, 10.0]`. A value of `0` is clamped to `1.0` (not treated as absent).

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Django 5+, Django ORM (SQLite / PostgreSQL) |
| DSS Engine | Pure Python — Weighted Euclidean Distance |
| Data Models | `CareerTrack`, `MarketCache` with `models.JSONField` |
| Frontend | HTML5, Tailwind CSS (JIT CDN), Vanilla JavaScript (ES2020) |
| Charts | Chart.js 4.4.1 — Radar (multi-axis, strict 1–10 scale) |
| External API | Remotive public jobs feed (no auth required) |
| Security | Django CSRF middleware, `ensure_csrf_cookie`, `json_script` XSS protection |
