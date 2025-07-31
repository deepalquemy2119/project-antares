from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or (current_user.role or '').strip().lower() != 'admin':
            
            # Para guardar registros de los intentos de ingreso
            logger.warning("Intento de acceso no autorizado a ruta admin")
            flash("Acceso denegado: se requieren permisos de administrador.", "error")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function