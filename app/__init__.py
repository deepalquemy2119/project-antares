from flask import Flask
from config import Config
from app.extensions import db, login_manager, mail  # <- ahora importa mail aquí
from flask_migrate import Migrate
from flask_mail import Mail



from app.routes.public_routes import public_bp
from app.routes import user_routes
from app.routes import tutor_routes
from app.routes.admin_routes import admin_bp
from app.routes.auth_routes import auth_bp
from app.routes.category_routes import category_bp
from app.models import Category

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicialización de extensiones
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registro de blueprints
    with app.app_context():
        app.register_blueprint(auth_bp)
        app.register_blueprint(user_routes.bp)
        app.register_blueprint(tutor_routes.tutor_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(public_bp)
        app.register_blueprint(category_bp)

        @app.context_processor
        def inject_categories():
            try:
                categories = Category.query.order_by(Category.name).all()
                return dict(global_categories=categories)
            except Exception:
                return dict(global_categories=[])

    return app
