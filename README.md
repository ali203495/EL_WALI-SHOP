# Maison El Wali - Luxury Jewelry Store

A premium e-commerce platform built with **Nuxt 4** (Frontend) and **FastAPI** (Backend).

## 🚀 Quick Start

### 1. Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL (Production) or SQLite (Development)

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Running Scripts
Most scripts are designed to be run from the project root:
```bash
python scripts/verify_full_system.py
```

## 📂 Project Structure

- `frontend/`: Nuxt 4 application.
- `backend/`: FastAPI application with SQLAlchemy (Async).
- `scripts/`: Utility, migration, and system verification scripts.
- `docs/`: Comprehensive guides for deployment, SEO, and integration.

## 🛠️ Key Scripts

| Script | Description |
|--------|-------------|
| `scripts/verify_full_system.py` | Health check for API and integration. |
| `scripts/migrate_to_postgres.py`| Migration tool for SQLite to PostgreSQL. |
| `scripts/audit_frontend.py` | Scans for broken links and NuxtLink issues. |
| `start_servers.sh` | Bash script to run both servers locally. |

## 🌐 Deployment

For detailed instructions, see:
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Production Hardening (Postgres/Cloudinary)](docs/PRODUCTION_GUIDE.md)
- [Domain Setup](docs/DOMAIN_SETUP.md)

---
© 2026 Maison El Wali
