# DPG Project Management System

A comprehensive project management system for educational institutions built with modern web technologies and AI-powered support.

## ✨ Features

- ✅ **OTP + JWT Authentication** - Secure 2-factor login with 5-min OTP and 24-hr JWT
- ✅ **Role-Based Access Control** - Admin, Supervisor, and Student roles
- ✅ **Project Management** - Create and manage projects with enrollment tokens
- ✅ **Team System** - Teams with leader, members, and approval workflows
- ✅ **4-Stage Submissions** - Synopsis, Progress Report 1-2, Final Submission
- ✅ **Supervisor Scoring** - Score submissions (0-10) with feedback
- ✅ **Admin Scoring** - Final scores (0-20) and audit logs
- ✅ **Auto-Leaderboard** - Real-time ranking with final scores
- ✅ **Email Notifications** - For OTP, invites, feedback, deadlines
- ✅ **RAG Chatbot** - AI-powered FAQ using Groq LLM
- ✅ **OneDrive Integration** - PDF file storage with metadata in database
- ✅ **Audit Trail** - Complete admin action logging

## 📊 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Next.js 14, React 18, Tailwind CSS, Zustand |
| **Backend** | FastAPI, SQLAlchemy, Alembic |
| **Database** | PostgreSQL / Supabase |
| **Storage** | OneDrive (PDFs) |
| **Auth** | JWT + OTP (SMS/Email) |
| **AI/LLM** | Groq API (Mixtral-8x7b) |
| **Deployment** | Azure (App Service / Static Web Apps / Container Apps) |

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- PostgreSQL 13+ (or Supabase account)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run server
uvicorn app.main:app --reload --port 8000
```

**Backend URL:** http://localhost:8000
**API Docs:** http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

**Frontend URL:** http://localhost:3000

## 📋 API Endpoints

### Authentication
```
POST   /api/auth/login              # Send OTP
POST   /api/auth/verify-otp         # Verify OTP & get JWT
POST   /api/auth/admin-login        # Admin password login
GET    /api/auth/verify-token       # Verify JWT
```

### Projects & Enrollment
```
POST   /api/projects                # Create project (Admin)
GET    /api/projects                # List projects
GET    /api/projects/{id}           # Get project details
POST   /api/projects/{id}/enroll    # Enroll student
GET    /api/projects/{id}/leaderboard  # Final rankings
```

### Teams
```
POST   /api/teams                   # Create team (Student)
GET    /api/teams/{id}              # Get team details
POST   /api/teams/{id}/invite       # Invite member
POST   /api/teams/{id}/invitations/{inv_id}/respond  # Accept/reject
POST   /api/teams/{id}/lock         # Lock team for submission
GET    /api/teams/{id}/members      # List members
```

### Submissions (4-Stage)
```
POST   /api/submissions/{team_id}/{stage}      # Upload
POST   /api/submissions/{id}/approve            # Member approval
GET    /api/submissions/{id}                    # Get details
POST   /api/submissions/{id}/supervisor-feedback  # Supervisor score
POST   /api/submissions/{id}/admin-feedback     # Admin score
GET    /api/submissions/{id}/feedback           # Get feedback
```

### Admin Panel
```
GET    /api/admin/requests          # Supervisor requests
POST   /api/admin/requests/{id}/approve      # Approve request
POST   /api/admin/requests/{id}/reject       # Reject request
GET    /api/admin/logs              # Audit logs
GET    /api/admin/stats             # Dashboard stats
```

### Chatbot
```
POST   /api/chatbot/ask             # Ask chatbot
GET    /api/chatbot/sessions        # Chat history
DELETE /api/chatbot/sessions/{id}   # Delete session
```

## 🗂️ Project Structure

```
dpg-pms/
├── backend/
│   ├── app/
│   │   ├── core/              # Config, JWT, OTP, Security
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   ├── routes/            # API routes
│   │   ├── db/                # Database config
│   │   └── main.py            # FastAPI app
│   ├── alembic/               # Database migrations
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── app/                   # Next.js pages
│   │   ├── auth/              # Login, OTP verify
│   │   ├── admin/             # Admin dashboard
│   │   ├── student/           # Student dashboard
│   │   └── supervisor/        # Supervisor dashboard
│   ├── components/            # Reusable components
│   ├── services/              # API clients
│   ├── store/                 # Zustand state management
│   ├── utils/                 # Helper utilities
│   └── package.json
│
├── .gitignore
├── README.md                  # This file
├── DEPLOYMENT.md              # Detailed deployment guide
└── .env.local                 # Environment variables
```

## 🔐 Security Features

- **JWT Tokens:** 24-hour expiry, HS256 algorithm
- **OTP:** 6-digit code, 5-minute expiry
- **Password Hashing:** bcrypt for admin passwords
- **CORS:** Environment-configurable origins
- **Rate Limiting:** 100 req/min (configurable)
- **Role Guards:** All endpoints protected by role
- **Audit Logs:** Complete admin action trail
- **File Validation:** Size limits and type checking

## 📊 Database Tables

### Core Tables
- **Users** - Stores user profiles, roles, authentication
- **Projects** - Project definitions with enrollment tokens
- **Teams** - Team groupings with leader and members
- **Submissions** - 4-stage submission workflow
- **SubmissionApprovals** - Member approvals per submission
- **SubmissionFeedback** - Supervisor and admin scores
- **SupervisorRequests** - Access request management
- **AdminLogs** - Audit trail for all admin actions

### Support Tables
- **OTPTokens** - OTP storage and expiry
- **TeamInvitations** - Team member invitations
- **ProjectEnrollments** - Student enrollments
- **Notifications** - In-app notifications
- **ChatSessions** - Chatbot conversation history

## 🎯 Workflow Examples

### Student Login & Enrollment
1. Student enters email → OTP sent
2. Enters OTP → JWT token issued
3. Redirected to `/student/dashboard`
4. Clicks "Enroll Project" with provided token
5. Auto-mapped to project

### Team Creation & Submission
1. Student creates team → Adds name
2. Invites members via email → Members receive invites
3. Members accept → Team becomes ACTIVE
4. Leader uploads submission → All members review
5. If all approve → Supervisor sees for review
6. Supervisor scores (0-10) → Admin adds final score (0-20)

### Admin Supervisor Access
1. Supervisor applies for access → `/request-access`
2. Admin reviews `/admin/requests`
3. Approves → Supervisor user created
4. Supervisor receives login email

## 📧 Email Configuration

Configure in `.env`:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=app-specific-password  # Not your actual password
SMTP_FROM_EMAIL=noreply@yourdomain.com
```

⚠️ **Gmail Users:** Use [App-specific password](https://myaccount.google.com/apppasswords), not your regular password.

## 🤖 AI Chatbot

Uses Groq API with Mixtral-8x7b model for contextual FAQ answers.

**Configure:**
```env
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL_NAME=mixtral-8x7b-32768
```

**Features:**
- Role-aware responses
- FAQ knowledge base
- Chat history per user
- Conversation context

## 📁 File Storage

**OneDrive Integration:**
- Submissions stored as PDFs on OneDrive
- Only URLs stored in database
- Supports up to 50 MB per file
- Automatic folder organization

**Configure:**
```env
ONEDRIVE_TENANT_ID=your-tenant-id
ONEDRIVE_CLIENT_ID=your-client-id
ONEDRIVE_CLIENT_SECRET=your-secret
ONEDRIVE_FOLDER_ID=your-folder-id
```

## 🚀 Deployment

### Quick Deploy on Azure

**Backend (Container Apps):**
```bash
# Create ACR
az acr create -g mygroup -n myregistry --sku Basic

# Build and push image
az acr build -r myregistry -t dpg-pms:latest .

# Deploy to Container Apps
az containerapp create \
  -n dpg-api \
  -g mygroup \
  --image myregistry.azurecr.io/dpg-pms:latest \
  --target-port 8000 \
  --environment myenv
```

**Frontend (Static Web Apps or Vercel):**
```bash
# With Vercel (recommended)
npm install -g vercel
vercel --prod

# Or with Azure Static Web Apps
az staticwebapp create \
  -n dpg-web \
  -g mygroup \
  --source https://github.com/user/repo \
  --app-location frontend
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete guide.

## 📱 Responsive Design

- Mobile-first Tailwind CSS
- Works on desktop, tablet, mobile
- Progressive enhancement
- Accessible (WCAG 2.1 AA)

## 🧪 Testing

```bash
# Backend
cd backend
pip install pytest
pytest

# Frontend
cd frontend
npm test
```

## 📝 Environment Variables

### Backend (.env)
```
# App
APP_NAME=DPG Project Management System
DEBUG=false

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# JWT & Auth
JWT_SECRET_KEY=your-super-secret-key
OTP_EXPIRY_MINUTES=5

# Email
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=app-password

# OneDrive
ONEDRIVE_TENANT_ID=...
ONEDRIVE_CLIENT_ID=...
ONEDRIVE_CLIENT_SECRET=...
ONEDRIVE_FOLDER_ID=...

# Groq
GROQ_API_KEY=...

# Security
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=DPG Project Management System
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| OTP not arriving | Check SMTP credentials, email spam folder |
| Login fails | Verify DB connection, clear browser cache |
| Submissions not saving | Check OneDrive credentials, file size |
| API 500 errors | Check backend logs, verify .env variables |
| Chatbot not working | Verify Groq API key and rate limits |

## 📚 Documentation

- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - Complete deployment guide
- **[backend/README.md](./backend/README.md)** - Backend setup details
- **[frontend/README.md](./frontend/README.md)** - Frontend setup details
- **API Docs:** http://localhost:8000/docs (Swagger UI)

## 🤝 Contributing

1. Clone the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes and test
4. Commit: `git commit -m "Add your feature"`
5. Push: `git push origin feature/your-feature`
6. Create Pull Request

## 📄 License

© 2024 DPG ITM College. All rights reserved.

## 📞 Support & Contact

- **Email:** support@dpg-itm.edu.in
- **Admin Dashboard:** `/admin/dashboard`
- **Documentation:** See deployment guide
- **Issues:** Report via GitHub issues

---

**Status:** ✅ Production Ready
**Last Updated:** January 2024
**Version:** 1.0.0
