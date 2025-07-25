from flask import Flask
from app.extensions import db, login_manager
from config import Config
from app.routes.public_routes import public_bp
from app.routes import user_routes
from flask_migrate import Migrate

from flask_mail import Mail

migrate = Migrate()

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mail.init_app(app)
  

# inicio extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app, db)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

# registro de blueprints
    with app.app_context():
        from app.routes.auth_routes import auth_bp
        from app.routes.user_routes import bp as user_bp
        from app.routes import user_routes
        from app.routes.course_routes import course_bp
        from app.routes.admin_routes import admin_bp
        from app.routes.tutor_routes import tutor_bp


        app.register_blueprint(tutor_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(user_bp)
        app.register_blueprint(course_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(public_bp)
        


    return app  
    
