# DPG Project Management System - Complete Guide

## 📋 Overview

A comprehensive project management system designed for educational institutions. Built with modern web technologies and AI-powered chatbot support.

**Stack:**
- **Frontend:** Next.js 14 + React 18 + Tailwind CSS
- **Backend:** FastAPI + SQLAlchemy + PostgreSQL
- **Storage:** OneDrive (PDFs) + PostgreSQL (metadata)
- **AI/LLM:** Groq API (Mixtral-8x7b)
- **Auth:** OTP (5 min expiry) + JWT (24 hr expiry)

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.10+ (for backend)
- PostgreSQL 13+ (or Supabase)
- Git

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup .env file (copy from .env.example)
cp .env.example .env
# Edit .env with your configuration

# Run migrations (auto-created on first run)
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

Server will be available at: **http://localhost:8000**
API docs: **http://localhost:8000/docs**

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Setup .env.local
cp .env.local.example .env.local
# Edit .env.local with backend URL

# Start development server
npm run dev
```

App will be available at: **http://localhost:3000**

---

## 📊 Database Schema

### Core Tables

**Users**
- id, email, name, role (admin/supervisor/student)
- student_id, department, batch (for students)
- teacher_id, department_supervisor (for supervisors)
- password_hash (for admins), is_active, timestamps

**Projects**
- id, title, description, branch, batch, deadline
- enrollment_token (unique), enrollment_link, is_active, timestamps

**ProjectEnrollments**
- project_id FK, user_id FK, enrolled_at

**Teams**
- id, project_id FK, leader_id FK, name
- status (pending/active/locked), is_locked, timestamps

**TeamInvitations**
- id, team_id FK, invitee_email
- status (pending/approved/rejected), invited_at, responded_at

**Submissions** (4-stage workflow)
- id, team_id FK, stage (synopsis/progress_1/progress_2/final)
- file_url (OneDrive), uploaded_by FK, approval_status, timestamps

**SubmissionApprovals**
- id, submission_id FK, user_id FK
- status (pending/approved/rejected), responded_at

**SubmissionFeedback**
- id, submission_id FK
- supervisor_id FK, supervisor_score (0-10)
- admin_id FK, admin_score (0-20)
- comments, resubmission_deadline, timestamps

**SupervisorRequests**
- id, name, email, department, teacher_id
- status (pending/approved/rejected)
- approved_by FK, request_date, approved_date

**AdminLogs** (Audit trail)
- id, admin_id FK, action, resource_type, resource_id
- details (JSON), created_at

**OTPTokens**
- id, email, otp, expires_at, is_used, created_at

**Notifications**
- id, user_id FK, title, message, notification_type
- is_read, created_at

**ChatSessions**
- id, user_id FK, question, answer, created_at

---

## 🔐 Authentication Flow

### Student/Supervisor Login
1. User enters email → `/api/auth/login` (POST)
2. OTP generated & sent via email (5 min expiry)
3. User enters OTP → `/api/auth/verify-otp` (POST)
4. JWT token returned (24 hr expiry)
5. Token stored in localStorage
6. Redirect based on role

### Admin Login
1. User enters email + password → `/api/auth/admin-login` (POST)
2. Credentials verified
3. JWT token returned
4. Redirect to admin dashboard

---

## 📌 API Endpoints

### Authentication
- `POST /api/auth/login` - Send OTP or request admin password
- `POST /api/auth/verify-otp` - Verify OTP and get JWT
- `POST /api/auth/admin-login` - Admin password login
- `POST /api/auth/verify-token` - Verify JWT validity

### Admin
- `GET /api/admin/requests` - Get supervisor access requests
- `POST /api/admin/requests/{id}/approve` - Approve request
- `POST /api/admin/requests/{id}/reject` - Reject request
- `GET /api/admin/logs` - Get audit logs (pagination)
- `GET /api/admin/stats` - Dashboard statistics

### Projects
- `POST /api/projects` - Create project (admin)
- `GET /api/projects` - List all projects
- `GET /api/projects/{id}` - Get project details
- `POST /api/projects/{id}/enroll` - Student enrolls with token
- `GET /api/projects/{id}/leaderboard` - Final rankings

### Teams
- `POST /api/teams` - Create team (student leader)
- `GET /api/teams/{id}` - Get team details
- `POST /api/teams/{id}/invite` - Invite member
- `POST /api/teams/{id}/invitations/{inv_id}/respond` - Accept/reject invite
- `POST /api/teams/{id}/lock` - Lock team for submission
- `GET /api/teams/{id}/members` - List members

### Submissions (4-stage)
- `POST /api/submissions/{team_id}/{stage}` - Upload submission
  - Stages: `synopsis`, `progress_1`, `progress_2`, `final_submission`
- `GET /api/submissions/{id}` - Get submission details
- `POST /api/submissions/{id}/approve` - Member approve/reject
- `GET /api/submissions/team/{team_id}` - Get team submissions
- `POST /api/submissions/{id}/supervisor-feedback` - Add supervisor score (0-10)
- `POST /api/submissions/{id}/admin-feedback` - Add admin score (0-20)
- `GET /api/submissions/{id}/feedback` - Get all feedback

### Supervisor
- `GET /api/supervisor/submissions` - Get pending submissions
- `GET /api/supervisor/submissions/{id}` - Get submission for review
- `POST /api/supervisor/submissions/{id}/score` - Score submission
- `GET /api/supervisor/stats` - Supervisor statistics

### Chatbot
- `POST /api/chatbot/ask` - Ask RAG chatbot
- `GET /api/chatbot/sessions` - Get chat history
- `DELETE /api/chatbot/sessions/{id}` - Delete chat session

---

## 🎯 Workflow Details

### Team Creation & Approval
1. **Leader creates team** → Team status: PENDING
2. **Leader invites members** → Each member gets email invitation
3. **Members respond** → Each can approve/reject
4. **All approve** → Team status: ACTIVE
5. **Leader locks team** → Team status: LOCKED (ready for submission)
6. **Any rejection** → Team stays PENDING

### Submission Workflow (4 Stages)

For each stage (Synopsis, Progress 1-2, Final):

1. **Team leader uploads** submission (PDF on OneDrive)
2. **All members review** → Can approve/reject
3. **If any reject** → Leader must re-upload
4. **All approve** → Submission status: APPROVED
5. **Supervisor reviews** → Gives score (0-10) + feedback
6. **Optional resubmission** → If deadline set
7. **Admin final score** → (0-20)

### Final Score Calculation
```
Supervisor Average = (Score1 + Score2 + Score3 + Score4) / 4
Final Score = Supervisor Average + Admin Score
Maximum = 30 points
```

### Leaderboard
Sorted by:
1. Final Score (DESC)
2. Submission Time (ASC)

---

## 📧 Email Events

Emails are sent for:
- ✅ OTP verification
- ✅ Team invitations
- ✅ Submission feedback
- ✅ Approval notifications
- ✅ Deadline reminders
- ✅ Supervisor request status
- ✅ Score updates

**Email Configuration in `.env`:**
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password  # NOT your actual password
SMTP_FROM_EMAIL=noreply@yourdom.com
```

⚠️ **Note:** Use Gmail app-specific password, not your regular password.

---

## 🤖 AI Chatbot (RAG)

Uses **Groq API** with Mixtral-8x7b model.

**Features:**
- FAQ knowledge base
- Role-specific responses
- Chat history per user
- Contextual answers

**FAQ Categories:**
- Enrollment
- Submission workflow
- Team management
- Scoring system
- General questions

**Setup:**
```
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL_NAME=mixtral-8x7b-32768
```

---

## 📁 File Storage

**OneDrive Integration:**
- Submissions stored as PDFs on OneDrive
- Only URLs stored in database
- File size limit: 50 MB
- Allowed types: PDF only

**Configuration:**
```
ONEDRIVE_TENANT_ID=your-tenant-id
ONEDRIVE_CLIENT_ID=your-client-id
ONEDRIVE_CLIENT_SECRET=your-secret
ONEDRIVE_FOLDER_ID=your-folder-id
```

---

## 🔒 Security

- **JWT:** 24-hour expiry, HS256 algorithm
- **OTP:** 6-digit, 5-minute expiry
- **Password:** bcrypt hashing for admins
- **CORS:** Configurable from environment
- **Rate Limiting:** 100 requests per minute (configurable)
- **Role-based Access Control:** Admin/Supervisor/Student
- **Audit Logs:** All admin actions logged

---

## 🚀 Deployment

### Backend Deployment (Azure App Service / Container Apps)

**Prerequisites:**
- PostgreSQL database
- OneDrive configured
- Groq API key

**Docker:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Deploy:**
```bash
az containerapp create \
  --resource-group my-rg \
  --name dpg-pms-api \
  --image myregistry.azurecr.io/dpg-pms:latest \
  --environment my-env \
  --target-port 8000 \
  --env-vars DATABASE_URL=... GROQ_API_KEY=...
```

### Frontend Deployment (Vercel)

**With Vercel:**
```bash
npm install -g vercel
vercel --prod
```

**With Azure Static Web Apps:**
```bash
az staticwebapp create \
  --name dpg-pms-web \
  --resource-group my-rg \
  --source https://github.com/yourusername/repo \
  --branch main \
  --app-location frontend
```

### Environment Variables (Production)

**Backend (.env production):**
```
DEBUG=false
DATABASE_URL=postgresql://user:pass@prod-db:5432/dpg
JWT_SECRET_KEY=<use-strong-key>
CORS_ORIGINS=https://yourdomain.com
```

**Frontend (.env.production):**
```
NEXT_PUBLIC_API_BASE_URL=https://api.yourdomain.com
```

---

## 📝 Configuration

### Database
Default uses PostgreSQL. Can also use Supabase:

```
DATABASE_URL=postgresql://[user]:[password]@db.supabase.co:5432/postgres
```

### Email
- **Gmail:** Use app-specific password
- **Custom SMTP:** Update SMTP_* variables
- **Test mode:** Disable EMAIL_NOTIFICATIONS

### File Storage
- **OneDrive:** Required for submissions
- **Azure Blob:** Alternative (needs implementation)
- **Local storage:** Not recommended for production

---

## 🐛 Troubleshooting

### OTP Not Arriving
- Check SMTP credentials
- Verify email provider settings
- Check spam folder
- Enable "Less secure app access" (Gmail)

### Login Failing
- Verify database connection
- Check JWT_SECRET_KEY is set
- Clear browser cache/cookies
- Check token expiry (24 hours)

### Submissions Not Saving
- Verify OneDrive credentials
- Check file size (max 50 MB)
- Ensure folder ID is correct
- Check OneDrive permissions

### Chatbot Not Responding
- Verify Groq API key is valid
- Check API rate limits
- Verify model name is correct

---

## 📚 Project Structure

```
dpg-pms/
├── backend/
│   ├── app/
│   │   ├── core/          # Config, security, JWT, OTP
│   │   ├── models/        # SQLAlchemy ORM models
│   │   ├── schemas/       # Pydantic request/response
│   │   ├── services/      # Business logic
│   │   ├── routes/        # API endpoints
│   │   ├── db/            # Database utilities
│   │   └── main.py        # FastAPI app
│   ├── alembic/           # Database migrations
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── app/               # Next.js App Router
│   │   ├── auth/
│   │   ├── admin/
│   │   ├── student/
│   │   ├── supervisor/
│   │   └── page.tsx
│   ├── components/        # React components
│   ├── services/          # API clients
│   ├── store/             # Zustand state
│   ├── utils/             # Utilities
│   ├── package.json
│   └── .env.local
│
├── .gitignore
├── README.md
└── DEPLOYMENT.md (this file)
```

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m "Add new feature"`
4. Push: `git push origin feature/new-feature`
5. Create Pull Request

---

## 📄 License

DPG ITM College © 2024

---

## 📞 Support

For issues or questions:
- Email: support@dpg-itm.edu.in
- Admin Dashboard: `/admin/dashboard`
- Documentation: See README.md files in each folder

---

**Last Updated:** January 2024
**Version:** 1.0.0
