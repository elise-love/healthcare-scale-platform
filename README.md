# Healthcare Scale Platform 🌷

A full-stack web application for healthcare assessment scales, specifically designed for mental health screening in elderly populations. 

## 🏗️ **Architecture**

**Backend (Python)**: FastAPI-based REST API with SQLite database  
**Frontend (JavaScript)**: React SPA with React Router and Axios  
**Styling (CSS)**: Custom CSS with responsive design  
**Auth**: JWT stored in HttpOnly cookies, bcrypt password hashing, email verification

## ✨ **Key Features**

- 📋 Dynamic scale loading from JSON definitions
- 🎯 Real-time progress tracking during assessments
- 💾 SQLite database for persistent storage of assessments
- 🔄 RESTful API with versioned scale support
- 📊 Automated scoring with interpretation
- 🌐 Responsive UI with Chinese (Traditional) localization
- 🔐 JWT-based authentication with HttpOnly cookies
- 📧 Email verification (dev-friendly token in API response)

## 🗂️ **Current Project Structure**

```
healthcare-scale-platform/
├── app/                          # FastAPI Backend
│   ├── main.py                   # Application entry point
│   ├── core/
│   │   ├── db.py                 # Database connection & initialization
│   │   ├── schema.sql            # SQLite schema (includes users + tokens)
│   │   └── config.py             # JWT / cookie settings
│   ├── models/
│   │   └── scale.py              # Pydantic models for scales & responses
│   ├── services/
│   │   ├── assessment_service.py # Assessment CRUD operations
│   │   ├── scale_loader.py       # JSON scale file loader
│   │   └── scoring.py            # Scoring algorithm with reverse items
│   └── routers/
│       ├── api.py                # Scale endpoints (/api/scales/*)
│       └── auth.py               # Auth endpoints (/api/auth/*)
│
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── App.jsx               # Main app component with routing
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── ScalePage.jsx
│   │   │   ├── ResultPage.jsx
│   │   │   ├── LoginPage.jsx     # ← new
│   │   │   ├── RegisterPage.jsx  # ← new
│   │   │   └── VerifyEmailPage.jsx # ← new
│   │   ├── components/common/
│   │   │   └── Header.jsx        # Navigation (Login + Register links)
│   │   └── services/
│   │       └── api.js            # Axios client (withCredentials + auth fns)
│   └── vite.config.js            # Vite config with proxy to backend
│
├── scales/
│   └── GDS-15.json
├── requirements.txt              # Python dependencies
└── README.md
```

---

## 🚀 **Local Development — Step-by-step**

### 1. Start the backend

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run FastAPI server (will auto-init SQLite DB on first start)
python -m uvicorn app.main:app --reload
# → http://127.0.0.1:8000
```

### 2. Start the frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:3002  (Vite proxies /api → http://127.0.0.1:8000)
```

---

## 🔐 **Auth Flow — Happy Path**

### Step 1 — Register

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "password": "secret123"}'
# Response includes `verification_token` (dev mode)
```

### Step 2 — Verify email

```bash
curl -X POST http://127.0.0.1:8000/api/auth/verify \
  -H "Content-Type: application/json" \
  -d '{"token": "<verification_token from step 1>"}'
```

### Step 3 — Login (sets HttpOnly cookie)

```bash
curl -sc /tmp/cookies.txt -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "password": "secret123"}'
```

### Step 4 — Submit a scale response (requires login cookie)

```bash
curl -sb /tmp/cookies.txt -X POST http://127.0.0.1:8000/api/scales/GDS-15/responses \
  -H "Content-Type: application/json" \
  -d '{
    "answers": {
      "gds15_q01": 1, "gds15_q02": 0, "gds15_q03": 1,
      "gds15_q04": 0, "gds15_q05": 0, "gds15_q06": 1,
      "gds15_q07": 0, "gds15_q08": 0, "gds15_q09": 0,
      "gds15_q10": 1, "gds15_q11": 0, "gds15_q12": 0,
      "gds15_q13": 0, "gds15_q14": 1, "gds15_q15": 0
    }
  }'
```

---

## ❌ **Negative Tests**

```bash
# Wrong password
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "password": "wrongpassword"}'
# → 401 "密碼錯誤"

# Email not found
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "nobody@example.com", "password": "anything"}'
# → 401 "找不到此電子郵件帳號"

# Login before verifying email
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "unverified@example.com", "password": "secret123"}'
# → 403 "請先完成電子郵件驗證再登入"

# Submit assessment without login
curl -X POST http://127.0.0.1:8000/api/scales/GDS-15/responses \
  -H "Content-Type: application/json" \
  -d '{"answers": {}}'
# → 401 "請先登入再提交評估"

# Register with missing email
curl -X POST http://127.0.0.1:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "", "password": "secret123"}'
# → 422 validation error

# Register with duplicate email
curl -X POST http://127.0.0.1:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "password": "secret123"}'
# → 409 "此電子郵件已被註冊"
```

---

## 🔑 **Auth API Reference**

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | Create account, returns `verification_token` |
| POST | `/api/auth/verify` | Verify email with token |
| POST | `/api/auth/login` | Login → sets `access_token` HttpOnly cookie |
| POST | `/api/auth/logout` | Clear auth cookie |
| GET  | `/api/auth/me` | Get current user from cookie |

JWT is stored as an **HttpOnly** cookie (`access_token`). Frontend never touches it directly — the browser sends it automatically with every request when `withCredentials: true` is set on Axios.