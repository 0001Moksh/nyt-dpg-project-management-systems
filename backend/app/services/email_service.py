import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from app.core.config import settings
import asyncio
from typing import List

class EmailService:
    """Email handling service"""
    
    @staticmethod
    def send_otp_email(email: str, otp: str) -> bool:
        """Send OTP email"""
        try:
            subject = f"Your {settings.APP_NAME} OTP"
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>DPG Project Management System</h2>
                    <p>Your One-Time Password (OTP) is:</p>
                    <h3 style="color: #007bff; font-size: 24px; letter-spacing: 5px;">{otp}</h3>
                    <p>This OTP will expire in {settings.OTP_EXPIRY_MINUTES} minutes.</p>
                    <p>If you didn't request this OTP, please ignore this email.</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">
                        © {settings.COLLEGE_NAME if hasattr(settings, 'COLLEGE_NAME') else 'DPG ITM'}. All rights reserved.
                    </p>
                </body>
            </html>
            """
            EmailService._send_email(email, subject, body)
            return True
        except Exception as e:
            print(f"Error sending OTP email: {e}")
            return False
    
    @staticmethod
    def send_team_invitation_email(email: str, team_name: str, leader_name: str, accept_link: str) -> bool:
        """Send team invitation email"""
        try:
            subject = f"Team Invitation: {team_name}"
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Team Invitation</h2>
                    <p>Hi,</p>
                    <p><strong>{leader_name}</strong> has invited you to join the team <strong>{team_name}</strong>.</p>
                    <p>
                        <a href="{accept_link}" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                            View Invitation
                        </a>
                    </p>
                    <p>If you didn't expect this invitation, please ignore this email.</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">© DPG Project Management System</p>
                </body>
            </html>
            """
            EmailService._send_email(email, subject, body)
            return True
        except Exception as e:
            print(f"Error sending team invitation email: {e}")
            return False
    
    @staticmethod
    def send_submission_feedback_email(
        email: str,
        team_name: str,
        stage: str,
        supervisor_score: float = None,
        comments: str = None
    ) -> bool:
        """Send submission feedback email"""
        try:
            subject = f"Feedback on {stage} Submission"
            
            score_html = f"<p><strong>Score:</strong> {supervisor_score}/10</p>" if supervisor_score else ""
            comments_html = f"<p><strong>Feedback:</strong><br>{comments}</p>" if comments else ""
            
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Submission Feedback</h2>
                    <p>Hi,</p>
                    <p>Your team <strong>{team_name}</strong> has received feedback on the <strong>{stage}</strong> submission.</p>
                    {score_html}
                    {comments_html}
                    <hr>
                    <p style="color: #666; font-size: 12px;">© DPG Project Management System</p>
                </body>
            </html>
            """
            EmailService._send_email(email, subject, body)
            return True
        except Exception as e:
            print(f"Error sending feedback email: {e}")
            return False
    
    @staticmethod
    def send_deadline_reminder_email(email: str, project_title: str, deadline: str) -> bool:
        """Send deadline reminder email"""
        try:
            subject = f"Deadline Reminder: {project_title}"
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Deadline Reminder</h2>
                    <p>Hi,</p>
                    <p>This is a reminder that the deadline for <strong>{project_title}</strong> is approaching.</p>
                    <p><strong>Deadline:</strong> {deadline}</p>
                    <p>Please submit your work before the deadline.</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">© DPG Project Management System</p>
                </body>
            </html>
            """
            EmailService._send_email(email, subject, body)
            return True
        except Exception as e:
            print(f"Error sending deadline reminder: {e}")
            return False
    
    @staticmethod
    def send_supervisor_request_email(email: str, admin_name: str, status: str) -> bool:
        """Send supervisor request approval/rejection email"""
        try:
            if status == "approved":
                subject = "Supervisor Access Approved"
                message = "Your request to become a supervisor has been approved."
                body_message = f"<p style='color: #28a745;'>{message}</p>"
            else:
                subject = "Supervisor Access Request Rejected"
                message = "Your request to become a supervisor has been rejected."
                body_message = f"<p style='color: #dc3545;'>{message}</p>"
            
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Request Status Update</h2>
                    <p>Hi,</p>
                    {body_message}
                    <p>If you have any questions, please contact the administration.</p>
                    <hr>
                    <p style="color: #666; font-size: 12px;">© DPG Project Management System</p>
                </body>
            </html>
            """
            EmailService._send_email(email, subject, body)
            return True
        except Exception as e:
            print(f"Error sending supervisor request email: {e}")
            return False
    
    @staticmethod
    def _send_email(to_email: str, subject: str, body: str) -> None:
        """Internal method to send email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = settings.SMTP_FROM_EMAIL
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Attach HTML body
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email to {to_email}: {e}")
            raise

class NotificationService:
    """In-app notification service"""
    
    @staticmethod
    def create_notification(user_id: int, title: str, message: str, notification_type: str, db) -> None:
        """Create in-app notification"""
        from app.models.models import Notification
        
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type
        )
        db.add(notification)
        db.commit()
    
    @staticmethod
    def get_user_notifications(user_id: int, db, unread_only: bool = False):
        """Get user notifications"""
        from app.models.models import Notification
        
        query = db.query(Notification).filter(Notification.user_id == user_id)
        
        if unread_only:
            query = query.filter(Notification.is_read == False)
        
        return query.order_by(Notification.created_at.desc()).all()
    
    @staticmethod
    def mark_notification_as_read(notification_id: int, db):
        """Mark notification as read"""
        from app.models.models import Notification
        
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if notification:
            notification.is_read = True
            db.commit()
