from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.schemas import (
    LoginRequest, OTPVerifyRequest, OTPVerifyResponse,
    AdminLoginRequest
)
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from app.core.security import JWTHandler

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint - Send OTP or ask for password if admin
    """
    user = db.query(__import__('app.models.models', fromlist=['User']).User).filter(
        __import__('app.models.models', fromlist=['User']).User.email == request.email
    ).first()
    
    # If admin, return prompt for password
    if user and user.role == "admin":
        return {
            "status": "admin",
            "message": "Please provide your password",
            "email": request.email
        }
    
    # Generate and send OTP
    otp = AuthService.generate_and_store_otp(request.email, db)
    
    # Send OTP email
    if EmailService.send_otp_email(request.email, otp):
        return {
            "status": "otp_sent",
            "message": "OTP sent to your email",
            "email": request.email
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to send OTP email")

@router.post("/admin-login")
async def admin_login(request: AdminLoginRequest, db: Session = Depends(get_db)):
    """
    Admin login with password
    """
    user = AuthService.verify_admin_password(request.email, request.password, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    access_token = AuthService.create_access_token(user.id, user.email, user.role)
    
    return OTPVerifyResponse(
        access_token=access_token,
        role=user.role,
        user_id=user.id,
        name=user.name
    )

@router.post("/verify-otp", response_model=OTPVerifyResponse)
async def verify_otp(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    """
    Verify OTP and return JWT token
    """
    # Verify OTP
    if not AuthService.verify_otp(request.email, request.otp, db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP"
        )
    
    # Get or create user
    from app.models.models import User
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        # Extract name from email (before @)
        name = request.email.split("@")[0].replace(".", " ").title()
        user = AuthService.get_or_create_user(request.email, name, db)
    
    # Create JWT token
    access_token = AuthService.create_access_token(user.id, user.email, user.role)
    
    return OTPVerifyResponse(
        access_token=access_token,
        role=user.role,
        user_id=user.id,
        name=user.name
    )

@router.post("/verify-token")
async def verify_token(token: str):
    """
    Verify JWT token validity
    """
    payload = JWTHandler.verify_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    return {
        "valid": True,
        "payload": payload
    }
