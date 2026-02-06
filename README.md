# Healthcare Scale Platform 🌷

A full-stack web application for healthcare assessment scales, specifically designed for mental health screening in elderly populations. 

## 🏗️ **Architecture**

**Backend (Python 32.8%)**: FastAPI-based REST API with SQLite database
**Frontend (JavaScript 43.9%)**: React SPA with React Router and Axios
**Styling (CSS 22.3%)**: Custom CSS with responsive design
**Templates (HTML 1%)**: Basic HTML structure

## ✨ **Key Features**

- 📋 Dynamic scale loading from JSON definitions
- 🎯 Real-time progress tracking during assessments
- 💾 SQLite database for persistent storage of assessments
- 🔄 RESTful API with versioned scale support
- 📊 Automated scoring with interpretation
- 🌐 Responsive UI with Chinese (Traditional) localization

## 🗂️ **Current Project Structure**

```
healthcare-scale-platform/
├── app/                          # FastAPI Backend
│   ├── main.py                   # Application entry point
│   ├── core/
│   │   ├── db.py                 # Database connection & initialization
│   │   └── schema.sql            # SQLite schema
│   │   └── scale.py              # Pydantic models for scales & responses
│   ├── services/
│   │   ├── assessment_service.py # Assessment CRUD operations
│   │   ├── scale_loader.py       # JSON scale file loader
│   │   └── scoring.py            # Scoring algorithm with reverse items
│   └── routers/
│       └── api.py                # API endpoints (/api/scales/*)
│
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── App.jsx               # Main app component with routing
│   │   ├── main.jsx              # React entry point
│   │   ├── index.css             # Global styles
│   │   ├── pages/
│   │   │   ├── HomePage.jsx      # Landing page with scale selection
│   │   │   ├── ScalePage.jsx     # Assessment form page
│   │   │   └── ResultPage.jsx    # Results display page
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Header.jsx    # Navigation header
│   │   │   │   ├── Loading.jsx   # Loading spinner
│   │   │   │   └── ErrorMessage.jsx
│   │   │   └── scale/
│   │   │       ├── ScaleForm.jsx      # Form with progress bar
│   │   │       ├── ScaleQuestion.jsx  # Individual question component
│   │   │       └── ResultDisplay.jsx  # Score & interpretation display
│   │   ├── services/
│   │   │   └── api.js            # Axios HTTP client
│   │   └── utils/
│   │       └── logger.js         # Development logging utility
│   ├── vite.config.js            # Vite config with proxy to backend
│   ├── package.json              # Dependencies (React 19, Axios, Router)
│   └── index.html                # HTML entry point
│
├── scales/                       # Scale Definitions (JSON)
│   └── GDS-15.json              # Geriatric Depression Scale
│
├── .gitignore                    # Python, Node, DB files
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```