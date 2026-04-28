"""Feedback generation routes."""
from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
from app.routes.auth import login_required
from app.models import get_db_connection
from app.services.llm_service import get_llm_service
from datetime import datetime

feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')


@feedback_bp.route('/<int:exam_id>')
@login_required
def feedback(exam_id):
    """Display feedback generation interface."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT name, course FROM exams WHERE id = ?', (exam_id,))
    exam = cursor.fetchone()

    if not exam:
        conn.close()
        return render_template('404.html', message='Exam not found'), 404

    # Get students without feedback
    cursor.execute('''
        SELECT s.id, s.student_id, s.name, s.marks, c.status, c.feedback
        FROM students s
        JOIN classifications c ON s.id = c.student_id
        WHERE s.exam_id = ?
        ORDER BY c.status DESC, s.marks DESC
    ''', (exam_id,))

    students = cursor.fetchall()
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
            'has_feedback': bool(s[5]),
        })

    return render_template(
        'feedback.html',
        exam_id=exam_id,
        exam_name=exam[0],
        course_name=exam[1],
        students=student_list
    )


@feedback_bp.route('/api/<int:exam_id>/generate', methods=['POST'])
@login_required
def generate_feedback(exam_id):
    """Generate feedback for all students in exam."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT course FROM exams WHERE id = ?', (exam_id,))
    exam = cursor.fetchone()

    if not exam:
        conn.close()
        return jsonify({'error': 'Exam not found'}), 404

    course_name = exam[0]

    # Get all students
    cursor.execute('''
        SELECT s.id, s.name, s.marks, c.status
        FROM students s
        JOIN classifications c ON s.id = c.student_id
        WHERE s.exam_id = ?
    ''', (exam_id,))

    students = cursor.fetchall()

    llm_service = get_llm_service()
    generated_count = 0

    for student in students:
        student_id, name, marks, status = student

        # Generate feedback
        feedback = llm_service.generate_feedback(name, marks, status, course_name)

        # Update database
        cursor.execute('''
            UPDATE classifications
            SET feedback = ?
            WHERE student_id = ? AND exam_id = ?
        ''', (feedback, student_id, exam_id))

        generated_count += 1

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'generated': generated_count,
        'message': f'Generated feedback for {generated_count} students'
    })


@feedback_bp.route('/api/<int:exam_id>/student/<int:student_id>/feedback', methods=['GET', 'POST'])
@login_required
def student_feedback(exam_id, student_id):
    """Get or update feedback for a specific student."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        data = request.get_json()
        feedback = data.get('feedback', '').strip()

        cursor.execute('''
            UPDATE classifications
            SET feedback = ?
            WHERE student_id = ? AND exam_id = ?
        ''', (feedback, student_id, exam_id))

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'feedback': feedback})

    else:
        cursor.execute('''
            SELECT c.feedback, s.name, s.marks
            FROM classifications c
            JOIN students s ON c.student_id = s.id
            WHERE c.student_id = ? AND c.exam_id = ?
        ''', (student_id, exam_id))

        result = cursor.fetchone()
        conn.close()

        if result:
            return jsonify({
                'feedback': result[0] or '',
                'name': result[1],
                'marks': result[2]
            })
        else:
            return jsonify({'error': 'Student not found'}), 404
