"""Summary statistics service."""
from app.models import get_db_connection
from typing import Dict, Any, List
import statistics


def get_exam_summary(exam_id: int) -> Dict[str, Any]:
    """Get summary statistics for an exam."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all students for the exam
    cursor.execute('''
        SELECT s.marks, c.status
        FROM students s
        JOIN classifications c ON s.id = c.student_id
        WHERE s.exam_id = ?
    ''', (exam_id,))
    
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {
            'total_students': 0,
            'pass_count': 0,
            'fail_count': 0,
            'distinction_count': 0,
            'pass_rate': 0,
            'avg_marks': 0,
            'top_scorer_name': 'N/A',
            'top_scorer_marks': 0,
            'median_marks': 0,
        }

    marks = [row[0] for row in rows]
    statuses = [row[1] for row in rows]
    
    total = len(rows)
    distinction_count = statuses.count('Distinction')
    pass_count = statuses.count('Pass')
    fail_count = statuses.count('Fail')
    
    avg_marks = sum(marks) / len(marks) if marks else 0
    median_marks = statistics.median(marks) if marks else 0
    pass_rate = ((distinction_count + pass_count) / total * 100) if total > 0 else 0

    # Get top scorer
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.name, s.marks
        FROM students s
        WHERE s.exam_id = ?
        ORDER BY s.marks DESC
        LIMIT 1
    ''', (exam_id,))
    
    top_row = cursor.fetchone()
    conn.close()

    top_scorer_name = top_row[0] if top_row else 'N/A'
    top_scorer_marks = top_row[1] if top_row else 0

    return {
        'total_students': total,
        'pass_count': pass_count,
        'fail_count': fail_count,
        'distinction_count': distinction_count,
        'pass_rate': round(pass_rate, 2),
        'avg_marks': round(avg_marks, 2),
        'median_marks': round(median_marks, 2),
        'top_scorer_name': top_scorer_name,
        'top_scorer_marks': round(top_scorer_marks, 2),
    }


def get_class_distribution(exam_id: int) -> Dict[str, int]:
    """Get distribution of Pass/Fail/Distinction for an exam."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT c.status, COUNT(*) as count
        FROM classifications c
        WHERE c.exam_id = ?
        GROUP BY c.status
    ''', (exam_id,))

    rows = cursor.fetchall()
    conn.close()

    distribution = {
        'Distinction': 0,
        'Pass': 0,
        'Fail': 0,
    }

    for row in rows:
        status, count = row
        distribution[status] = count

    return distribution


def get_marks_distribution(exam_id: int) -> Dict[str, List[float]]:
    """Get marks for each category for charting."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT c.status, s.marks
        FROM students s
        JOIN classifications c ON s.id = c.student_id
        WHERE s.exam_id = ?
        ORDER BY c.status, s.marks
    ''', (exam_id,))

    rows = cursor.fetchall()
    conn.close()

    distribution = {
        'Distinction': [],
        'Pass': [],
        'Fail': [],
    }

    for row in rows:
        status, marks = row
        distribution[status].append(marks)

    # Calculate averages
    avg_marks = {}
    for status, marks_list in distribution.items():
        if marks_list:
            avg_marks[status] = round(sum(marks_list) / len(marks_list), 2)
        else:
            avg_marks[status] = 0

    return avg_marks, distribution
