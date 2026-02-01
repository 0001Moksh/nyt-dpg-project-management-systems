from sqlalchemy import Column, String, Integer, DateTime, Boolean, Enum, ForeignKey, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    roll_no = Column(String, nullable=True)
    branch = Column(String, nullable=True)
    batch = Column(String, nullable=True)
    role = Column(String, nullable=False)  # STUDENT, SUPERVISOR, ADMIN
    profile_image = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)
    otp_code = Column(String, nullable=True)
    otp_expiry = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    teams = relationship("Team", back_populates="leader")
    notifications = relationship("Notification", back_populates="recipient")
    chat_sessions = relationship("ChatSession", back_populates="user")


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    branch = Column(String, nullable=False)
    batch = Column(String, nullable=False)
    created_by_id = Column(String, ForeignKey("users.id"))
    enrollment_status = Column(String, default="OPEN")  # OPEN, CLOSED, ARCHIVED
    enrollment_link = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    teams = relationship("Team", back_populates="project")


class Team(Base):
    __tablename__ = "teams"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    project_id = Column(String, ForeignKey("projects.id"))
    leader_id = Column(String, ForeignKey("users.id"))
    supervisor_id = Column(String, ForeignKey("users.id"), nullable=True)
    status = Column(String, default="FORMING")  # FORMING, ACTIVE, COMPLETED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="teams")
    leader = relationship("User", back_populates="teams", foreign_keys=[leader_id])
    members = relationship("TeamMember", back_populates="team")
    submissions = relationship("Submission", back_populates="team")


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(String, primary_key=True)
    team_id = Column(String, ForeignKey("teams.id"))
    user_id = Column(String, ForeignKey("users.id"))
    role = Column(String, default="MEMBER")  # LEADER, MEMBER
    approval_status = Column(String, default="PENDING")  # PENDING, APPROVED, REJECTED
    joined_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    team = relationship("Team", back_populates="members")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String, primary_key=True)
    team_id = Column(String, ForeignKey("teams.id"))
    stage = Column(String, nullable=False)  # SYNOPSIS, PROGRESS_1, PROGRESS_2, FINAL_SUBMISSION
    document_url = Column(String, nullable=False)
    document_name = Column(String, nullable=False)
    team_approval_status = Column(String, default="PENDING")  # PENDING, APPROVED, REJECTED
    supervisor_review_status = Column(String, default="PENDING")  # PENDING, APPROVED, REJECTED
    supervisor_score = Column(Float, nullable=True)
    supervisor_feedback = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    team = relationship("Team", back_populates="submissions")


class StageScore(Base):
    __tablename__ = "stage_scores"

    id = Column(String, primary_key=True)
    team_id = Column(String, ForeignKey("teams.id"))
    stage = Column(String, nullable=False)
    supervisor_score = Column(Float, nullable=False)
    admin_score = Column(Float, nullable=True)
    final_score = Column(Float, nullable=True)
    scored_at = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True)
    recipient_id = Column(String, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String, default="BOTH")  # EMAIL, IN_APP, BOTH
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    recipient = relationship("User", back_populates="notifications")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String, primary_key=True)
    session_id = Column(String, ForeignKey("chat_sessions.id"))
    sender = Column(String, nullable=False)  # USER, BOT
    content = Column(Text, nullable=False)
    relevant_documents = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    session = relationship("ChatSession", back_populates="messages")
