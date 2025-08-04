from functools import wraps
from flask import redirect, url_for, flash, current_app
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        role = getattr(current_user, 'role', None)
        role_str = (role or '').strip().lower()
        print(f"[admin_required] current_user.is_authenticated={current_user.is_authenticated}")
        print(f"[admin_required] current_user.role raw: {repr(role)}")
        print(f"[admin_required] current_user.role processed: '{role_str}'")

        if not current_user.is_authenticated or role_str != 'admin':
            flash("Acceso denegado: se requieren permisos de administrador.", "error")
            return redirect(url_for('public.home'))

        return f(*args, **kwargs)
    return decorated_function
