from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.database import get_db
from app.models.models import Project, Team, Submission, SubmissionFeedback, User
from app.schemas.schemas import ProjectCreate, ProjectResponse, LeaderboardEntry, LeaderboardResponse
from app.core.security import JWTHandler
from app.services.email_service import EmailService
import secrets
from datetime import datetime
import json

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """
    Admin creates a new project
    """
    # Generate enrollment token
    token = secrets.token_urlsafe(32)
    enrollment_link = f"http://localhost:3000/enroll?token={token}"
    
    new_project = Project(
        title=project.title,
        description=project.description,
        branch=project.branch,
        batch=project.batch,
        deadline=project.deadline,
        enrollment_token=token,
        enrollment_link=enrollment_link
    )
    
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return new_project

@router.get("/", response_model=list[ProjectResponse])
async def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all projects
    """
    projects = db.query(Project).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    """
    Get project details
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project

@router.post("/{project_id}/enroll")
async def enroll_in_project(
    project_id: int,
    token: str,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Student enrolls in a project using token
    """
    from app.models.models import ProjectEnrollment
    
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Verify token
    if project.enrollment_token != token:
        raise HTTPException(status_code=400, detail="Invalid enrollment token")
    
    # Check if already enrolled
    existing = db.query(ProjectEnrollment).filter(
        ProjectEnrollment.project_id == project_id,
        ProjectEnrollment.user_id == user_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this project")
    
    # Create enrollment
    enrollment = ProjectEnrollment(
        project_id=project_id,
        user_id=user_id
    )
    db.add(enrollment)
    db.commit()
    
    return {
        "status": "success",
        "message": "Enrolled in project",
        "project_id": project_id
    }

@router.get("/{project_id}/leaderboard", response_model=LeaderboardResponse)
async def get_project_leaderboard(project_id: int, db: Session = Depends(get_db)):
    """
    Get final leaderboard for a project
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get all teams for this project with their final scores
    teams = db.query(Team).filter(Team.project_id == project_id).all()
    
    entries = []
    
    for idx, team in enumerate(teams, 1):
        # Calculate supervisor average
        supervisor_feedbacks = db.query(SubmissionFeedback).join(
            Submission
        ).filter(
            Submission.team_id == team.id,
            SubmissionFeedback.supervisor_score != None
        ).all()
        
        supervisor_avg = 0
        if supervisor_feedbacks:
            supervisor_avg = sum(fb.supervisor_score for fb in supervisor_feedbacks) / len(supervisor_feedbacks)
        
        # Get admin score (latest feedback)
        admin_feedback = db.query(SubmissionFeedback).join(
            Submission
        ).filter(
            Submission.team_id == team.id,
            SubmissionFeedback.admin_score != None
        ).order_by(SubmissionFeedback.created_at.desc()).first()
        
        admin_score = admin_feedback.admin_score if admin_feedback else 0
        
        # Calculate final score (max 30)
        final_score = supervisor_avg + admin_score
        
        # Get submission time
        submission = db.query(Submission).filter(
            Submission.team_id == team.id,
            Submission.stage == "final_submission"
        ).order_by(Submission.submitted_at.asc()).first()
        
        submission_time = submission.submitted_at if submission else datetime.now()
        
        # Get team members names
        members = [member.name for member in team.members]
        
        entry = LeaderboardEntry(
            rank=idx,
            team_name=team.name,
            members=members,
            supervisor_avg=round(supervisor_avg, 2),
            admin_score=admin_score,
            final_score=round(final_score, 2),
            submission_time=submission_time
        )
        entries.append(entry)
    
    # Sort by final score DESC, then submission time ASC
    entries.sort(key=lambda x: (-x.final_score, x.submission_time))
    
    # Re-rank after sorting
    for idx, entry in enumerate(entries, 1):
        entry.rank = idx
    
    return LeaderboardResponse(
        entries=entries,
        project_id=project_id,
        total_teams=len(teams)
    )

@router.put("/{project_id}")
async def update_project(
    project_id: int,
    project_update: ProjectCreate,
    db: Session = Depends(get_db)
):
    """
    Update project details
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project.title = project_update.title
    project.description = project_update.description
    project.branch = project_update.branch
    project.batch = project_update.batch
    project.deadline = project_update.deadline
    
    db.commit()
    db.refresh(project)
    
    return project

@router.delete("/{project_id}")
async def delete_project(project_id: int, db: Session = Depends(get_db)):
    """
    Delete a project
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    
    return {
        "status": "success",
        "message": "Project deleted"
    }
