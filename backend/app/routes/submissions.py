from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import (
    Submission, SubmissionApproval, SubmissionFeedback, Team, User,
    ApprovalStatusEnum, SubmissionStageEnum
)
from app.schemas.schemas import (
    SubmissionUploadRequest, SubmissionResponse,
    SupervisorFeedbackRequest, AdminFeedbackRequest
)
from app.services.email_service import EmailService

router = APIRouter(prefix="/api/submissions", tags=["submissions"])

@router.post("/{team_id}/{stage}", response_model=SubmissionResponse)
async def upload_submission(
    team_id: int,
    stage: str,
    file_url: str,  # OneDrive URL
    user_id: int,  # From JWT token
    db: Session = Depends(get_db)
):
    """
    Team leader uploads submission for a stage
    Stage: synopsis, progress_1, progress_2, final_submission
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Only team leader can upload
    if team.leader_id != user_id:
        raise HTTPException(status_code=403, detail="Only team leader can upload submissions")
    
    # Validate stage
    valid_stages = [e.value for e in SubmissionStageEnum]
    if stage not in valid_stages:
        raise HTTPException(status_code=400, detail=f"Invalid stage. Must be one of {valid_stages}")
    
    # Create submission
    submission = Submission(
        team_id=team_id,
        stage=stage,
        file_url=file_url,
        uploaded_by=user_id,
        approval_status=ApprovalStatusEnum.PENDING
    )
    
    db.add(submission)
    db.commit()
    db.refresh(submission)
    
    # Create approval records for all team members (except leader)
    for member in team.members:
        if member.id != user_id:
            approval = SubmissionApproval(
                submission_id=submission.id,
                user_id=member.id,
                status=ApprovalStatusEnum.PENDING
            )
            db.add(approval)
    
    db.commit()
    
    # Send emails to members for approval
    leader = db.query(User).filter(User.id == user_id).first()
    for member in team.members:
        if member.id != user_id:
            EmailService.send_team_invitation_email(
                member.email,
                f"{team.name} - {stage} Submission",
                leader.name,
                f"http://localhost:3000/submissions/{submission.id}/approve"
            )
    
    return submission

@router.post("/{submission_id}/approve")
async def approve_submission(
    submission_id: int,
    approve: bool,
    user_id: int,  # From JWT token
    db: Session = Depends(get_db)
):
    """
    Team member approves or rejects submission
    """
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Find approval record for this user
    approval = db.query(SubmissionApproval).filter(
        SubmissionApproval.submission_id == submission_id,
        SubmissionApproval.user_id == user_id
    ).first()
    
    if not approval:
        raise HTTPException(status_code=404, detail="Approval record not found")
    
    approval.status = ApprovalStatusEnum.APPROVED if approve else ApprovalStatusEnum.REJECTED
    
    db.commit()
    
    # Check if all members have approved
    all_approvals = db.query(SubmissionApproval).filter(
        SubmissionApproval.submission_id == submission_id
    ).all()
    
    if all_approvals:
        all_approved = all(app.status == ApprovalStatusEnum.APPROVED for app in all_approvals)
        
        if all_approved:
            submission.approval_status = ApprovalStatusEnum.APPROVED
            db.commit()
            
            # Notify supervisor
            team = submission.team
            # TODO: Send notification to assigned supervisor
    else:
        # No approvals needed, mark as approved
        submission.approval_status = ApprovalStatusEnum.APPROVED
        db.commit()
    
    return {
        "status": "success",
        "message": "Approval recorded",
        "submission_approval_status": submission.approval_status
    }

@router.get("/{submission_id}", response_model=SubmissionResponse)
async def get_submission(submission_id: int, db: Session = Depends(get_db)):
    """
    Get submission details
    """
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    return submission

@router.get("/team/{team_id}")
async def get_team_submissions(team_id: int, db: Session = Depends(get_db)):
    """
    Get all submissions for a team
    """
    submissions = db.query(Submission).filter(Submission.team_id == team_id).all()
    
    return {
        "team_id": team_id,
        "submissions": [
            {
                "id": s.id,
                "stage": s.stage,
                "file_url": s.file_url,
                "approval_status": s.approval_status,
                "submitted_at": s.submitted_at
            }
            for s in submissions
        ]
    }

@router.post("/{submission_id}/supervisor-feedback")
async def add_supervisor_feedback(
    submission_id: int,
    feedback: SupervisorFeedbackRequest,
    db: Session = Depends(get_db)
):
    """
    Supervisor provides feedback and score (0-10)
    """
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Create or update feedback
    existing_feedback = db.query(SubmissionFeedback).filter(
        SubmissionFeedback.submission_id == submission_id,
        SubmissionFeedback.supervisor_id != None
    ).first()
    
    if existing_feedback:
        existing_feedback.supervisor_score = feedback.score
        existing_feedback.comments = feedback.comments
        existing_feedback.resubmission_deadline = feedback.resubmission_deadline
        db.commit()
        feedback_id = existing_feedback.id
    else:
        new_feedback = SubmissionFeedback(
            submission_id=submission_id,
            supervisor_score=feedback.score,
            comments=feedback.comments,
            resubmission_deadline=feedback.resubmission_deadline
        )
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        feedback_id = new_feedback.id
    
    # Send feedback email to team leader
    team = submission.team
    leader = db.query(User).filter(User.id == team.leader_id).first()
    
    EmailService.send_submission_feedback_email(
        leader.email,
        team.name,
        submission.stage,
        feedback.score,
        feedback.comments
    )
    
    return {
        "status": "success",
        "message": "Feedback recorded",
        "feedback_id": feedback_id
    }

@router.post("/{submission_id}/admin-feedback")
async def add_admin_feedback(
    submission_id: int,
    feedback: AdminFeedbackRequest,
    user_id: int,  # From JWT token - must be admin
    db: Session = Depends(get_db)
):
    """
    Admin provides final score (0-20)
    """
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Create or update feedback
    existing_feedback = db.query(SubmissionFeedback).filter(
        SubmissionFeedback.submission_id == submission_id,
        SubmissionFeedback.admin_id != None
    ).first()
    
    if existing_feedback:
        existing_feedback.admin_score = feedback.score
        existing_feedback.comments = feedback.comments
        db.commit()
        feedback_id = existing_feedback.id
    else:
        new_feedback = SubmissionFeedback(
            submission_id=submission_id,
            admin_id=user_id,
            admin_score=feedback.score,
            comments=feedback.comments
        )
        db.add(new_feedback)
        db.commit()
        db.refresh(new_feedback)
        feedback_id = new_feedback.id
    
    return {
        "status": "success",
        "message": "Admin feedback recorded",
        "feedback_id": feedback_id
    }

@router.get("/{submission_id}/feedback")
async def get_submission_feedback(submission_id: int, db: Session = Depends(get_db)):
    """
    Get all feedback for a submission
    """
    feedbacks = db.query(SubmissionFeedback).filter(
        SubmissionFeedback.submission_id == submission_id
    ).all()
    
    return {
        "submission_id": submission_id,
        "feedbacks": [
            {
                "id": f.id,
                "supervisor_score": f.supervisor_score,
                "admin_score": f.admin_score,
                "comments": f.comments,
                "created_at": f.created_at
            }
            for f in feedbacks
        ]
    }
