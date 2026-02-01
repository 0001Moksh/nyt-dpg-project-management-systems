from sqlalchemy.orm import Session
from app.models.models import User, OTPToken, RoleEnum
from app.core.security import JWTHandler, OTPHandler, PasswordHandler
from app.core.config import settings
from datetime import datetime, timedelta, timezone
from typing import Optional

class AuthService:
    """Authentication business logic"""
    
    @staticmethod
    def generate_and_store_otp(email: str, db: Session) -> str:
        """Generate OTP and store with expiry"""
        otp = OTPHandler.generate_otp()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        
        # Delete previous unused OTPs
        db.query(OTPToken).filter(
            OTPToken.email == email,
            OTPToken.is_used == False
        ).delete()
        
        otp_token = OTPToken(email=email, otp=otp, expires_at=expires_at)
        db.add(otp_token)
        db.commit()
        
        return otp
    
    @staticmethod
    def verify_otp(email: str, otp: str, db: Session) -> bool:
        """Verify OTP and check expiry"""
        otp_token = db.query(OTPToken).filter(
            OTPToken.email == email,
            OTPToken.otp == otp,
            OTPToken.is_used == False,
            OTPToken.expires_at > datetime.now(timezone.utc)
        ).first()
        
        if otp_token:
            otp_token.is_used = True
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_or_create_user(email: str, name: str, db: Session) -> User:
        """Get existing user or create student user"""
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            user = User(
                email=email,
                name=name,
                role=RoleEnum.STUDENT
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        return user
    
    @staticmethod
    def verify_admin_password(email: str, password: str, db: Session) -> Optional[User]:
        """Verify admin login"""
        user = db.query(User).filter(
            User.email == email,
            User.role == RoleEnum.ADMIN
        ).first()
        
        if user and user.password_hash:
            if PasswordHandler.verify_password(password, user.password_hash):
                return user
        
        return None
    
    @staticmethod
    def create_access_token(user_id: int, email: str, role: str) -> str:
        """Create JWT token"""
        return JWTHandler.create_access_token({
            "user_id": user_id,
            "email": email,
            "role": role
        })

class UserService:
    """User business logic"""
    
    @staticmethod
    def get_user_by_id(user_id: int, db: Session) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(email: str, db: Session) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def create_supervisor(email: str, name: str, department: str, teacher_id: str, db: Session) -> User:
        """Create supervisor user"""
        user = User(
            email=email,
            name=name,
            role=RoleEnum.SUPERVISOR,
            department_supervisor=department,
            teacher_id=teacher_id
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_all_supervisors(db: Session) -> list:
        """Get all supervisors"""
        return db.query(User).filter(User.role == RoleEnum.SUPERVISOR).all()
    
    @staticmethod
    def get_all_students(db: Session) -> list:
        """Get all students"""
        return db.query(User).filter(User.role == RoleEnum.STUDENT).all()
    
    @staticmethod
    def update_user(user_id: int, **kwargs) -> User:
        """Update user fields"""
        # This will be called within a session context
        pass
