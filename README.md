# DPG Project Management System (PMS)

A comprehensive, large-scale project management system for DPG ITM College by NexyugTech Company. Built with React frontend and FastAPI backend, featuring role-based access, SMTP email notifications, OTP authentication, and Groq LLM-powered RAG chatbot.

## 📋 Project Overview

The DPG PMS is designed to manage academic projects with three main roles:
- **Students**: Form teams, submit deliverables, track progress
- **Supervisors**: Review submissions, provide feedback, score stages
- **Admins**: Manage projects, assign supervisors, generate reports

### Key Features

✅ **Email OTP Authentication** - Secure login via SMTP  
✅ **Role-Based Dashboards** - Customized interfaces for each role  
✅ **Team Management** - Form teams, manage members, lock teams  
✅ **4-Stage Project Submission** - Synopsis, Progress 1, Progress 2, Final Submission  
✅ **Supervisor Review System** - Score submissions (0-10), provide feedback  
✅ **Leaderboard** - Rank teams by final score (30 points total)  
✅ **SMTP Email Notifications** - OTP, team approvals, submission alerts, feedback  
✅ **RAG Chatbot** - Role-specific AI assistant powered by Groq LLM  
✅ **Analytics & Risk Prediction** - Predict delays and project risks  
✅ **OneDrive Integration** - Secure file storage for submissions  
✅ **Scalable Architecture** - Separate frontend and backend repos ready for microservices  

## 🏗️ Project Structure

```
DPG-PMS/
├── frontend/                    # React/Next.js Frontend
│   ├── app/
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   ├── globals.css         # Global styles
│   │   ├── (auth)/             # Auth routes
│   │   ├── (student)/          # Student dashboard
│   │   ├── (supervisor)/       # Supervisor dashboard
│   │   └── (admin)/            # Admin dashboard
│   ├── components/
│   │   ├── ui/                 # shadcn/ui components
│   │   ├── auth/               # Auth components
│   │   ├── dashboard/          # Dashboard components
│   │   └── common/             # Shared components
│   ├── services/
│   │   ├── api.ts              # API client
│   │   ├── auth.ts             # Auth service
│   │   └── projects.ts         # Project service
│   ├── hooks/                  # Custom hooks
│   ├── store/                  # Zustand stores
│   ├── types/                  # TypeScript types
│   └── utils/                  # Utilities
│
├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── main.py             # FastAPI app
│   │   ├── config.py           # Configuration
│   │   ├── models.py           # Database models
│   │   ├── schemas.py          # Pydantic schemas
│   │   ├── services/
│   │   │   ├── auth_service.py       # Auth logic
│   │   │   ├── email_service.py      # SMTP emails
│   │   │   ├── rag_chatbot.py        # Groq LLM
│   │   │   ├── projects.py           # Project logic
│   │   │   └── submissions.py        # Submission logic
│   │   ├── routes/
│   │   │   ├── auth.py         # Auth endpoints
│   │   │   ├── projects.py     # Project endpoints
│   │   │   ├── teams.py        # Team endpoints
│   │   │   ├── submissions.py  # Submission endpoints
│   │   │   ├── chatbot.py      # Chatbot endpoints
│   │   │   └── admin.py        # Admin endpoints
│   │   ├── middleware/         # Custom middleware
│   │   └── utils/              # Utilities
│   ├── migrations/             # Database migrations
│   ├── tests/                  # Unit tests
│   ├── requirements.txt        # Python dependencies
│   └── main.py                 # Entry point
│
├── .env.example                 # Environment template
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ (for frontend)
- Python 3.9+ (for backend)
- PostgreSQL 12+
- SMTP account (Gmail, SendGrid, etc.)
- Groq API key for LLM

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp ../.env.example .env.local

# Update with your values
# NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

# Run development server
npm run dev
```

Visit `http://localhost:3000`

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example .env

# Update with your values
# DATABASE_URL=postgresql://user:password@localhost:5432/dpg_pms
# SMTP_HOST=smtp.gmail.com
# SMTP_USER=your-email@gmail.com
# SMTP_PASSWORD=your-app-password
# GROQ_API_KEY=your-groq-api-key

# Run database migrations
alembic upgrade head

# Run development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` for API documentation

## 🔐 Environment Variables

See `.env.example` for the complete list. Key variables:

```env
# Frontend
NEXT_PUBLIC_API_BASE_URL=https://your-api-domain.com
NEXT_PUBLIC_APP_NAME=DPG Project Management System

# Backend API
FASTAPI_BASE_URL=https://your-api-domain.com

# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/dpg_pms

# SMTP Email (Gmail example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password

# Authentication
JWT_SECRET_KEY=your-super-secret-jwt-key
OTP_EXPIRY_MINUTES=5
OTP_LENGTH=6

# Groq LLM
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL_NAME=mixtral-8x7b-32768

# OneDrive/Azure Storage
ONEDRIVE_CLIENT_ID=your-client-id
ONEDRIVE_CLIENT_SECRET=your-client-secret
ONEDRIVE_TENANT_ID=your-tenant-id
ONEDRIVE_FOLDER_ID=your-folder-id

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,https://your-domain.com
```

## 📧 SMTP Configuration

### Gmail Setup
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Use app password in `SMTP_PASSWORD`

### SendGrid Setup
1. Create API key at https://app.sendgrid.com/settings/api_keys
2. Use `apikey` as SMTP_USER and API key as SMTP_PASSWORD

### Other Providers
- Microsoft 365: `smtp.office365.com:587`
- Outlook: `smtp-mail.outlook.com:587`
- AWS SES: `email-smtp.region.amazonaws.com:587`

## 🔌 API Endpoints

### Authentication
```
POST   /api/v1/auth/request-otp      - Request OTP
POST   /api/v1/auth/verify-otp       - Verify OTP and Login
GET    /api/v1/auth/me               - Get current user
POST   /api/v1/auth/logout           - Logout
```

### Projects
```
GET    /api/v1/projects              - List projects
POST   /api/v1/projects              - Create project
GET    /api/v1/projects/{id}         - Get project
PUT    /api/v1/projects/{id}         - Update project
POST   /api/v1/projects/{id}/generate-enrollment-link
```

### Teams
```
GET    /api/v1/teams/{id}            - Get team
POST   /api/v1/teams/{id}/join       - Join team
POST   /api/v1/teams/{id}/leave      - Leave team
POST   /api/v1/teams/{id}/members/{memberId}/approve
```

### Submissions
```
GET    /api/v1/submissions           - List submissions
POST   /api/v1/submissions           - Upload submission
POST   /api/v1/submissions/{id}/approve
POST   /api/v1/submissions/{id}/reject
POST   /api/v1/submissions/{id}/review - Supervisor review
```

### Chatbot
```
POST   /api/v1/chatbot/chat          - Send message
POST   /api/v1/chatbot/faq           - Get FAQ answer
```

### Admin
```
GET    /api/v1/admin/users           - List users
POST   /api/v1/admin/users           - Create user
GET    /api/v1/admin/analytics       - Analytics dashboard
GET    /api/v1/leaderboard           - Leaderboard
```

Full API documentation: `http://localhost:8000/docs`

## 🎨 Frontend Architecture

### Authentication Flow
1. User enters email → Request OTP
2. OTP sent via SMTP
3. User enters OTP → Verify
4. JWT token returned
5. User redirected based on role

### Role-Based Routes
- `/auth/login` - Login page
- `/student/*` - Student dashboard (protected)
- `/supervisor/*` - Supervisor dashboard (protected)
- `/admin/*` - Admin dashboard (protected)

### State Management (Zustand)
- `useAuthStore` - Authentication state
- `useProjectStore` - Project state
- `useNotificationStore` - Notifications

### API Client (SWR)
- Automatic caching
- Real-time updates
- Error handling
- Request deduplication

## 🗄️ Database Schema

### Core Tables
- **users** - User accounts (Student, Supervisor, Admin)
- **projects** - Project definitions
- **teams** - Student teams
- **team_members** - Team memberships
- **submissions** - Project submissions
- **stage_scores** - Scoring records
- **notifications** - Email/In-app notifications
- **chat_sessions** - Chatbot sessions
- **chat_messages** - Chat messages

### Relationships
```
Project → Teams → TeamMembers → Users
        → Submissions → StageScores
Users → Notifications
Users → ChatSessions → ChatMessages
```

## 🤖 RAG Chatbot

The system includes a role-specific RAG chatbot powered by **Groq LLM**:

### Features
- **Role-Based Responses** - Different prompts for Student/Supervisor/Admin
- **Chat History** - Maintains conversation context
- **FAQ Database** - Quick answers for common questions
- **Document Context** - References project documentation

### Usage
```bash
# Backend endpoint
POST /api/v1/chatbot/chat
{
  "message": "How do I submit my project?",
  "role": "STUDENT"
}

# Response
{
  "success": true,
  "response": "To submit your project...",
  "tokens_used": 150
}
```

## 📊 Scoring System

### Stage Scoring (Supervisor)
- Each stage scored out of 10
- 4 stages total
- Supervisor Average = Sum of all scores / 4

### Final Scoring
- Supervisor Average: out of 10
- Admin Score: out of 20
- **Final Score = Supervisor Average + Admin Score** (out of 30)

### Leaderboard
Teams ranked by final score (descending)

## 🔔 Email Notifications

The system sends emails for:
- **OTP Login** - 6-digit codes, 5-minute validity
- **Team Approval** - Invitation links for members
- **Supervisor Assignment** - Notify supervisors of teams
- **Submission Alerts** - Notify supervisors of submissions
- **Review Feedback** - Send scores and feedback to teams
- **Deadline Reminders** - Upcoming submission deadlines

## 🧪 Testing

### Frontend Tests
```bash
cd frontend
npm run test
npm run test:coverage
```

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app
```

## 📦 Deployment

### Frontend (Vercel)
```bash
vercel deploy
```

### Backend (Azure)
```bash
# Build Docker image
docker build -t dpg-pms .

# Push to Azure Container Registry
az acr build --registry your-registry --image dpg-pms:latest .

# Deploy to Azure App Service
az webapp deployment source config-zip --resource-group your-rg --name your-app --src-path app.zip
```

## 🛡️ Security Best Practices

✅ **OTP Authentication** - No password stored  
✅ **JWT Tokens** - Secure session management  
✅ **HTTPS Only** - All production traffic encrypted  
✅ **CORS Enabled** - Cross-origin restrictions  
✅ **SQL Injection Prevention** - SQLAlchemy ORM  
✅ **Rate Limiting** - Prevent abuse (implement in production)  
✅ **Role-Based Access Control** - Routes protected by role  
✅ **Environment Variables** - Sensitive data not in code  

## 📝 Logging

Logs are written to:
- **Development**: Console output
- **Production**: `/var/log/dpg-pms/app.log`

Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

## 🐛 Troubleshooting

### SMTP Connection Error
- Check credentials in `.env`
- Verify SMTP server settings
- For Gmail, ensure app password is used (not account password)

### Database Connection Error
- Ensure PostgreSQL is running
- Check `DATABASE_URL` format
- Run migrations: `alembic upgrade head`

### CORS Error
- Verify frontend URL in `CORS_ORIGINS`
- Check `NEXT_PUBLIC_API_BASE_URL`

### OTP Not Received
- Check SMTP configuration
- Verify email address
- Check spam/junk folder

## 📚 Documentation

- [API Documentation](http://localhost:8000/docs)
- [Frontend Setup Guide](./frontend/README.md)
- [Backend Setup Guide](./backend/README.md)
- [Database Schema](./backend/docs/schema.md)
- [Architecture Overview](./docs/architecture.md)

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/your-feature`
4. Open Pull Request

## 📄 License

NexyugTech Company - All Rights Reserved

## 👥 Support

For support, contact NexyugTech at https://nexyugtech.com

## 📞 Contact

**DPG ITM College**  
**NexyugTech Company**  
https://nexyugtech.com

---

**Built with ❤️ for DPG ITM College**
