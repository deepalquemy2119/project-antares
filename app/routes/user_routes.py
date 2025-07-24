from flask import Blueprint, render_template, session, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app.models import db
from sqlalchemy import text

user_bp = Blueprint('user', __name__, url_prefix='/user')


#------------------- DASHBOARD -----------------
# @user_bp.route('/dashboard')
# def dashboard():
#     if not session.get('user_id'):
#         flash("Debes iniciar sesión para ver el dashboard", "warning")
#         return redirect(url_for('auth.login'))
#     return render_template('user/dashboard.html')

#/////////////////////////////




user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'alumno':
        return "Acceso no autorizado", 403

    query = text("""
        SELECT 
            sc.course_id, 
            c.title, 
            c.description, 
            c.duration, 
            sc.payment_status,
            EXISTS (
                SELECT 1 
                FROM certificados ce 
                WHERE ce.student_id = :user_id AND ce.course_id = sc.course_id
            ) AS has_certificate
        FROM student_courses sc
        JOIN courses c ON sc.course_id = c.id
        WHERE sc.student_id = :user_id
    """)

    result = db.session.execute(query, {'user_id': current_user.id})
    courses = [dict(row) for row in result.fetchall()]

    return render_template('user/dashboard.html', courses=courses)




#-------------------- PROFILE -------------------
@user_bp.route('/profile')
@login_required
def profile():
    if session.get('user_role') != 'alumno':
        flash("Solo los alumnos pueden ver este perfil.", "danger")
        return redirect(url_for('user.dashboard'))

    user = current_user

    # 🔹 Simulación de datos (reemplazar con consulta real)
    user.courses = [
        {
            "name": "Python desde cero",
            "progress": 85,
            "certified": True,
            "payment_due": datetime(2025, 7, 28)
        },
        {
            "name": "Fundamentos de Machine Learning",
            "progress": 45,
            "certified": False,
            "payment_due": datetime(2025, 7, 25)
        }
    ]

    user.messages = [
        {"sender": "Tutor Juan", "text": "¡Buen trabajo en el módulo 2!", "date": datetime(2025, 7, 21)},
        {"sender": "Antares", "text": "Certificado disponible para descargar", "date": datetime(2025, 6, 30)}
    ]

    return render_template("user/profile.html", user=user, fecha_hoy=datetime.today())

@user_bp.route('/courses')
def courses():
    # lógica para mostrar cursos del usuario
    return render_template('user/courses.html')

@user_bp.route('/settings')
def settings():
    # configuración de usuario
    return render_template('user/settings.html')


@user.route('/materials/<int:course_id>')
@login_required
def view_materials(course_id):
    # lógica para mostrar archivos del curso
    pass

@user.route('/certificate/download/<int:course_id>')
@login_required
def download_certificate(course_id):
    # lógica para descargar PDF del certificado emitido
    pass
