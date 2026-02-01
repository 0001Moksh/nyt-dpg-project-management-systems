# DPG Project Management System - Setup Guide

## 🎯 Quick Setup (5 minutes)

This guide will get you running the complete system locally.

## Prerequisites

- **Node.js 18+** - [Download](https://nodejs.org/)
- **Python 3.10+** - [Download](https://www.python.org/)
- **PostgreSQL 13+** or **Supabase account** - [Free tier available](https://supabase.com/)
- **Git** - [Download](https://git-scm.com/)

## Step 1: Clone & Structure

```bash
# Create project directory
mkdir dpg-pms-project
cd dpg-pms-project

# The structure is already created in your workspace:
# backend/  <- FastAPI backend
# frontend/ <- Next.js frontend
```

## Step 2: Backend Setup

### 2.1 Create Python Virtual Environment

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.3 Configure Database

**Option A: Local PostgreSQL**

```bash
# Install PostgreSQL locally
# Create database
createdb dpg_pms

# Update .env
DATABASE_URL=postgresql://username:password@localhost:5432/dpg_pms
```

**Option B: Supabase (Recommended)**

1. Create account at [supabase.com](https://supabase.com/)
2. Create new project
3. Copy connection string from "Connection Pooler"
4. Update `.env`:

```env
DATABASE_URL=postgresql://[user]:[password]@db.supabase.co:5432/postgres
```

### 2.4 Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

**Required variables to update:**
```env
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=choose-a-strong-secret-key
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
GROQ_API_KEY=your-groq-api-key
ONEDRIVE_*=your-onedrive-credentials
```

### 2.5 Run Backend

```bash
# Create database tables (automatic on first run)
python app/main.py

# Or start with uvicorn
uvicorn app.main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Test API:**
- Visit: http://localhost:8000/docs
- You should see interactive API documentation

## Step 3: Frontend Setup

### 3.1 Install Dependencies

```bash
cd frontend
npm install
```

### 3.2 Configure Environment

```bash
# Copy template if needed
cat .env.local

# Or create if missing
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local
```

### 3.3 Run Frontend

```bash
npm run dev
```

**Expected output:**
```
> ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

**Visit:** http://localhost:3000

## Step 4: Test the System

### 4.1 Create Admin User (Database)

Connect to PostgreSQL:

```bash
# Supabase users: Use SQL Editor in dashboard
# Local users: psql dpg_pms

INSERT INTO users (email, name, role, password_hash, is_active)
VALUES (
    'admin@dpg-itm.edu.in',
    'Admin User',
    'admin',
    'add-hashed-password-here',
    true
);
```

To hash a password in Python:
```python
from app.core.security import PasswordHandler
hashed = PasswordHandler.hash_password('admin123')
print(hashed)
```

### 4.2 Test Admin Login

1. Go to http://localhost:3000/auth/login
2. Enter: `admin@dpg-itm.edu.in`
3. Should show password prompt
4. Enter password
5. Should redirect to `/admin/dashboard`

### 4.3 Test Student Login

1. Go to http://localhost:3000/auth/login
2. Enter: `student@example.com` (any email)
3. OTP will be logged to console in dev mode
4. Enter OTP (5-digit code shown in backend logs)
5. Should redirect to `/student/dashboard`

### 4.4 Test API Directly

```bash
# Login - send OTP
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# Expected response
# {
#   "status": "otp_sent",
#   "message": "OTP sent to your email",
#   "email": "test@example.com"
# }

# Check backend logs for OTP code in dev mode
```

## Step 5: Configuration Details

### Email (SMTP)

**With Gmail:**
1. Enable 2-factor authentication
2. Generate app-specific password: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Update `.env`:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@example.com
```

### AI Chatbot (Groq)

1. Sign up at [console.groq.com](https://console.groq.com/)
2. Create API key
3. Update `.env`:

```env
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL_NAME=mixtral-8x7b-32768
```

### OneDrive File Storage

1. Register app at [azure.microsoft.com/en-us/services/app-service/](https://portal.azure.com/)
2. Get credentials (Tenant ID, Client ID, Secret)
3. Update `.env`:

```env
ONEDRIVE_TENANT_ID=your-tenant-id
ONEDRIVE_CLIENT_ID=your-client-id
ONEDRIVE_CLIENT_SECRET=your-secret
ONEDRIVE_FOLDER_ID=your-folder-id
```

## Troubleshooting

### Issue: "Connection refused" to database

**Solution:**
- Ensure PostgreSQL is running
- Verify DATABASE_URL in .env
- Check credentials are correct

### Issue: OTP not sending

**Solution:**
- Verify SMTP credentials
- Check Gmail app-specific password
- Enable "Less Secure Apps" if using regular Gmail password
- Check spam folder

### Issue: Frontend can't reach backend

**Solution:**
- Verify backend is running on port 8000
- Check NEXT_PUBLIC_API_BASE_URL in .env.local
- Clear browser cache

### Issue: Module not found errors (Python)

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue: npm dependency errors

**Solution:**
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

## What's Included

### Backend (FastAPI)
- ✅ OTP + JWT authentication
- ✅ Database models (SQLAlchemy)
- ✅ RESTful API endpoints
- ✅ Email service (SMTP)
- ✅ Groq AI chatbot
- ✅ OneDrive integration
- ✅ Audit logging

### Frontend (Next.js)
- ✅ Login & OTP verification pages
- ✅ Role-based dashboards (admin/student/supervisor)
- ✅ API client with Axios
- ✅ State management (Zustand)
- ✅ Tailwind CSS styling
- ✅ Responsive design

### Database
- ✅ Users, Projects, Teams
- ✅ Submissions (4-stage workflow)
- ✅ Feedback & Scoring
- ✅ Notifications & Logs
- ✅ Chat sessions

## Next Steps

1. **Create a project** - Admin → Create Project
2. **Get enrollment token** - Share with students
3. **Student enrolls** - Use token to join project
4. **Form teams** - Create team, invite members
5. **Submit work** - Upload submissions for review
6. **Score submissions** - Supervisor & admin scoring
7. **View leaderboard** - Final rankings

## Development Tips

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### API Documentation

Auto-generated Swagger UI:
- http://localhost:8000/docs

ReDoc documentation:
- http://localhost:8000/redoc

### Frontend Development

Hot reload enabled - changes auto-refresh in browser.

Debug mode:
```bash
npm run dev -- --verbose
```

### Logs

**Backend logs** - Terminal where uvicorn runs
**Frontend logs** - Browser console (F12)
**Database logs** - Check PostgreSQL/Supabase logs

## Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for:
- Docker containerization
- Azure App Service deployment
- Vercel/Static Web Apps deployment
- Environment configuration
- Security hardening

## Support & Resources

- **API Docs:** http://localhost:8000/docs
- **Main README:** [README.md](./README.md)
- **Deployment Guide:** [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Backend README:** [backend/README.md](./backend/README.md)
- **Frontend README:** [frontend/README.md](./frontend/README.md)

## Common Commands

```bash
# Backend
cd backend
python -m venv venv          # Create virtual env
pip install -r requirements.txt  # Install deps
uvicorn app.main:app --reload   # Start server

# Frontend
cd frontend
npm install                      # Install deps
npm run dev                      # Start dev server
npm run build                    # Build for production
npm run start                    # Start production server

# Database
# Connect with your PostgreSQL client
# Create database: createdb dpg_pms
# Apply migrations: alembic upgrade head
```

## Next: Run the Project

You're ready! Open two terminals:

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Then open: **http://localhost:3000**

---

**Status:** ✅ Ready to Run
**Last Updated:** January 2024
