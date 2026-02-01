from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import (
    Team, TeamInvitation, User, Submission,
    SubmissionApproval, ApprovalStatusEnum, TeamStatusEnum
)
from app.schemas.schemas import (
    TeamCreate, TeamResponse, TeamDetailResponse,
    TeamInviteRequest, TeamInvitationApproveRequest
)
from app.services.email_service import EmailService

router = APIRouter(prefix="/api/teams", tags=["teams"])

@router.post("/", response_model=TeamResponse)
async def create_team(
    team: TeamCreate,
    user_id: int,  # From JWT token
    db: Session = Depends(get_db)
):
    """
    Student creates a new team for a project
    """
    # Verify project exists
    from app.models.models import Project
    project = db.query(Project).filter(Project.id == team.project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Create team with student as leader
    new_team = Team(
        project_id=team.project_id,
        leader_id=user_id,
        name=team.name,
        status=TeamStatusEnum.PENDING
    )
    
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    
    # Add leader to members
    leader = db.query(User).filter(User.id == user_id).first()
    new_team.members.append(leader)
    db.commit()
    
    return new_team

@router.get("/{team_id}", response_model=TeamDetailResponse)
async def get_team(team_id: int, db: Session = Depends(get_db)):
    """
    Get team details with members and invitations
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    return team

@router.post("/{team_id}/invite")
async def invite_member(
    team_id: int,
    invite_request: TeamInviteRequest,
    user_id: int,  # From JWT token
    db: Session = Depends(get_db)
):
    """
    Team leader invites a member
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user is team leader
    if team.leader_id != user_id:
        raise HTTPException(status_code=403, detail="Only team leader can invite members")
    
    # Check if invitation already exists
    existing = db.query(TeamInvitation).filter(
        TeamInvitation.team_id == team_id,
        TeamInvitation.invitee_email == invite_request.invitee_email
    ).first()
    
    if existing and existing.status == ApprovalStatusEnum.PENDING:
        raise HTTPException(status_code=400, detail="Invitation already sent")
    
    # Create invitation
    invitation = TeamInvitation(
        team_id=team_id,
        invitee_email=invite_request.invitee_email,
        status=ApprovalStatusEnum.PENDING
    )
    
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    
    # Send email
    leader = db.query(User).filter(User.id == user_id).first()
    EmailService.send_team_invitation_email(
        invite_request.invitee_email,
        team.name,
        leader.name,
        f"http://localhost:3000/teams/{team_id}/invitations/{invitation.id}"
    )
    
    return {
        "status": "success",
        "message": "Invitation sent",
        "invitation_id": invitation.id
    }

@router.post("/{team_id}/invitations/{invitation_id}/respond")
async def respond_to_invitation(
    team_id: int,
    invitation_id: int,
    approve: bool,
    user_id: int,  # From JWT token
    db: Session = Depends(get_db)
):
    """
    Team member accepts or rejects invitation
    """
    invitation = db.query(TeamInvitation).filter(
        TeamInvitation.id == invitation_id,
        TeamInvitation.team_id == team_id
    ).first()
    
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    # Get user by email
    user = db.query(User).filter(User.email == invitation.invitee_email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if approve:
        # Add user to team
        if user not in team.members:
            team.members.append(user)
        invitation.status = ApprovalStatusEnum.APPROVED
    else:
        invitation.status = ApprovalStatusEnum.REJECTED
    
    # Check if all members have approved
    all_invitations = db.query(TeamInvitation).filter(
        TeamInvitation.team_id == team_id
    ).all()
    
    all_approved = all(inv.status == ApprovalStatusEnum.APPROVED for inv in all_invitations)
    
    if all_approved and len(team.members) > 1:
        team.status = TeamStatusEnum.ACTIVE
    
    db.commit()
    
    return {
        "status": "success",
        "message": "Response recorded",
        "team_status": team.status
    }

@router.post("/{team_id}/lock")
async def lock_team(
    team_id: int,
    user_id: int,  # From JWT token
    db: Session = Depends(get_db)
):
    """
    Team leader locks the team for submission
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    if team.leader_id != user_id:
        raise HTTPException(status_code=403, detail="Only team leader can lock the team")
    
    if team.status != TeamStatusEnum.ACTIVE:
        raise HTTPException(status_code=400, detail="Team must be ACTIVE to lock")
    
    team.is_locked = True
    team.status = TeamStatusEnum.LOCKED
    db.commit()
    
    return {
        "status": "success",
        "message": "Team locked for submission"
    }

@router.get("/{team_id}/members")
async def get_team_members(team_id: int, db: Session = Depends(get_db)):
    """
    Get all team members
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    return {
        "team_id": team_id,
        "members": [
            {
                "id": member.id,
                "name": member.name,
                "email": member.email,
                "role": member.role
            }
            for member in team.members
        ]
    }
