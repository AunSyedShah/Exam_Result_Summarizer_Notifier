"""Dashboard routes."""
from flask import Blueprint, render_template, request, jsonify
from app.routes.auth import login_required
from app.models import get_db_connection
from app.services.summary import get_exam_summary, get_class_distribution, get_marks_distribution
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('')
@login_required
def dashboard():
    """Display dashboard with exam list."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all exams
    cursor.execute('''
        SELECT id, name, course, created_at FROM exams
        ORDER BY created_at DESC LIMIT 10
    ''')

    exams = cursor.fetchall()
    conn.close()

    exam_list = []
    for exam in exams:
        summary = get_exam_summary(exam[0])
        exam_list.append({
            'id': exam[0],
            'name': exam[1],
            'course': exam[2],
            'created_at': exam[3],
            'summary': summary
        })

    return render_template('dashboard.html', exams=exam_list)


@dashboard_bp.route('/api/exam/<int:exam_id>/stats')
@login_required
def get_exam_stats(exam_id):
    """Get exam statistics as JSON for charts."""
    summary = get_exam_summary(exam_id)
    distribution = get_class_distribution(exam_id)
    avg_marks, _ = get_marks_distribution(exam_id)

    return jsonify({
        'summary': summary,
        'distribution': distribution,
        'avg_marks': avg_marks,
    })


@dashboard_bp.route('/exam/<int:exam_id>')
@login_required
def exam_detail(exam_id):
    """Display detailed exam dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id, name, course, created_at FROM exams WHERE id = ?', (exam_id,))
    exam = cursor.fetchone()
    conn.close()

    if not exam:
        return render_template('404.html', message='Exam not found'), 404

    summary = get_exam_summary(exam_id)
    distribution = get_class_distribution(exam_id)
    avg_marks, _ = get_marks_distribution(exam_id)

    return render_template(
        'exam_detail.html',
        exam={
            'id': exam[0],
            'name': exam[1],
            'course': exam[2],
            'created_at': exam[3]
        },
        summary=summary,
        distribution=distribution,
        avg_marks=avg_marks
    )
