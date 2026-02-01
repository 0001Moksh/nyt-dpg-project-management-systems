# DPG PMS - Backend

FastAPI-based backend for the DPG Project Management System. Handles authentication, project management, submissions, scoring, and RAG chatbot integration.

## 🏗️ Folder Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Configuration management
│   ├── models.py                  # SQLAlchemy ORM models
│   ├── schemas.py                 # Pydantic validation schemas
│   │
│   ├── services/                  # Business logic
│   │   ├── __init__.py
│   │   ├── auth_service.py        # Authentication logic
│   │   ├── email_service.py       # SMTP email service
│   │   ├── rag_chatbot.py         # Groq LLM chatbot
│   │   ├── projects.py            # Project operations
│   │   ├── submissions.py         # Submission handling
│   │   ├── teams.py               # Team management
│   │   └── analytics.py           # Analytics & predictions
│   │
│   ├── routes/                    # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py                # /auth endpoints
│   │   ├── projects.py            # /projects endpoints
│   │   ├── teams.py               # /teams endpoints
│   │   ├── submissions.py         # /submissions endpoints
│   │   ├── chatbot.py             # /chatbot endpoints
│   │   ├── leaderboard.py         # /leaderboard endpoints
│   │   └── admin.py               # /admin endpoints
│   │
│   ├── middleware/                # Custom middleware
│   │   ├── __init__.py
│   │   ├── auth_middleware.py     # JWT verification
│   │   ├── rate_limit.py          # Rate limiting
│   │   └── error_handler.py       # Error handling
│   │
│   ├── utils/                     # Utility functions
│   │   ├── __init__.py
│   │   ├── security.py            # Security utilities
│   │   ├── validators.py          # Validators
│   │   ├── decorators.py          # Custom decorators
│   │   ├── constants.py           # App constants
│   │   └── exceptions.py          # Custom exceptions
│   │
│   ├── db/                        # Database utilities
│   │   ├── __init__.py
│   │   ├── session.py             # DB session management
│   │   └── base.py                # Base models
│   │
│   └── deps.py                    # Dependency injection
│
├── migrations/                    # Alembic database migrations
│   ├── alembic.ini
│   ├── env.py
│   └── versions/
│
├── tests/                         # Unit and integration tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_projects.py
│   ├── test_submissions.py
│   └── test_chatbot.py
│
├── docs/                          # Documentation
│   ├── architecture.md
│   ├── api_guide.md
│   └── deployment.md
│
├── scripts/                       # Utility scripts
│   ├── create_admin.py            # Create admin user
│   ├── seed_data.py               # Seed test data
│   └── generate_links.py          # Generate enrollment links
│
├── .env.example                   # Environment template
├── requirements.txt               # Python dependencies
├── main.py                        # Entry point
├── README.md                      # This file
└── Dockerfile                     # Docker configuration
```

## 🚀 Quick Start

### 1. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example
cp .env.example .env

# Edit .env with your values
nano .env
# or use your editor of choice
```

**Key environment variables:**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dpg_pms
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
JWT_SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
```

### 4. Database Setup

```bash
# Create database
createdb dpg_pms

# Run migrations
alembic upgrade head

# Seed data (optional)
python scripts/seed_data.py
```

### 5. Run Server

```bash
# Development
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🔐 Authentication System

### OTP-Based Login Flow

1. **Request OTP**
   ```bash
   POST /api/v1/auth/request-otp
   {
     "email": "student@dpg-itm.edu.in"
   }
   ```

2. **Verify OTP**
   ```bash
   POST /api/v1/auth/verify-otp
   {
     "email": "student@dpg-itm.edu.in",
     "otp": "123456"
   }
   ```

3. **Response**
   ```json
   {
     "success": true,
     "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
     "user": {
       "id": "user_123",
       "email": "student@dpg-itm.edu.in",
       "name": "John Doe",
       "role": "STUDENT"
     }
   }
   ```

### JWT Token Usage

```bash
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## 📧 SMTP Email Service

### Supported Providers

#### Gmail
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
```

#### SendGrid
```env
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.your-sendgrid-api-key
```

#### Microsoft 365 / Outlook
```env
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USER=your-email@outlook.com
SMTP_PASSWORD=your-password
```

### Email Functions

```python
from app.services.email_service import email_service

# Send OTP
await email_service.send_otp_email("user@example.com", "123456", "User Name")

# Send team approval
await email_service.send_team_approval_email(
  "user@example.com",
  "Team Alpha",
  "Project Name",
  "https://approval-link.com"
)

# Send submission notification
await email_service.send_submission_notification(
  "supervisor@example.com",
  "Team Beta",
  "SYNOPSIS",
  "Project Name"
)

# Send feedback
await email_service.send_review_feedback_email(
  "team@example.com",
  "Team Gamma",
  "PROGRESS_1",
  "Good work. Improve documentation.",
  8.5
)
```

## 🤖 RAG Chatbot with Groq LLM

### Setup

```env
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL_NAME=mixtral-8x7b-32768
```

### Usage

```bash
# Send message
POST /api/v1/chatbot/chat
{
  "message": "How do I submit my project?",
  "role": "STUDENT",
  "chat_history": []
}

# Get FAQ
POST /api/v1/chatbot/faq
{
  "question": "What are the submission deadlines?",
  "role": "STUDENT"
}
```

### Role-Based Responses

The chatbot provides different prompts for:
- **STUDENT** - Project submission, team formation, scoring
- **SUPERVISOR** - Evaluation criteria, feedback, analytics
- **ADMIN** - Project setup, user management, system configuration

## 📊 Database Models

### User
```python
- id: String (PK)
- email: String (unique, indexed)
- name: String
- roll_no: String
- branch: String
- batch: String
- role: String (STUDENT, SUPERVISOR, ADMIN)
- otp_code: String
- otp_expiry: DateTime
- is_active: Boolean
```

### Project
```python
- id: String (PK)
- title: String
- description: Text
- branch: String
- batch: String
- created_by_id: FK(User)
- enrollment_status: String (OPEN, CLOSED, ARCHIVED)
- enrollment_link: String (unique)
```

### Team
```python
- id: String (PK)
- name: String
- project_id: FK(Project)
- leader_id: FK(User)
- supervisor_id: FK(User)
- status: String (FORMING, ACTIVE, COMPLETED)
```

### Submission
```python
- id: String (PK)
- team_id: FK(Team)
- stage: String (SYNOPSIS, PROGRESS_1, PROGRESS_2, FINAL_SUBMISSION)
- document_url: String
- document_name: String
- team_approval_status: String
- supervisor_review_status: String
- supervisor_score: Float
- supervisor_feedback: Text
```

### StageScore
```python
- id: String (PK)
- team_id: FK(Team)
- stage: String
- supervisor_score: Float (0-10)
- admin_score: Float (0-20)
- final_score: Float (0-30)
```

## 🔗 API Endpoints

### Authentication `/api/v1/auth`
```
POST   /request-otp         - Send OTP to email
POST   /verify-otp          - Verify OTP and login
GET    /me                  - Get current user
POST   /logout              - Logout
POST   /refresh-token       - Refresh JWT token
```

### Projects `/api/v1/projects`
```
GET    /                    - List all projects
GET    /{id}                - Get project by ID
POST   /                    - Create project (Admin)
PUT    /{id}                - Update project (Admin)
POST   /{id}/generate-enrollment-link - Generate link
GET    /{id}/teams          - Get project teams
GET    /{id}/stats          - Get project statistics
```

### Teams `/api/v1/teams`
```
GET    /{id}                - Get team details
POST   /{id}/join           - Join team
POST   /{id}/leave          - Leave team
POST   /{id}/members/{mid}/approve - Approve member
POST   /{id}/assign-supervisor - Assign supervisor
```

### Submissions `/api/v1/submissions`
```
GET    /                    - List submissions
GET    /{id}                - Get submission details
POST   /                    - Upload submission
POST   /{id}/approve        - Team approve submission
POST   /{id}/reject         - Team reject submission
POST   /{id}/review         - Supervisor review & score
```

### Chatbot `/api/v1/chatbot`
```
POST   /chat                - Send message
POST   /faq                 - Get FAQ answer
GET    /sessions            - List chat sessions
DELETE /sessions/{id}       - Clear session
```

### Leaderboard `/api/v1/leaderboard`
```
GET    /                    - Get leaderboard
GET    /?projectId=...      - Get project leaderboard
```

### Admin `/api/v1/admin`
```
GET    /users               - List users
POST   /users               - Create user
GET    /analytics           - Analytics dashboard
GET    /reports             - Generate reports
```

## 🔄 Scoring System

### Calculation
```
Supervisor Average = (S1 + S2 + S3 + S4) / 4    (out of 10)
Admin Score = provided manually                   (out of 20)
Final Score = Supervisor Average + Admin Score   (out of 30)
```

### Example
```
Stage 1: 8/10
Stage 2: 7.5/10
Stage 3: 9/10
Stage 4: 8.5/10

Supervisor Average = (8 + 7.5 + 9 + 8.5) / 4 = 8.25
Admin Score = 18/20
Final Score = 8.25 + 18 = 26.25/30
```

## 🧪 Testing

### Unit Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app tests/
```

### Example Test
```python
def test_otp_request(client, db):
    response = client.post("/api/v1/auth/request-otp", 
                          json={"email": "test@example.com"})
    assert response.status_code == 200
    assert response.json()["success"] == True
```

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t dpg-pms-backend .
```

### Run Container
```bash
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:pass@db:5432/dpg_pms \
  -e SMTP_HOST=smtp.gmail.com \
  -e SMTP_USER=your-email@gmail.com \
  -e SMTP_PASSWORD=your-password \
  --name dpg-pms-backend \
  dpg-pms-backend
```

### Docker Compose
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: dpg_pms
      POSTGRES_USER: dpg_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://dpg_user:secure_password@db:5432/dpg_pms
      SMTP_HOST: smtp.gmail.com
      SMTP_USER: your-email@gmail.com
      SMTP_PASSWORD: your-app-password
      GROQ_API_KEY: your-groq-api-key
    depends_on:
      - db

volumes:
  postgres_data:
```

## 📈 Performance Optimization

### Database Indexing
```python
# Index on frequently queried fields
email = Column(String, unique=True, index=True)
created_at = Column(DateTime, index=True)
```

### Query Optimization
```python
# Use eager loading
teams = db.query(Team).options(
    joinedload(Team.members).joinedload(TeamMember.user)
).all()
```

### Connection Pooling
```env
DATABASE_POOL_SIZE=20
DATABASE_POOL_RECYCLE=3600
```

## 🔒 Security Best Practices

✅ **OTP Authentication** - No plain passwords  
✅ **JWT Tokens** - Secure session management  
✅ **Password Hashing** - bcrypt for admin passwords  
✅ **SQL Injection Prevention** - SQLAlchemy ORM  
✅ **CORS** - Whitelist allowed origins  
✅ **Rate Limiting** - Prevent brute force attacks  
✅ **Environment Variables** - No secrets in code  
✅ **HTTPS** - All production traffic encrypted  
✅ **Input Validation** - Pydantic schemas  
✅ **Error Handling** - No sensitive data in errors  

## 📝 Logging

Configure in `config.py`:
```python
LOG_LEVEL = "info"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE_PATH = "/var/log/dpg-pms/app.log"
```

### Usage
```python
import logging
logger = logging.getLogger(__name__)

logger.info("User logged in")
logger.warning("OTP verification failed")
logger.error("Database connection error")
```

## 🚀 Deployment Checklist

- [ ] Set all environment variables
- [ ] Run database migrations
- [ ] Configure SMTP credentials
- [ ] Add Groq API key
- [ ] Enable CORS for frontend domain
- [ ] Configure OneDrive/Azure Storage
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Test email notifications
- [ ] Test authentication flow
- [ ] Load testing
- [ ] Security audit

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org)
- [Groq API Documentation](https://console.groq.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs)
- [Alembic Migrations](https://alembic.sqlalchemy.org)

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and add tests
3. Run tests: `pytest`
4. Submit PR

## 📞 Support

For backend-specific issues, check GitHub issues or contact the team.

---

**Backend for DPG Project Management System**
