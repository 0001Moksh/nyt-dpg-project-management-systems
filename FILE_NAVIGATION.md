# 📍 DPG Project Management System - File Navigation Guide

## 🎯 Start Here

**New to this project?** Start with these files in order:

1. **[README.md](./README.md)** - Project overview and features (5 min read)
2. **[SETUP.md](./SETUP.md)** - Quick start guide (10 min to setup)
3. **[COMPLETION_SUMMARY.md](./COMPLETION_SUMMARY.md)** - What's been built (5 min read)
4. **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Deploy to production (reference as needed)

---

## 📂 Directory Structure & Navigation

### Root Level Files
```
📄 README.md              ← PROJECT OVERVIEW & FEATURES
📄 SETUP.md              ← QUICK START GUIDE (START HERE)
📄 DEPLOYMENT.md         ← PRODUCTION DEPLOYMENT
📄 COMPLETION_SUMMARY.md ← WHAT'S BEEN BUILT
📄 .gitignore            ← Git ignore rules
📄 .env.local            ← Environment template
```

### Backend Directory (`backend/`)
```
backend/
├── 📄 README.md                    ← Backend documentation
├── 📄 requirements.txt             ← Python dependencies
├── 📄 .env                         ← Backend config template
├── 📄 alembic.ini                  ← Database migration config
│
├── app/                            ← Main application code
│   ├── 📄 main.py                  ← FastAPI entry point
│   ├── 📄 __init__.py
│   │
│   ├── core/                       ← Core utilities
│   │   ├── 📄 __init__.py
│   │   ├── 📄 config.py            ← Settings & environment
│   │   └── 📄 security.py          ← JWT, OTP, passwords
│   │
│   ├── models/                     ← Database models
│   │   ├── 📄 __init__.py
│   │   └── 📄 models.py            ← 14 SQLAlchemy models
│   │
│   ├── schemas/                    ← Request/response schemas
│   │   ├── 📄 __init__.py
│   │   └── 📄 schemas.py           ← 20+ Pydantic schemas
│   │
│   ├── services/                   ← Business logic
│   │   ├── 📄 __init__.py
│   │   ├── 📄 auth_service.py      ← Authentication logic
│   │   └── 📄 email_service.py     ← Email & notifications
│   │
│   ├── routes/                     ← API endpoints (7 router files)
│   │   ├── 📄 __init__.py
│   │   ├── 📄 auth.py              ← Auth endpoints (4)
│   │   ├── 📄 admin.py             ← Admin endpoints (4)
│   │   ├── 📄 projects.py          ← Project endpoints (6)
│   │   ├── 📄 teams.py             ← Team endpoints (6)
│   │   ├── 📄 submissions.py       ← Submission endpoints (7)
│   │   ├── 📄 supervisor.py        ← Supervisor endpoints (3)
│   │   └── 📄 chatbot.py           ← Chatbot endpoints (3)
│   │
│   └── db/                         ← Database configuration
│       ├── 📄 __init__.py
│       └── 📄 database.py          ← Connection & session setup
│
└── alembic/                        ← Database migrations
    ├── 📄 alembic.ini              ← Migration config
    ├── 📄 script.py.mako           ← Migration template
    ├── 📄 __init__.py
    └── versions/
        └── 📄 001_initial.py       ← Initial migration
```

**Backend Quick Links:**
- **Main Entry:** [app/main.py](./backend/app/main.py)
- **Database Models:** [app/models/models.py](./backend/app/models/models.py)
- **API Routes:** [app/routes/](./backend/app/routes/)
- **Config:** [app/core/config.py](./backend/app/core/config.py)

### Frontend Directory (`frontend/`)
```
frontend/
├── 📄 README.md                    ← Frontend documentation
├── 📄 package.json                 ← Node.js dependencies
├── 📄 .env.local                   ← Frontend config
├── 📄 tsconfig.json                ← TypeScript config
├── 📄 tailwind.config.ts           ← Tailwind CSS config
├── 📄 postcss.config.js            ← PostCSS config
├── 📄 next.config.js               ← Next.js config
│
├── app/                            ← Next.js App Router
│   ├── 📄 page.tsx                 ← Home page
│   ├── 📄 layout.tsx               ← Root layout
│   ├── 📄 globals.css              ← Global styles
│   │
│   ├── auth/                       ← Authentication pages
│   │   └── login/
│   │       └── 📄 page.tsx         ← Login page
│   │   └── verify-otp/
│   │       └── 📄 page.tsx         ← OTP verification page
│   │
│   └── student/                    ← Student pages
│       └── dashboard/
│           └── 📄 page.tsx         ← Student dashboard
│
├── components/                     ← React components
│   ├── 📄 NavBar.tsx              ← Navigation bar
│   └── 📄 ProtectedRoute.tsx       ← Route guard component
│
├── services/                       ← API integration
│   └── 📄 api.ts                  ← API client (40+ endpoints)
│
├── store/                          ← State management
│   └── 📄 authStore.ts            ← Zustand auth store
│
└── utils/                          ← Utility functions
    └── (helper functions)
```

**Frontend Quick Links:**
- **API Client:** [services/api.ts](./frontend/services/api.ts)
- **Auth Store:** [store/authStore.ts](./frontend/store/authStore.ts)
- **Login Page:** [app/auth/login/page.tsx](./frontend/app/auth/login/page.tsx)
- **OTP Page:** [app/auth/verify-otp/page.tsx](./frontend/app/auth/verify-otp/page.tsx)

---

## 🔗 Important Files by Purpose

### For Developers

**Backend Setup:**
- [backend/requirements.txt](./backend/requirements.txt) - Install dependencies
- [backend/.env](./backend/.env) - Configure backend
- [backend/app/main.py](./backend/app/main.py) - Start API

**Frontend Setup:**
- [frontend/package.json](./frontend/package.json) - Install dependencies
- [frontend/.env.local](./frontend/.env.local) - Configure frontend
- [SETUP.md](./SETUP.md) - Step-by-step guide

**Database:**
- [backend/app/models/models.py](./backend/app/models/models.py) - View all tables
- [backend/alembic/versions/001_initial.py](./backend/alembic/versions/001_initial.py) - Migrations

**API Integration:**
- [frontend/services/api.ts](./frontend/services/api.ts) - API endpoints
- [backend/app/routes/](./backend/app/routes/) - API implementation

### For Administrators

**Project Management:**
- [README.md](./README.md) - Overview
- [COMPLETION_SUMMARY.md](./COMPLETION_SUMMARY.md) - What's included
- [backend/app/routes/admin.py](./backend/app/routes/admin.py) - Admin APIs

**Deployment:**
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Production setup
- [backend/.env](./backend/.env) - Production config
- [frontend/.env.local](./frontend/.env.local) - Frontend config

**Security:**
- [backend/app/core/security.py](./backend/app/core/security.py) - Auth implementation
- [DEPLOYMENT.md#Security](./DEPLOYMENT.md) - Security checklist

### For DevOps

**Infrastructure:**
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Azure setup
- [backend/requirements.txt](./backend/requirements.txt) - Dependencies
- [frontend/package.json](./frontend/package.json) - Dependencies

**Configuration:**
- [backend/.env](./backend/.env) - Backend env
- [frontend/.env.local](./frontend/.env.local) - Frontend env

---

## 📚 Documentation Map

| Document | Size | Read Time | For |
|----------|------|-----------|-----|
| [README.md](./README.md) | ~2KB | 5 min | Everyone |
| [SETUP.md](./SETUP.md) | ~4KB | 10 min | Developers |
| [DEPLOYMENT.md](./DEPLOYMENT.md) | ~8KB | 20 min | DevOps/Admins |
| [COMPLETION_SUMMARY.md](./COMPLETION_SUMMARY.md) | ~6KB | 10 min | Project Managers |
| [backend/README.md](./backend/README.md) | ~2KB | 5 min | Backend Devs |
| [frontend/README.md](./frontend/README.md) | ~2KB | 5 min | Frontend Devs |

---

## 🚀 Getting Started Paths

### Path 1: Quick Start (Fastest)
1. Read [README.md](./README.md) (5 min)
2. Read [SETUP.md](./SETUP.md) (5 min)
3. Follow setup steps (10 min)
4. Run and test (5 min)
**Total: 25 minutes**

### Path 2: Thorough Setup (Recommended)
1. Read [README.md](./README.md)
2. Read [SETUP.md](./SETUP.md)
3. Read [backend/README.md](./backend/README.md)
4. Read [frontend/README.md](./frontend/README.md)
5. Follow setup steps
6. Test endpoints
**Total: 1-2 hours**

### Path 3: Full Deployment
1. Complete Path 2
2. Read [DEPLOYMENT.md](./DEPLOYMENT.md)
3. Configure production environment
4. Deploy to Azure
**Total: 2-4 hours**

---

## 🔍 Finding Things

### "How do I...?"

**Login a user?**
- Frontend: [app/auth/login/page.tsx](./frontend/app/auth/login/page.tsx)
- Backend: [routes/auth.py](./backend/app/routes/auth.py#L10)

**Create a project?**
- Backend: [routes/projects.py](./backend/app/routes/projects.py#L13)
- API: `POST /api/projects`

**Submit work?**
- Frontend: [services/api.ts](./frontend/services/api.ts#L92) → `submissionAPI.upload()`
- Backend: [routes/submissions.py](./backend/app/routes/submissions.py#L12)

**Score a submission?**
- Backend: [routes/submissions.py](./backend/app/routes/submissions.py#L146)
- API: `POST /api/submissions/{id}/supervisor-feedback`

**Deploy to Azure?**
- See [DEPLOYMENT.md#Backend-Deployment](./DEPLOYMENT.md)

### "Where is...?"

**Database models?**
- [backend/app/models/models.py](./backend/app/models/models.py)

**API endpoints?**
- [backend/app/routes/](./backend/app/routes/) (7 files)

**Environment config?**
- [backend/.env](./backend/.env)
- [frontend/.env.local](./frontend/.env.local)

**Authentication logic?**
- [backend/app/core/security.py](./backend/app/core/security.py)

**Email templates?**
- [backend/app/services/email_service.py](./backend/app/services/email_service.py#L8)

**Chatbot implementation?**
- [backend/app/routes/chatbot.py](./backend/app/routes/chatbot.py)

---

## 📊 File Size Summary

```
Backend:    ~2000 lines of code
Frontend:   ~800 lines of code
Config:     ~400 lines of configuration
Docs:       ~2000 lines of documentation
────────────────────────────
Total:      ~5200 lines
```

---

## ✅ Navigation Checklist

- [ ] Read [README.md](./README.md)
- [ ] Read [SETUP.md](./SETUP.md)
- [ ] Review [backend/app/main.py](./backend/app/main.py)
- [ ] Review [backend/app/models/models.py](./backend/app/models/models.py)
- [ ] Review [frontend/services/api.ts](./frontend/services/api.ts)
- [ ] Review [frontend/app/auth/login/page.tsx](./frontend/app/auth/login/page.tsx)
- [ ] Read [DEPLOYMENT.md](./DEPLOYMENT.md)
- [ ] Set up local environment
- [ ] Test all endpoints

---

## 🎯 Quick Commands

```bash
# Backend
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend && npm install
npm run dev  # Opens http://localhost:3000

# Check backend API
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Swagger UI
```

---

## 📞 Need Help?

1. **Setting up?** → Read [SETUP.md](./SETUP.md)
2. **Understanding code?** → Check file headers and comments
3. **Deploying?** → Read [DEPLOYMENT.md](./DEPLOYMENT.md)
4. **API details?** → Visit http://localhost:8000/docs
5. **Troubleshooting?** → See [DEPLOYMENT.md#Troubleshooting](./DEPLOYMENT.md)

---

**Happy coding! 🚀**

Last Updated: January 2024
