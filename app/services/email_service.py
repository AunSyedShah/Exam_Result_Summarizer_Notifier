"""Email notification service."""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from app.models import get_db_connection


class EmailService:
    """Service for sending email notifications."""

    def __init__(self):
        """Initialize email configuration."""
        self.sender_email = os.getenv('EMAIL_ADDRESS', '')
        self.sender_password = os.getenv('EMAIL_PASSWORD', '')
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))

    def send_email(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        is_html: bool = True
    ) -> bool:
        """
        Send email via SMTP.
        
        Args:
            recipient_email: Recipient email address
            subject: Email subject
            body: Email body
            is_html: Whether body is HTML
            
        Returns:
            True if successful, False otherwise
        """
        if not self.sender_email or not self.sender_password:
            print(f"[MOCK EMAIL] To: {recipient_email}\nSubject: {subject}\n\n{body[:200]}...")
            return True

        try:
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = recipient_email

            if is_html:
                part = MIMEText(body, 'html')
            else:
                part = MIMEText(body, 'plain')

            message.attach(part)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            print(f"[✅ EMAIL SENT] To: {recipient_email} | Subject: {subject}")
            return True

        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def send_notification_email(
        self,
        recipient_email: str,
        student_name: str,
        marks: float,
        category: str,
        feedback: str,
        course_name: str,
        max_marks: float = 100
    ) -> bool:
        """
        Send personalized notification email to student.
        
        Args:
            recipient_email: Student's email
            student_name: Student name
            marks: Marks obtained
            category: Pass/Fail/Distinction
            feedback: Personalized feedback message
            course_name: Course/exam name
            max_marks: Total marks
            
        Returns:
            True if successful
        """
        percentage = (marks / max_marks) * 100

        category_color = {
            'Distinction': '#28a745',
            'Pass': '#17a2b8',
            'Fail': '#dc3545',
        }

        color = category_color.get(category, '#6c757d')

        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; background: #f9f9f9; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #333;">Exam Result Notification</h2>
                    
                    <p>Dear <strong>{student_name}</strong>,</p>
                    
                    <p>Your results for <strong>{course_name}</strong> are now available.</p>
                    
                    <div style="background: white; padding: 20px; border-left: 4px solid {color}; margin: 20px 0; border-radius: 4px;">
                        <p><strong>Marks Obtained:</strong> {marks}/{max_marks} ({percentage:.1f}%)</p>
                        <p><strong>Status:</strong> <span style="color: {color}; font-weight: bold;">{category}</span></p>
                    </div>
                    
                    <div style="background: #f0f8ff; padding: 15px; border-radius: 4px; margin: 20px 0;">
                        <h4 style="color: #333; margin-top: 0;">Feedback:</h4>
                        <p>{feedback}</p>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <p style="color: #666; font-size: 12px;">
                        If you have any questions, please contact your instructor.<br>
                        <strong>Exam Result Summarizer System</strong>
                    </p>
                </div>
            </body>
        </html>
        """

        return self.send_email(
            recipient_email,
            f"Exam Result: {course_name}",
            html_body,
            is_html=True
        )

    def log_notification(
        self,
        student_id: int,
        exam_id: int,
        recipient_email: str,
        subject: str,
        message_body: str,
        status: str = 'sent'
    ) -> int:
        """
        Log notification in database.
        
        Args:
            student_id: Student ID
            exam_id: Exam ID
            recipient_email: Email address
            subject: Email subject
            message_body: Email body
            status: sent/failed/pending
            
        Returns:
            Notification ID
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO notifications (student_id, exam_id, recipient_email, subject, message_body, status, sent_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (student_id, exam_id, recipient_email, subject, message_body, status, datetime.now()))

        conn.commit()
        notification_id = cursor.lastrowid
        conn.close()

        return notification_id


# Global instance
_email_service = None


def get_email_service() -> EmailService:
    """Get or create email service instance."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service
