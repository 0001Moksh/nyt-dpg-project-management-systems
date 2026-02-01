from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, Text, ForeignKey, Table, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum as PyEnum
from app.db.database import Base

class RoleEnum(str, PyEnum):
    ADMIN = "admin"
    SUPERVISOR = "supervisor"
    STUDENT = "student"

class SubmissionStageEnum(str, PyEnum):
    SYNOPSIS = "synopsis"
    PROGRESS_1 = "progress_1"
    PROGRESS_2 = "progress_2"
    FINAL_SUBMISSION = "final_submission"

class ApprovalStatusEnum(str, PyEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class TeamStatusEnum(str, PyEnum):
    PENDING = "pending"
    ACTIVE = "active"
    LOCKED = "locked"
    INACTIVE = "inactive"

# Association table for team members
team_members_table = Table(
    'team_members',
    Base.metadata,
    Column('team_id', Integer, ForeignKey('teams.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default=RoleEnum.STUDENT)
    password_hash = Column(String, nullable=True)  # For admins
    
    # Student fields
    student_id = Column(String, unique=True, nullable=True, index=True)
    department = Column(String, nullable=True)
    batch = Column(String, nullable=True)
    
    # Supervisor fields
    teacher_id = Column(String, unique=True, nullable=True, index=True)
    department_supervisor = Column(String, nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    teams = relationship("Team", secondary=team_members_table, back_populates="members")
    led_teams = relationship("Team", back_populates="leader", foreign_keys="Team.leader_id")
    submissions = relationship("Submission", back_populates="uploader")
    supervisor_feedbacks = relationship("SubmissionFeedback", back_populates="supervisor", foreign_keys="SubmissionFeedback.supervisor_id")
    admin_feedbacks = relationship("SubmissionFeedback", back_populates="admin", foreign_keys="SubmissionFeedback.admin_id")
    admin_logs = relationship("AdminLog", back_populates="admin")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    branch = Column(String, nullable=False)
    batch = Column(String, nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=False)
    enrollment_token = Column(String, unique=True, index=True, nullable=False)
    enrollment_link = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    teams = relationship("Team", back_populates="project")
    enrollments = relationship("ProjectEnrollment", back_populates="project")

class ProjectEnrollment(Base):
    __tablename__ = "project_enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="enrollments")
    user = relationship("User")

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    leader_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, default=TeamStatusEnum.PENDING)
    is_locked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="teams")
    leader = relationship("User", back_populates="led_teams", foreign_keys=[leader_id])
    members = relationship("User", secondary=team_members_table, back_populates="teams")
    team_invitations = relationship("TeamInvitation", back_populates="team")
    submissions = relationship("Submission", back_populates="team")

class TeamInvitation(Base):
    __tablename__ = "team_invitations"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    invitee_email = Column(String, nullable=False)
    status = Column(String, default=ApprovalStatusEnum.PENDING)
    invited_at = Column(DateTime(timezone=True), server_default=func.now())
    responded_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    team = relationship("Team", back_populates="team_invitations")

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)
    stage = Column(String, nullable=False)  # SubmissionStageEnum
    file_url = Column(String, nullable=False)  # OneDrive URL
    uploaded_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    approval_status = Column(String, default=ApprovalStatusEnum.PENDING)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    team = relationship("Team", back_populates="submissions")
    uploader = relationship("User", back_populates="submissions", foreign_keys=[uploaded_by])
    feedbacks = relationship("SubmissionFeedback", back_populates="submission")
    approvals = relationship("SubmissionApproval", back_populates="submission")

class SubmissionApproval(Base):
    __tablename__ = "submission_approvals"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String, default=ApprovalStatusEnum.PENDING)  # pending, approved, rejected
    responded_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    submission = relationship("Submission", back_populates="approvals")
    user = relationship("User")

class SubmissionFeedback(Base):
    __tablename__ = "submission_feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey('submissions.id'), nullable=False)
    supervisor_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    admin_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    supervisor_score = Column(Float, nullable=True)  # 0-10
    admin_score = Column(Float, nullable=True)  # 0-20
    comments = Column(Text, nullable=True)
    resubmission_deadline = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    submission = relationship("Submission", back_populates="feedbacks")
    supervisor = relationship("User", back_populates="supervisor_feedbacks", foreign_keys=[supervisor_id])
    admin = relationship("User", back_populates="admin_feedbacks", foreign_keys=[admin_id])

class SupervisorRequest(Base):
    __tablename__ = "supervisor_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    department = Column(String, nullable=False)
    teacher_id = Column(String, unique=True, nullable=False)
    status = Column(String, default=ApprovalStatusEnum.PENDING)  # pending, approved, rejected
    approved_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    request_date = Column(DateTime(timezone=True), server_default=func.now())
    approved_date = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    approver = relationship("User")

class AdminLog(Base):
    __tablename__ = "admin_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)
    resource_id = Column(Integer, nullable=True)
    details = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    admin = relationship("User", back_populates="admin_logs")

class OTPToken(Base):
    __tablename__ = "otp_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    otp = Column(String, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String, nullable=False)  # email_sent, team_invite, etc
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
