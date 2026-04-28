"""CSV Upload routes."""
import os
from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from werkzeug.utils import secure_filename
from app.routes.auth import login_required
from app.models import get_db_connection
from app.services.csv_parser import parse_csv
from app.services.classifier import classify_students
from datetime import datetime

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route('', methods=['GET', 'POST'])
@login_required
def upload_csv():
    """Handle CSV file upload and exam creation."""
    if request.method == 'POST':
        # Check if file is present
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('upload.upload_csv'))

        file = request.files['file']

        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('upload.upload_csv'))

        if not allowed_file(file.filename):
            flash('Invalid file type. Allowed: CSV, XLSX', 'error')
            return redirect(url_for('upload.upload_csv'))

        try:
            # Get form data
            exam_name = request.form.get('exam_name', '').strip()
            course_name = request.form.get('course_name', '').strip()
            pass_threshold = float(request.form.get('pass_threshold', 40))
            fail_threshold = float(request.form.get('fail_threshold', 40))
            distinction_threshold = float(request.form.get('distinction_threshold', 70))

            if not exam_name or not course_name:
                flash('Exam name and course name are required', 'error')
                return redirect(url_for('upload.upload_csv'))

            if not (0 <= pass_threshold <= 100 and 0 <= distinction_threshold <= 100):
                flash('Thresholds must be between 0 and 100', 'error')
                return redirect(url_for('upload.upload_csv'))

            # Save file temporarily
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}")
            file.save(filepath)

            # Parse CSV
            students = parse_csv(filepath)

            # Classify students
            classified = classify_students(students, pass_threshold, fail_threshold, distinction_threshold)

            # Create exam record in database
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO exams (name, course, created_by, pass_threshold, fail_threshold, distinction_threshold, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (exam_name, course_name, session['user_id'], pass_threshold, fail_threshold, distinction_threshold, datetime.now()))

            exam_id = cursor.lastrowid
            conn.commit()

            # Insert students and classifications
            for student in classified:
                cursor.execute('''
                    INSERT INTO students (exam_id, student_id, name, marks)
                    VALUES (?, ?, ?, ?)
                ''', (exam_id, student['Student Id'], student['Name'], student['Marks']))

                student_db_id = cursor.lastrowid

                cursor.execute('''
                    INSERT INTO classifications (student_id, exam_id, status)
                    VALUES (?, ?, ?)
                ''', (student_db_id, exam_id, student['Status']))

            conn.commit()
            conn.close()

            # Clean up uploaded file
            os.remove(filepath)

            flash(f'Successfully uploaded {len(classified)} students for {exam_name}', 'success')
            return redirect(url_for('results.results', exam_id=exam_id))

        except ValueError as e:
            flash(f'Error parsing file: {str(e)}', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

        return redirect(url_for('upload.upload_csv'))

    return render_template('upload.html')
