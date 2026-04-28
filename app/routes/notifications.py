"""Email notification routes."""
import os
from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from app.routes.auth import login_required
from app.models import get_db_connection
from app.services.email_service import get_email_service
from datetime import datetime

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')


@notifications_bp.route('/<int:exam_id>')
@login_required
def notifications(exam_id):
    """Display notifications interface."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT name, course FROM exams WHERE id = ?', (exam_id,))
    exam = cursor.fetchone()

    if not exam:
        conn.close()
        return render_template('404.html', message='Exam not found'), 404

    # Get students with feedback
    cursor.execute('''
        SELECT s.id, s.student_id, s.name, s.marks, c.status, c.feedback
        FROM students s
        JOIN classifications c ON s.id = c.student_id
        WHERE s.exam_id = ? AND c.feedback IS NOT NULL
        ORDER BY c.status DESC, s.marks DESC
    ''', (exam_id,))

    students = cursor.fetchall()

    # Get sent notifications
    cursor.execute('''
        SELECT id, recipient_email, status, sent_at
        FROM notifications
        WHERE exam_id = ?
        ORDER BY sent_at DESC LIMIT 50
    ''', (exam_id,))

    sent_notifications = cursor.fetchall()
    conn.close()

    student_list = []
    for s in students:
        student_list.append({
            'id': s[0],
            'student_id': s[1],
            'name': s[2],
            'marks': s[3],
            'status': s[4],
            'feedback': s[5],
        })

    notification_list = []
    for n in sent_notifications:
        notification_list.append({
            'id': n[0],
            'email': n[1],
            'status': n[2],
            'sent_at': n[3],
        })

    # Check if SMTP is properly configured
    smtp_configured = bool(os.getenv('EMAIL_ADDRESS') and os.getenv('EMAIL_PASSWORD'))

    return render_template(
        'notifications.html',
        exam_id=exam_id,
        exam_name=exam[0],
        course_name=exam[1],
        students=student_list,
        sent_notifications=notification_list,
        smtp_configured=smtp_configured
    )


@notifications_bp.route('/api/<int:exam_id>/send-email', methods=['POST'])
@login_required
def send_email(exam_id):
    """Send email notification to a student."""
    data = request.get_json()
    student_id = data.get('student_id')
    email = data.get('email')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT s.id, s.name, s.marks, c.status, c.feedback, e.course, e.id
        FROM students s
        JOIN classifications c ON s.id = c.student_id
        JOIN exams e ON s.exam_id = e.id
        WHERE s.id = ? AND s.exam_id = ?
    ''', (student_id, exam_id))

    result = cursor.fetchone()

    if not result:
        conn.close()
        return jsonify({'error': 'Student not found'}), 404

    student_name = result[1]
    marks = result[2]
    status = result[3]
    feedback = result[4]
    course = result[5]

    # Send email
    email_service = get_email_service()
    success = email_service.send_notification_email(
        email,
        student_name,
        marks,
        status,
        feedback,
        course
    )

    if success:
        # Log notification
        cursor.execute('''
            INSERT INTO notifications (student_id, exam_id, recipient_email, subject, message_body, status, sent_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            student_id,
            exam_id,
            email,
            f"Exam Result: {course}",
            f"Status: {status}, Marks: {marks}/100, Feedback: {feedback}",
            'sent',
            datetime.now()
        ))
        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': f'Email sent to {email}'})
    else:
        conn.close()
        return jsonify({'error': 'Failed to send email'}), 500


@notifications_bp.route('/api/<int:exam_id>/send-batch', methods=['POST'])
@login_required
def send_batch_emails(exam_id):
    """Send emails to all students in exam."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT s.id, s.student_id, s.name, s.marks, c.status, c.feedback, e.course
        FROM students s
        JOIN classifications c ON s.id = c.student_id
        JOIN exams e ON s.exam_id = e.id
        WHERE s.exam_id = ?
    ''', (exam_id,))

    students = cursor.fetchall()

    if not students:
        conn.close()
        return jsonify({'error': 'No students found'}), 404

    email_service = get_email_service()
    sent_count = 0
    failed_count = 0

    for student in students:
        student_db_id, student_id, name, marks, status, feedback, course = student

        # Create dummy email (in real scenario, this would come from a student database)
        email = f"{student_id}@students.university.edu"

        # Send email
        success = email_service.send_notification_email(
            email,
            name,
            marks,
            status,
            feedback,
            course
        )

        if success:
            # Log notification
            cursor.execute('''
                INSERT INTO notifications (student_id, exam_id, recipient_email, subject, message_body, status, sent_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                student_db_id,
                exam_id,
                email,
                f"Exam Result: {course}",
                f"Status: {status}, Marks: {marks}/100",
                'sent',
                datetime.now()
            ))
            sent_count += 1
        else:
            failed_count += 1

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'sent': sent_count,
        'failed': failed_count,
        'message': f'Sent {sent_count} emails, {failed_count} failed'
    })
