from flask import Blueprint, render_template, session, redirect, url_for, flash

from flask_login import login_required, current_user
from app.decorators import admin_required  

admin_bp = Blueprint('admin_bp', __name__)


# Con decorador Personalizado

#admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/dashboard')
@login_required
@admin_required

def dashboard():
    return render_template('admin/dashboard.html')





#============================================


@admin_bp.route('/manage_users')
def manage_users():
    # mostrar administración de usuarios
    return render_template('admin/manage_users.html')


#---------------------------
@admin_bp.route('/admin/manage_courses')
def manage_courses():
    # Filtrar los cursos que están en estado 'borrador' o 'publicado'
    cursos_pendientes = Curso.query.filter(Curso.status.in_(['borrador', 'publicado'])).all()
    return render_template('admin/manage_courses.html', cursos=cursos_pendientes)



#---------------------------
@admin_bp.route('/courses')
@login_required
def view_courses():
    # Filtrar los cursos que están aprobados
    courses = Course.query.filter_by(status='aprobado').all()
    return render_template('app/templates/user/courses.html', courses=courses, user=current_user)


# ------- Envio de Correo A Tutor DE CURSO APROBADO !!! ---------
import smtplib
import ssl
from flask import current_app

def send_approval_email(tutor_email, course_title):
    sender_email = current_app.config['MAIL_USERNAME']
    sender_password = current_app.config['MAIL_PASSWORD']
    
    # Configuración del servidor SMTP de Gmail
    smtp_server = current_app.config['MAIL_SERVER']
    smtp_port = current_app.config['MAIL_PORT']
    
    subject = "Tu curso ha sido aprobado"
    body = f"¡Felicidades! Tu curso '{course_title}' ha sido aprobado y ya está disponible para los estudiantes."

    message = f"Subject: {subject}\n\n{body}"

    # Crear una conexión segura con el servidor SMTP
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)  # Usamos TLS para la conexión segura
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, tutor_email, message)
        print(f"Correo de aprobación enviado a {tutor_email} con éxito.")
    except Exception as e:
        print(f"Error al enviar correo: {e}")


#==============================================


#--------------- REPORTES ---------------

@admin_bp.route('/reports')
def reports():
    # mostrar reportes y estadísticas
    return render_template('admin/reports.html')

