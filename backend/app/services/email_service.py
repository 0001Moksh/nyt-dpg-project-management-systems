import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from app.config import settings
from jinja2 import Template

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending emails via SMTP"""

    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL
        self.from_name = settings.SMTP_FROM_NAME

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str = None,
    ) -> bool:
        """Send email via SMTP"""
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email

            if text_content:
                part1 = MIMEText(text_content, "plain")
                msg.attach(part1)

            part2 = MIMEText(html_content, "html")
            msg.attach(part2)

            async with aiosmtplib.SMTP(hostname=self.smtp_host, port=self.smtp_port) as smtp:
                await smtp.login(self.smtp_user, self.smtp_password)
                await smtp.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    async def send_otp_email(self, to_email: str, otp: str, name: str = "User") -> bool:
        """Send OTP email"""
        subject = "Your DPG PMS Login Code"
        html_template = """
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2>Welcome to DPG Project Management System</h2>
                    <p>Hello {name},</p>
                    <p>Your One-Time Password (OTP) for login is:</p>
                    <div style="background-color: #f0f0f0; padding: 20px; text-align: center; border-radius: 5px; margin: 20px 0;">
                        <h1 style="margin: 0; font-size: 32px; color: #007bff; letter-spacing: 5px;">{otp}</h1>
                    </div>
                    <p><strong>This OTP is valid for 5 minutes only.</strong></p>
                    <p>If you didn't request this code, please ignore this email.</p>
                    <hr style="margin: 20px 0;">
                    <p style="font-size: 12px; color: #666;">
                        DPG Project Management System<br/>
                        NexyugTech Company
                    </p>
                </div>
            </body>
        </html>
        """

        text_content = f"Your OTP code is: {otp}. Valid for 5 minutes."

        html_content = html_template.format(name=name, otp=otp)
        return await self.send_email(to_email, subject, html_content, text_content)

    async def send_team_approval_email(
        self, to_email: str, team_name: str, project_name: str, approval_link: str
    ) -> bool:
        """Send team approval email to members"""
        subject = f"Team Approval Request: {team_name}"
        html_template = """
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2>Team Approval Request</h2>
                    <p>You have been added to the team <strong>{team_name}</strong> for project <strong>{project_name}</strong>.</p>
                    <p>Please review and approve to join the team:</p>
                    <div style="margin: 20px 0;">
                        <a href="{approval_link}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Review & Approve</a>
                    </div>
                    <p><strong>Note:</strong> You must approve within 24 hours to join the team.</p>
                </div>
            </body>
        </html>
        """

        html_content = html_template.format(
            team_name=team_name,
            project_name=project_name,
            approval_link=approval_link,
        )
        return await self.send_email(to_email, subject, html_content)

    async def send_submission_notification(
        self, to_email: str, team_name: str, stage: str, project_name: str
    ) -> bool:
        """Send submission notification to supervisor"""
        subject = f"New Submission: {project_name} - {stage}"
        html_template = """
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2>New Project Submission</h2>
                    <p>Team <strong>{team_name}</strong> has submitted their work for <strong>{stage}</strong> stage of project <strong>{project_name}</strong>.</p>
                    <p>Please review and score the submission in the dashboard.</p>
                    <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Team:</strong> {team_name}</p>
                        <p><strong>Project:</strong> {project_name}</p>
                        <p><strong>Stage:</strong> {stage}</p>
                    </div>
                </div>
            </body>
        </html>
        """

        html_content = html_template.format(
            team_name=team_name,
            stage=stage,
            project_name=project_name,
        )
        return await self.send_email(to_email, subject, html_content)

    async def send_supervisor_assignment_email(
        self, to_email: str, project_name: str, teams: list
    ) -> bool:
        """Send supervisor assignment notification"""
        subject = f"You have been assigned as supervisor for {project_name}"
        teams_html = "\n".join([f"<li>{team}</li>" for team in teams])

        html_template = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2>Supervisor Assignment</h2>
                    <p>You have been assigned as supervisor for the project <strong>{project_name}</strong>.</p>
                    <p><strong>Teams under your supervision:</strong></p>
                    <ul>
                        {teams_html}
                    </ul>
                    <p>Please log in to the dashboard to view and manage the submissions.</p>
                </div>
            </body>
        </html>
        """

        return await self.send_email(to_email, subject, html_template)

    async def send_review_feedback_email(
        self, to_email: str, team_name: str, stage: str, feedback: str, score: float
    ) -> bool:
        """Send review feedback to team"""
        subject = f"Review Feedback: {stage} Stage - Score: {score}/10"
        html_template = """
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2>Stage Review Feedback</h2>
                    <p>Hello {team_name} team,</p>
                    <p>Your submission for the <strong>{stage}</strong> stage has been reviewed.</p>
                    <div style="background-color: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p><strong>Score:</strong> {score}/10</p>
                        <p><strong>Feedback:</strong></p>
                        <p>{feedback}</p>
                    </div>
                    <p>Please log in to the dashboard to view more details.</p>
                </div>
            </body>
        </html>
        """

        html_content = html_template.format(
            team_name=team_name,
            stage=stage,
            feedback=feedback,
            score=score,
        )
        return await self.send_email(to_email, subject, html_content)


# Singleton instance
email_service = EmailService()
