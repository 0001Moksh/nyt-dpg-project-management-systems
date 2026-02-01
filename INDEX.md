# DPG Project Management System - Complete File Index

## 📑 Documentation Files (Read These First)

| File | Purpose | Read Time |
|------|---------|-----------|
| [README.md](./README.md) | Main project overview, features, and quick start | 5 min |
| [PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md) | Complete project summary, deliverables, and next steps | 10 min |
| [SETUP_GUIDE.md](./SETUP_GUIDE.md) | Step-by-step setup instructions for local development | 15 min |
| [DEPLOYMENT.md](./DEPLOYMENT.md) | Production deployment guide for various platforms | 10 min |
| [INDEX.md](./INDEX.md) | This file - complete project structure reference | 5 min |

---

## 🔧 Configuration Files

### Root Level
```
.env.example              # Environment template for development
.env.production           # Production environment configuration
```

### Frontend Configuration
```
frontend/
├── package.json          # NPM dependencies and scripts
├── tsconfig.json         # TypeScript configuration
├── next.config.mjs       # Next.js build configuration
├── tailwind.config.js    # Tailwind CSS theme (if present)
└── postcss.config.js     # PostCSS plugins (if present)
```

### Backend Configuration
```
backend/
├── requirements.txt      # Python dependencies
├── app/config.py         # FastAPI configuration management
└── .env                  # Backend environment variables (not committed)
```

---

## 📁 Frontend Structure

### App Directory (`frontend/app/`)
```
(auth)/
├── login/
│   └── page.tsx          # Login page with email input
└── verify-otp/
    └── page.tsx          # OTP verification page

(student)/
├── dashboard/
│   └── page.tsx          # Student dashboard shell
├── projects/
├── teams/
└── submissions/

(supervisor)/
├── dashboard/
│   └── page.tsx          # Supervisor dashboard shell
├── teams/
├── submissions/
└── scoring/

(admin)/
├── dashboard/
│   └── page.tsx          # Admin dashboard shell
├── projects/
├── users/
├── leaderboard/
└── analytics/

layout.tsx                # Root layout with metadata
page.tsx                  # Home page
globals.css               # Global styles and Tailwind theme
```

### Services (`frontend/services/`)
```
api.ts                    # Base HTTP client with axios
auth.ts                   # Authentication service (OTP, login)
projects.ts               # Project and team operations
```

### Store (`frontend/store/`)
```
auth.ts                   # Zustand authentication store
```

### Types (`frontend/types/`)
```
index.ts                  # All TypeScript type definitions
```

### Components (`frontend/components/`)
```
auth/                     # Authentication components
dashboard/                # Dashboard components
projects/                 # Project components
teams/                    # Team components
submissions/              # Submission components
chatbot/                  # Chatbot components
leaderboard/              # Leaderboard components
common/                   # Shared components
ui/                       # shadcn/ui components (auto-generated)
```

### Documentation
```
frontend/README.md        # Frontend development guide
```

---

## 📁 Backend Structure

### App Core (`backend/app/`)
```
main.py                   # FastAPI application entry point
config.py                 # Configuration management
models.py                 # SQLAlchemy ORM models
schemas.py                # Pydantic validation schemas
deps.py                   # Dependency injection
```

### Services (`backend/app/services/`)
```
auth_service.py           # OTP generation, JWT tokens
email_service.py          # SMTP email sending
rag_chatbot.py            # Groq LLM chatbot integration
projects.py               # Project operations
submissions.py            # Submission handling
teams.py                  # Team management
analytics.py              # Analytics and predictions
```

### Routes (`backend/app/routes/`)
```
auth.py                   # /api/v1/auth endpoints
projects.py               # /api/v1/projects endpoints
teams.py                  # /api/v1/teams endpoints
submissions.py            # /api/v1/submissions endpoints
chatbot.py                # /api/v1/chatbot endpoints
leaderboard.py            # /api/v1/leaderboard endpoints
admin.py                  # /api/v1/admin endpoints
```

### Middleware (`backend/app/middleware/`)
```
auth_middleware.py        # JWT verification
rate_limit.py             # Rate limiting
error_handler.py          # Error handling and logging
```

### Utilities (`backend/app/utils/`)
```
security.py               # Security utilities
validators.py             # Input validation
decorators.py             # Custom decorators
constants.py              # Application constants
exceptions.py             # Custom exceptions
```

### Database (`backend/app/db/`)
```
session.py                # Database session management
base.py                   # Base model class
```

### Migrations (`backend/migrations/`)
```
alembic.ini               # Alembic configuration
env.py                    # Migration environment
versions/                 # Migration files (auto-generated)
```

### Tests (`backend/tests/`)
```
conftest.py               # Test configuration
test_auth.py              # Authentication tests
test_projects.py          # Project tests
test_submissions.py       # Submission tests
test_chatbot.py           # Chatbot tests
```

### Scripts (`backend/scripts/`)
```
create_admin.py           # Script to create admin user
seed_data.py              # Script to seed test data
generate_links.py         # Script to generate enrollment links
```

### Documentation
```
backend/README.md         # Backend development guide
```

---

## 🗄️ Database Schema

### Tables
```
users                     # User accounts (Student, Supervisor, Admin)
projects                  # Project definitions
teams                     # Student teams
team_members              # Team membership records
submissions               # Project submissions (4 stages)
stage_scores              # Scoring for each stage
notifications             # Email and in-app notifications
chat_sessions             # Chatbot conversation sessions
chat_messages             # Chat messages
```

### Relationships
```
User → Team (one-to-many, team.leader_id → user.id)
Project → Team (one-to-many, team.project_id → project.id)
Team → TeamMember (one-to-many, member.team_id → team.id)
User → TeamMember (one-to-many, member.user_id → user.id)
Team → Submission (one-to-many, submission.team_id → team.id)
Team → StageScore (one-to-many, score.team_id → team.id)
User → Notification (one-to-many, notification.recipient_id → user.id)
User → ChatSession (one-to-many, session.user_id → user.id)
ChatSession → ChatMessage (one-to-many, message.session_id → session.id)
```

---

## 📚 API Endpoints

### Authentication (`/api/v1/auth`)
```
POST   /request-otp         # Send OTP to email
POST   /verify-otp          # Verify OTP and login
GET    /me                  # Get current user
POST   /logout              # Logout
POST   /refresh-token       # Refresh JWT token
```

### Projects (`/api/v1/projects`)
```
GET    /                    # List projects
POST   /                    # Create project
GET    /{id}                # Get project details
PUT    /{id}                # Update project
POST   /{id}/generate-enrollment-link
GET    /{id}/teams          # Get project teams
GET    /{id}/stats          # Get project statistics
```

### Teams (`/api/v1/teams`)
```
GET    /{id}                # Get team details
POST   /{id}/join           # Join team
POST   /{id}/leave          # Leave team
POST   /{id}/members/{mid}/approve
POST   /{id}/assign-supervisor
```

### Submissions (`/api/v1/submissions`)
```
GET    /                    # List submissions
POST   /                    # Upload submission
GET    /{id}                # Get submission details
POST   /{id}/approve        # Approve submission
POST   /{id}/reject         # Reject submission
POST   /{id}/review         # Review and score
```

### Chatbot (`/api/v1/chatbot`)
```
POST   /chat                # Send message
POST   /faq                 # Get FAQ answer
GET    /sessions            # List sessions
DELETE /sessions/{id}       # Clear session
```

### Leaderboard (`/api/v1/leaderboard`)
```
GET    /                    # Get leaderboard
GET    /?projectId=...      # Get project leaderboard
```

### Admin (`/api/v1/admin`)
```
GET    /users               # List users
POST   /users               # Create user
GET    /analytics           # Analytics dashboard
GET    /reports             # Generate reports
```

---

## 🔐 Environment Variables

### Frontend (NEXT_PUBLIC prefix)
```
NEXT_PUBLIC_API_BASE_URL       # Backend API URL
NEXT_PUBLIC_APP_NAME           # Application name
NEXT_PUBLIC_COLLEGE_NAME       # College name
NEXT_PUBLIC_COMPANY_NAME       # Company name
```

### Backend
```
FASTAPI_BASE_URL               # Backend base URL
FASTAPI_DEBUG                  # Debug mode (false in production)
DATABASE_URL                   # PostgreSQL connection string
SMTP_HOST                      # SMTP server hostname
SMTP_PORT                      # SMTP port (usually 587)
SMTP_USER                      # SMTP username/email
SMTP_PASSWORD                  # SMTP password or app password
JWT_SECRET_KEY                 # JWT signing secret (32+ chars)
GROQ_API_KEY                   # Groq LLM API key
CORS_ORIGINS                   # Comma-separated allowed origins
```

Full list in `.env.example` and `.env.production`

---

## 🚀 Getting Started Workflow

### 1. Read Documentation (30 min)
1. Read `README.md` for overview
2. Read `PROJECT_SUMMARY.md` for complete picture
3. Skim through frontend and backend READMEs

### 2. Setup Development Environment (45 min)
1. Follow `SETUP_GUIDE.md` step-by-step
2. Install dependencies
3. Configure database
4. Setup SMTP email
5. Get Groq API key

### 3. Start Development (30 min)
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Browser
open http://localhost:3000
```

### 4. Test Core Features
- Login with OTP
- Navigate to dashboards
- Check API documentation

---

## 📊 Project Statistics

| Metric | Count |
|--------|-------|
| Configuration Files | 5 |
| Documentation Files | 6 |
| Frontend Pages | 6+ |
| Backend Services | 6 |
| API Endpoints | 30+ |
| Database Tables | 10 |
| TypeScript Types | 15+ |
| Components | 15+ |
| Total Lines of Documentation | 3000+ |

---

## 🎯 Development Workflow

### Daily Development
```bash
# Update backend
cd backend
python -m uvicorn app.main:app --reload

# Update frontend (auto-reloads)
cd frontend
npm run dev

# Test changes at localhost:3000
```

### Code Quality
```bash
# Frontend
npm run lint
npm run type-check
npm run test

# Backend
black app/
flake8 app/
mypy app/
pytest
```

### Git Workflow
```bash
git checkout -b feature/new-feature
git commit -am "Add feature"
git push origin feature/new-feature
# Create pull request
```

---

## 📞 Quick Reference

### Key Contacts
- **NexyugTech:** https://nexyugtech.com
- **DPG ITM College:** [Your contact here]

### Important URLs
- **Frontend Dev:** http://localhost:3000
- **Backend Dev:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Vercel Dashboard:** https://vercel.com
- **Azure Portal:** https://portal.azure.com
- **Groq Console:** https://console.groq.com

### Important Files to Read First
1. `README.md` ← Start here
2. `PROJECT_SUMMARY.md` ← Then here
3. `SETUP_GUIDE.md` ← Setup instructions
4. `frontend/README.md` ← Frontend specifics
5. `backend/README.md` ← Backend specifics

---

## ✅ Completion Checklist

- [x] Frontend architecture setup
- [x] Backend architecture setup
- [x] Database schema designed
- [x] Authentication system implemented
- [x] Email service configured
- [x] API endpoints designed
- [x] Type definitions created
- [x] Documentation written
- [x] Setup guide created
- [x] Deployment guide created
- [x] Environment templates provided
- [x] Project ready for team development

---

## 🎓 Learning Path

### For Frontend Developers
1. Read `frontend/README.md`
2. Understand types in `frontend/types/index.ts`
3. Review auth store in `frontend/store/auth.ts`
4. Study services in `frontend/services/`
5. Start building components

### For Backend Developers
1. Read `backend/README.md`
2. Understand models in `backend/app/models.py`
3. Review services in `backend/app/services/`
4. Study routes in `backend/app/routes/`
5. Start implementing endpoints

### For DevOps/Deployment
1. Read `DEPLOYMENT.md`
2. Understand environment variables
3. Review Docker setup
4. Setup CI/CD pipeline
5. Configure monitoring

---

## 🔗 File Cross-References

### If You Need To...

**Setup Database:**
- Read: `SETUP_GUIDE.md` → Database Setup section
- File: `backend/app/models.py`
- File: `backend/migrations/`

**Configure Email:**
- Read: `SETUP_GUIDE.md` → Email Configuration section
- File: `backend/app/services/email_service.py`
- File: `.env.example`

**Understand API:**
- Read: `backend/README.md` → API Endpoints section
- Access: `http://localhost:8000/docs`
- File: `backend/app/routes/`

**Build Frontend Page:**
- Read: `frontend/README.md` → Component Examples
- File: `frontend/app/(auth)/login/page.tsx`
- File: `frontend/services/api.ts`

**Deploy to Production:**
- Read: `DEPLOYMENT.md`
- File: `.env.production`
- Follow: Step-by-step in DEPLOYMENT.md

---

## 🎬 Next Actions

1. **Download/Clone:** Get all project files
2. **Read:** Start with `README.md`
3. **Setup:** Follow `SETUP_GUIDE.md`
4. **Develop:** Start building components
5. **Deploy:** Follow `DEPLOYMENT.md`

---

**Status: READY FOR DEVELOPMENT**

All files are in place. Development team can begin immediately.

For any questions, refer to the documentation files or visit the NexyugTech website.

---

Generated: January 2024  
For: DPG ITM College  
By: NexyugTech Company
