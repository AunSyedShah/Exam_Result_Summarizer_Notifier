"""Flask application factory."""
import os
from flask import Flask, g
from dotenv import load_dotenv
from app.models import init_db, close_db

# Load environment variables
load_dotenv()


def create_app():
    """Create and configure Flask application."""
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

    # Initialize database
    init_db()

    # Register teardown function
    app.teardown_appcontext(close_db)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.upload import upload_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.feedback import feedback_bp
    from app.routes.notifications import notifications_bp
    from app.routes.results import results_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(results_bp)

    @app.route('/')
    def index():
        """Redirect to dashboard or login."""
        from flask import redirect, session
        if 'user_id' in session:
            return redirect('/dashboard')
        return redirect('/login')

    return app
