from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Submission, SubmissionFeedback, Team, User
from app.services.email_service import EmailService

router = APIRouter(prefix="/api/supervisor", tags=["supervisor"])

@router.get("/submissions")
async def get_pending_submissions(
    user_id: int,  # From JWT token
    db: Session = Depends(get_db)
):
    """
    Get all pending submissions assigned to supervisor
    Note: Need to implement supervisor assignment logic
    """
    # TODO: Implement supervisor assignment to teams/projects
    # For now, return empty list
    return {
        "supervisor_id": user_id,
        "submissions": []
    }

@router.get("/submissions/{submission_id}")
async def get_submission_detail(
    submission_id: int,
    user_id: int,  # From JWT token
    db: Session = Depends(get_db)
):
    """
    Get submission details for review
    """
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    team = submission.team
    
    return {
        "submission_id": submission.id,
        "team_name": team.name,
        "stage": submission.stage,
        "file_url": submission.file_url,
        "submitted_at": submission.submitted_at,
        "members": [
            {
                "id": member.id,
                "name": member.name,
                "email": member.email
            }
            for member in team.members
        ]
    }

@router.post("/submissions/{submission_id}/score")
async def score_submission(
    submission_id: int,
    score: float,
    comments: str = None,
    user_id: int = None,  # From JWT token
    db: Session = Depends(get_db)
):
    """
    Supervisor scores a submission (0-10)
    """
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Validate score
    if score < 0 or score > 10:
        raise HTTPException(status_code=400, detail="Score must be between 0 and 10")
    
    # Create feedback
    feedback = SubmissionFeedback(
        submission_id=submission_id,
        supervisor_id=user_id,
        supervisor_score=score,
        comments=comments
    )
    
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    
    # Send notification to team leader
    team = submission.team
    leader = db.query(User).filter(User.id == team.leader_id).first()
    
    EmailService.send_submission_feedback_email(
        leader.email,
        team.name,
        submission.stage,
        score,
        comments
    )
    
    return {
        "status": "success",
        "message": "Score recorded",
        "feedback_id": feedback.id,
        "score": score
    }

@router.get("/stats")
async def get_supervisor_stats(
    user_id: int,  # From JWT token
    db: Session = Depends(get_db)
):
    """
    Get supervisor statistics
    """
    from sqlalchemy import func
    
    # Get stats for this supervisor
    feedback_count = db.query(func.count(SubmissionFeedback.id)).filter(
        SubmissionFeedback.supervisor_id == user_id
    ).scalar()
    
    avg_score = db.query(func.avg(SubmissionFeedback.supervisor_score)).filter(
        SubmissionFeedback.supervisor_id == user_id
    ).scalar() or 0
    
    return {
        "supervisor_id": user_id,
        "total_submissions_reviewed": feedback_count,
        "average_score_given": round(avg_score, 2)
    }
