import random
import string
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.models import User
from app.config import settings
from app.services.email_service import email_service
import logging

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for handling authentication"""

    @staticmethod
    def generate_otp(length: int = None) -> str:
        """Generate a random OTP"""
        length = length or settings.OTP_LENGTH
        return "".join(random.choices(string.digits, k=length))

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                hours=settings.JWT_EXPIRY_HOURS
            )
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return payload
        except JWTError as e:
            logger.error(f"Token verification failed: {str(e)}")
            return None

    async def request_otp(self, email: str, db: Session) -> dict:
        """Request OTP for email"""
        try:
            # Check if user exists or create new
            user = db.query(User).filter(User.email == email).first()
            if not user:
                # Create new user
                user = User(
                    id=f"user_{datetime.utcnow().timestamp()}",
                    email=email,
                    name=email.split("@")[0],
                    role="STUDENT",
                )
                db.add(user)
                db.commit()

            # Generate and save OTP
            otp = self.generate_otp()
            otp_expiry = datetime.utcnow() + timedelta(
                minutes=settings.OTP_EXPIRY_MINUTES
            )

            user.otp_code = otp
            user.otp_expiry = otp_expiry
            db.commit()

            # Send OTP email
            await email_service.send_otp_email(email, otp, user.name)

            return {"success": True, "message": "OTP sent to your email"}

        except Exception as e:
            logger.error(f"OTP request failed: {str(e)}")
            return {"success": False, "message": "Failed to request OTP"}

    async def verify_otp(self, email: str, otp: str, db: Session) -> dict:
        """Verify OTP and create session"""
        try:
            user = db.query(User).filter(User.email == email).first()

            if not user:
                return {"success": False, "message": "User not found"}

            # Check OTP validity
            if not user.otp_code or user.otp_code != otp:
                return {"success": False, "message": "Invalid OTP"}

            if user.otp_expiry < datetime.utcnow():
                return {"success": False, "message": "OTP expired"}

            # Clear OTP
            user.otp_code = None
            user.otp_expiry = None
            user.is_active = True
            db.commit()

            # Create token
            token = self.create_access_token({"sub": user.id, "email": user.email})

            return {
                "success": True,
                "token": token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "role": user.role,
                    "rollNo": user.roll_no,
                    "branch": user.branch,
                    "batch": user.batch,
                },
            }

        except Exception as e:
            logger.error(f"OTP verification failed: {str(e)}")
            return {"success": False, "message": "OTP verification failed"}

    @staticmethod
    def get_current_user(token: str, db: Session) -> User:
        """Get current user from token"""
        payload = AuthService.verify_token(token)
        if not payload:
            return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        user = db.query(User).filter(User.id == user_id).first()
        return user


# Singleton instance
auth_service = AuthService()
