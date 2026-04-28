"""Authentication routes."""
from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from werkzeug.security import check_password_hash
from app.models import get_db_connection

auth_bp = Blueprint('auth', __name__, url_prefix='')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Username and password are required', 'error')
            return redirect(url_for('auth.login'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, role, password_hash FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session.clear()
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[2]
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """User logout route."""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))


def login_required(f):
    """Decorator to require login."""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)

    return decorated_function
