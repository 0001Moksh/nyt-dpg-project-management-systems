from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User, SupervisorRequest, AdminLog
from app.schemas.schemas import SupervisorRequestCreate, SupervisorRequestResponse, SupervisorRequestApproveRequest
from app.services.auth_service import AuthService, UserService
from app.services.email_service import EmailService
from typing import List
import json

router = APIRouter(prefix="/api/admin", tags=["admin"])

def get_current_user(db: Session = Depends(get_db)) -> User:
    """
    Get current user from request (simplified - implement proper JWT verification)
    This is a placeholder - implement proper JWT extraction from headers
    """
    # TODO: Extract from Authorization header
    pass

@router.get("/requests", response_model=List[SupervisorRequestResponse])
async def get_supervisor_requests(db: Session = Depends(get_db)):
    """
    Get all pending supervisor access requests
    """
    requests = db.query(SupervisorRequest).filter(
        SupervisorRequest.status == "pending"
    ).all()
    return requests

@router.post("/requests/{request_id}/approve")
async def approve_supervisor_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Admin approves supervisor request
    """
    supervisor_request = db.query(SupervisorRequest).filter(
        SupervisorRequest.id == request_id
    ).first()
    
    if not supervisor_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if supervisor_request.status != "pending":
        raise HTTPException(status_code=400, detail="Request already processed")
    
    # Create supervisor user
    supervisor = UserService.create_supervisor(
        email=supervisor_request.email,
        name=supervisor_request.name,
        department=supervisor_request.department,
        teacher_id=supervisor_request.teacher_id,
        db=db
    )
    
    # Update request status
    supervisor_request.status = "approved"
    supervisor_request.approved_by = current_user.id if current_user else None
    
    # Log admin action
    log = AdminLog(
        admin_id=current_user.id if current_user else None,
        action="approve_supervisor_request",
        resource_type="supervisor_request",
        resource_id=request_id,
        details={"supervisor_id": supervisor.id, "email": supervisor.email}
    )
    db.add(log)
    
    db.commit()
    
    # Send approval email
    EmailService.send_supervisor_request_email(supervisor_request.email, "Admin", "approved")
    
    return {
        "status": "success",
        "message": "Supervisor request approved",
        "supervisor_id": supervisor.id
    }

@router.post("/requests/{request_id}/reject")
async def reject_supervisor_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Admin rejects supervisor request
    """
    supervisor_request = db.query(SupervisorRequest).filter(
        SupervisorRequest.id == request_id
    ).first()
    
    if not supervisor_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    if supervisor_request.status != "pending":
        raise HTTPException(status_code=400, detail="Request already processed")
    
    # Update request status
    supervisor_request.status = "rejected"
    
    # Log admin action
    log = AdminLog(
        admin_id=current_user.id if current_user else None,
        action="reject_supervisor_request",
        resource_type="supervisor_request",
        resource_id=request_id,
        details={"email": supervisor_request.email, "reason": "Admin rejection"}
    )
    db.add(log)
    
    db.commit()
    
    # Send rejection email
    EmailService.send_supervisor_request_email(supervisor_request.email, "Admin", "rejected")
    
    return {
        "status": "success",
        "message": "Supervisor request rejected"
    }

@router.get("/logs")
async def get_admin_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get admin action logs for audit trail
    """
    logs = db.query(AdminLog).order_by(AdminLog.created_at.desc()).offset(skip).limit(limit).all()
    return logs

@router.get("/stats")
async def get_admin_stats(db: Session = Depends(get_db)):
    """
    Get admin dashboard statistics
    """
    from sqlalchemy import func
    
    total_users = db.query(func.count(User.id)).scalar()
    total_supervisors = db.query(func.count(User.id)).filter(User.role == "supervisor").scalar()
    total_students = db.query(func.count(User.id)).filter(User.role == "student").scalar()
    pending_requests = db.query(func.count(SupervisorRequest.id)).filter(
        SupervisorRequest.status == "pending"
    ).scalar()
    
    return {
        "total_users": total_users,
        "total_supervisors": total_supervisors,
        "total_students": total_students,
        "pending_requests": pending_requests
    }
