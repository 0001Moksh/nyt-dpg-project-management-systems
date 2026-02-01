# DPG PMS - Complete Setup Guide

This guide walks you through setting up the entire DPG Project Management System from scratch.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Email Configuration](#email-configuration)
6. [Database Setup](#database-setup)
7. [Testing](#testing)
8. [Deployment](#deployment)

---

## Prerequisites

### Required Software

- **Node.js 18+** - [Download](https://nodejs.org)
  ```bash
  node --version  # Should be v18 or higher
  npm --version
  ```

- **Python 3.9+** - [Download](https://www.python.org)
  ```bash
  python --version  # Should be 3.9 or higher
  ```

- **PostgreSQL 12+** - [Download](https://www.postgresql.org)
  ```bash
  psql --version
  ```

- **Git** - [Download](https://git-scm.com)
  ```bash
  git --version
  ```

### Required Accounts

- **Gmail Account** (for SMTP) or other email provider
- **Groq API Key** - [Get here](https://console.groq.com)
- **Azure Account** (optional, for OneDrive storage)

### Hardware Requirements

- Minimum 4GB RAM
- 5GB free disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)

---

## Environment Setup

### 1. Clone Repository (or Create Folders)

```bash
# Create project directory
mkdir dpg-pms
cd dpg-pms

# Initialize git (if not already done)
git init

# Create subdirectories
mkdir frontend backend
```

### 2. Create .env File

Copy the provided `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# ===== FRONTEND CONFIGURATION =====
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=DPG Project Management System
NEXT_PUBLIC_COLLEGE_NAME=DPG ITM College
NEXT_PUBLIC_COMPANY_NAME=NexyugTech

# ===== BACKEND CONFIGURATION =====
FASTAPI_BASE_URL=http://localhost:8000
FASTAPI_DEBUG=true

# ===== SMTP EMAIL CONFIGURATION =====
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@dpg-itm.com
SMTP_FROM_NAME=DPG Project Management System

# ===== DATABASE CONFIGURATION =====
DATABASE_URL=postgresql://dpg_user:secure_password@localhost:5432/dpg_pms
DATABASE_POOL_SIZE=20
DATABASE_POOL_RECYCLE=3600

# ===== AUTHENTICATION =====
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRY_HOURS=24
OTP_EXPIRY_MINUTES=5
OTP_LENGTH=6

# ===== GROQ LLM =====
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL_NAME=mixtral-8x7b-32768

# ===== SECURITY =====
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

---

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 4: Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE dpg_pms;

# Create user
CREATE USER dpg_user WITH PASSWORD 'secure_password';

# Grant privileges
ALTER ROLE dpg_user SET client_encoding TO 'utf8';
ALTER ROLE dpg_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE dpg_user SET default_transaction_deferrable TO on;
ALTER ROLE dpg_user SET default_transaction_read_only TO off;
GRANT ALL PRIVILEGES ON DATABASE dpg_pms TO dpg_user;

# Exit psql
\q
```

### Step 5: Run Database Migrations

```bash
# Initialize Alembic (if not done)
alembic init migrations

# Run migrations
alembic upgrade head
```

### Step 6: Create Admin User (Optional)

```bash
# Create a script to add admin
python scripts/create_admin.py
```

Or manually:
```python
from app.models import User, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://dpg_user:secure_password@localhost/dpg_pms")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

admin = User(
    id="admin_001",
    email="admin@dpg-itm.edu.in",
    name="Admin User",
    role="ADMIN",
    is_active=True
)
session.add(admin)
session.commit()
```

### Step 7: Test Backend

```bash
# Run development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, test API
curl http://localhost:8000/health

# Visit API docs
open http://localhost:8000/docs
```

✅ Backend should be running at `http://localhost:8000`

---

## Frontend Setup

### Step 1: Navigate to Frontend Directory

```bash
cd ../frontend  # Go to frontend folder
```

### Step 2: Install Dependencies

```bash
npm install
```

### Step 3: Create Environment File

```bash
# Create .env.local
echo "NEXT_PUBLIC_API_BASE_URL=http://localhost:8000" > .env.local
```

Or edit `.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=DPG Project Management System
```

### Step 4: Run Development Server

```bash
npm run dev
```

✅ Frontend should be running at `http://localhost:3000`

### Step 5: Build for Production

```bash
npm run build
npm start
```

---

## Email Configuration

### Gmail SMTP Setup

#### Step 1: Enable 2-Factor Authentication
1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click "Security" (left menu)
3. Enable 2-Step Verification

#### Step 2: Generate App Password
1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Select "Mail" and "Windows Computer" (or your device)
3. Click "Generate"
4. Copy the 16-character password

#### Step 3: Update .env
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx  # Paste your app password
SMTP_FROM_EMAIL=noreply@dpg-itm.com
SMTP_FROM_NAME=DPG Project Management System
```

#### Step 4: Test Email
```python
import asyncio
from app.services.email_service import email_service

async def test_email():
    result = await email_service.send_otp_email(
        "your-email@gmail.com",
        "123456",
        "Test User"
    )
    print(f"Email sent: {result}")

asyncio.run(test_email())
```

### Alternative: SendGrid

```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.your-sendgrid-api-key
```

### Alternative: Outlook/Microsoft 365

```env
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-outlook-password
```

---

## Database Setup

### Create Initial Schema

The backend automatically creates tables on startup. To manually create:

```bash
# From backend directory
python -c "from app.models import Base; Base.metadata.create_all()"
```

### View Database

```bash
# Connect to database
psql -U dpg_user -d dpg_pms

# List tables
\dt

# View schema
\d users

# Exit
\q
```

### Seed Demo Data

```bash
python scripts/seed_data.py
```

This creates:
- 10 demo students
- 3 demo supervisors
- 1 demo admin
- 2 demo projects
- 3 demo teams

### Backup Database

```bash
# Backup
pg_dump -U dpg_user -d dpg_pms > backup.sql

# Restore
psql -U dpg_user -d dpg_pms < backup.sql
```

---

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_auth.py::test_otp_request -v
```

### Frontend Tests

```bash
cd frontend

# Run tests
npm run test

# Run with coverage
npm run test:coverage

# Watch mode
npm run test -- --watch
```

### Integration Testing

```bash
# Test full flow
1. Start backend: python -m uvicorn app.main:app --reload
2. Start frontend: npm run dev
3. Open http://localhost:3000
4. Login with test user (check seed data)
```

### Manual API Testing

```bash
# Request OTP
curl -X POST http://localhost:8000/api/v1/auth/request-otp \
  -H "Content-Type: application/json" \
  -d '{"email":"student@dpg-itm.edu.in"}'

# Verify OTP (check console/email for OTP)
curl -X POST http://localhost:8000/api/v1/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"email":"student@dpg-itm.edu.in","otp":"123456"}'

# Get projects
curl http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Deployment

### Frontend Deployment (Vercel)

```bash
cd frontend

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables
vercel env add NEXT_PUBLIC_API_BASE_URL https://api.your-domain.com

# Deploy with environment
vercel --prod
```

### Backend Deployment (Azure)

#### Option 1: Azure App Service

```bash
# Install Azure CLI
# Download from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Create resource group
az group create --name dpg-pms-rg --location eastus

# Create app service plan
az appservice plan create --name dpg-pms-plan --resource-group dpg-pms-rg --sku F1

# Create web app
az webapp create --resource-group dpg-pms-rg --plan dpg-pms-plan --name dpg-pms-backend

# Deploy from local git
az webapp deployment user set --user-name your-username --password your-password
git remote add azure https://your-username@dpg-pms-backend.scm.azurewebsites.net:443/dpg-pms-backend.git
git push azure main

# Set environment variables
az webapp config appsettings set --resource-group dpg-pms-rg --name dpg-pms-backend \
  --settings DATABASE_URL="postgresql://..." SMTP_HOST="smtp.gmail.com" ...
```

#### Option 2: Docker on Azure

```bash
# Build Docker image
docker build -t dpg-pms:latest .

# Tag image
docker tag dpg-pms:latest your-registry.azurecr.io/dpg-pms:latest

# Push to Azure Container Registry
az acr build --registry your-registry --image dpg-pms:latest .

# Deploy to Azure Container Instances
az container create --resource-group dpg-pms-rg \
  --name dpg-pms-backend \
  --image your-registry.azurecr.io/dpg-pms:latest \
  --ports 8000 \
  --environment-variables DATABASE_URL="..." SMTP_HOST="..."
```

### Production Checklist

- [ ] Set `DEBUG=false` in environment
- [ ] Change `JWT_SECRET_KEY` to strong value
- [ ] Configure HTTPS certificates
- [ ] Set up database backups
- [ ] Configure monitoring and logging
- [ ] Set up error tracking (Sentry)
- [ ] Enable rate limiting
- [ ] Configure CDN for static files
- [ ] Set up CI/CD pipeline
- [ ] Test email notifications
- [ ] Load testing
- [ ] Security audit

---

## Troubleshooting

### Backend Issues

#### Database Connection Error
```
Error: could not connect to server: Connection refused
```
**Solution:**
- Ensure PostgreSQL is running: `pg_ctl start` (Mac) or `sudo service postgresql start` (Linux)
- Check DATABASE_URL in .env
- Verify database exists: `psql -U dpg_user -d dpg_pms -c "\dt"`

#### SMTP Connection Error
```
Error: SMTPAuthenticationError
```
**Solution:**
- Verify SMTP credentials in .env
- For Gmail: Use App Password (not account password)
- Check SMTP_HOST and SMTP_PORT

#### Port Already in Use
```
Error: Address already in use: ('0.0.0.0', 8000)
```
**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python -m uvicorn app.main:app --port 8001
```

### Frontend Issues

#### API Connection Error
```
Error: Network request failed
```
**Solution:**
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_BASE_URL` in .env.local
- Check browser console for CORS errors

#### Port Already in Use
```
Error: Port 3000 is already in use
```
**Solution:**
```bash
# Kill process
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Or use different port
npm run dev -- -p 3001
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` | Missing Python package | `pip install -r requirements.txt` |
| `CORS error` | Frontend domain not allowed | Add to `CORS_ORIGINS` in .env |
| `JWT token expired` | Token invalid | Clear localStorage, login again |
| `Database locked` | Another process using DB | Kill other processes or restart |
| `OTP not received` | SMTP configuration | Test SMTP credentials manually |

---

## Development Workflow

### Day-to-Day Development

```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Visit http://localhost:3000
```

### Making Changes

**Backend:**
```bash
# Make changes in backend/app
# Server auto-reloads with --reload flag
```

**Frontend:**
```bash
# Make changes in frontend
# HMR (Hot Module Replacement) automatically reloads browser
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature

# Create pull request
```

---

## Useful Commands

### Backend

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/

# Run migrations
alembic upgrade head

# Create migration
alembic revision --autogenerate -m "Description"

# Downgrade migration
alembic downgrade -1
```

### Frontend

```bash
# Format code
npm run format

# Lint
npm run lint

# Type check
npm run type-check

# Build
npm run build

# Start production build
npm start
```

---

## Next Steps

1. ✅ Complete setup following this guide
2. 📧 Test email notifications
3. 🔐 Test OTP login flow
4. 📊 Create demo projects
5. 👥 Add test users
6. 🧪 Run test suite
7. 📚 Read API documentation
8. 🚀 Deploy to production

---

## Support & Resources

- **API Docs**: http://localhost:8000/docs
- **Frontend Docs**: `./frontend/README.md`
- **Backend Docs**: `./backend/README.md`
- **Issues**: Check GitHub issues or contact support

---

**Happy developing! 🚀**

For questions or issues, reach out to the NexyugTech team.
