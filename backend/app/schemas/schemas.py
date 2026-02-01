from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

# Auth Schemas
class LoginRequest(BaseModel):
    email: EmailStr

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str

class OTPVerifyResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: int
    name: str

class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenPayload(BaseModel):
    user_id: int
    email: str
    role: str

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str
    role: str

class UserCreate(UserBase):
    password: Optional[str] = None
    student_id: Optional[str] = None
    department: Optional[str] = None
    batch: Optional[str] = None
    teacher_id: Optional[str] = None
    department_supervisor: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Project Schemas
class ProjectCreate(BaseModel):
    title: str
    description: str
    branch: str
    batch: str
    deadline: datetime

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    branch: str
    batch: str
    deadline: datetime
    enrollment_link: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProjectEnrollRequest(BaseModel):
    token: str

# Team Schemas
class TeamCreate(BaseModel):
    name: str
    project_id: int

class TeamInviteRequest(BaseModel):
    invitee_email: EmailStr

class TeamResponse(BaseModel):
    id: int
    name: str
    status: str
    is_locked: bool
    leader_id: int
    project_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class TeamDetailResponse(TeamResponse):
    members: List[UserResponse]
    team_invitations: List['TeamInvitationResponse']

# Team Invitation Schemas
class TeamInvitationResponse(BaseModel):
    id: int
    invitee_email: str
    status: str
    invited_at: datetime
    
    class Config:
        from_attributes = True

class TeamInvitationApproveRequest(BaseModel):
    invitation_id: int
    approve: bool

# Submission Schemas
class SubmissionUploadRequest(BaseModel):
    stage: str
    file_url: str  # OneDrive URL

class SubmissionApprovalRequest(BaseModel):
    submission_id: int
    approve: bool

class SubmissionResponse(BaseModel):
    id: int
    team_id: int
    stage: str
    file_url: str
    approval_status: str
    submitted_at: datetime
    approved_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Feedback Schemas
class SupervisorFeedbackRequest(BaseModel):
    submission_id: int
    score: float = Field(..., ge=0, le=10)
    comments: str
    resubmission_deadline: Optional[datetime] = None

class AdminFeedbackRequest(BaseModel):
    submission_id: int
    score: float = Field(..., ge=0, le=20)
    comments: str

class FeedbackResponse(BaseModel):
    id: int
    supervisor_score: Optional[float]
    admin_score: Optional[float]
    comments: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Supervisor Request Schemas
class SupervisorRequestCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    teacher_id: str

class SupervisorRequestResponse(BaseModel):
    id: int
    name: str
    email: str
    department: str
    teacher_id: str
    status: str
    request_date: datetime
    
    class Config:
        from_attributes = True

class SupervisorRequestApproveRequest(BaseModel):
    request_id: int
    approve: bool

# Leaderboard Schemas
class LeaderboardEntry(BaseModel):
    rank: int
    team_name: str
    members: List[str]
    supervisor_avg: float
    admin_score: float
    final_score: float
    submission_time: datetime

class LeaderboardResponse(BaseModel):
    entries: List[LeaderboardEntry]
    project_id: int
    total_teams: int

# Chatbot Schemas
class ChatbotQuestion(BaseModel):
    question: str

class ChatbotResponse(BaseModel):
    answer: str
    session_id: int
    created_at: datetime

# Notification Schemas
class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Admin Log Schemas
class AdminLogResponse(BaseModel):
    id: int
    admin_id: int
    action: str
    resource_type: str
    resource_id: Optional[int]
    details: Optional[dict]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Update forward references for Pydantic V2
TeamDetailResponse.model_rebuild()
