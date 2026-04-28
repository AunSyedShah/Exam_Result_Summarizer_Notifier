"""Results viewing routes."""
from flask import Blueprint, render_template, request, jsonify
from app.routes.auth import login_required
from app.models import get_db_connection

results_bp = Blueprint('results', __name__, url_prefix='/results')


@results_bp.route('/<int:exam_id>')
@login_required
def results(exam_id):
    """Display exam results."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get exam info
    cursor.execute('SELECT name, course FROM exams WHERE id = ?', (exam_id,))
    exam = cursor.fetchone()

    if not exam:
        conn.close()
        return render_template('404.html', message='Exam not found'), 404

    # Get students and classifications
    cursor.execute('''
        SELECT s.id, s.student_id, s.name, s.marks, c.status, c.feedback
        FROM students s
        JOIN classifications c ON s.id = c.student_id
        WHERE s.exam_id = ?
        ORDER BY s.marks DESC
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
        })

    return render_template(
        'results.html',
        exam_id=exam_id,
        exam_name=exam[0],
        course_name=exam[1],
        students=student_list
    )


@results_bp.route('/api/<int:exam_id>')
@login_required
def get_results_json(exam_id):
    """Get exam results as JSON."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT s.student_id, s.name, s.marks, c.status, c.feedback
        FROM students s
        JOIN classifications c ON s.id = c.student_id
        WHERE s.exam_id = ?
        ORDER BY s.marks DESC
    ''', (exam_id,))

    students = cursor.fetchall()
    conn.close()

    return jsonify({
        'students': [
            {
                'student_id': s[0],
                'name': s[1],
                'marks': s[2],
                'status': s[3],
                'feedback': s[4],
            } for s in students
        ]
    })
