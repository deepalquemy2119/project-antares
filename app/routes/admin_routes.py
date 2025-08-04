from flask import current_app, Blueprint, render_template, session, redirect, url_for, flash

from flask_login import login_required, current_user
from app.decorators import admin_required  
import smtplib
import ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ------- para probar boton desde el panel ADMIN-------
from app.models import User, Course, Payment 

admin_bp = Blueprint('admin', __name__)



@admin_bp.route('/dashboard')
@login_required
@admin_required

def dashboard():

    print("Usuario:", current_user.id)
    print("Rol:", repr(current_user.role))  # para ver si tiene espacios
    print("Autenticado:", current_user.is_authenticated)
    return render_template('admin/dashboard.html')





#============================================


@admin_bp.route('/manage_users')
def manage_users():
    # mostrar administración de usuarios
    return render_template('admin/manage_users.html')


#---------------------------
@admin_bp.route('/manage_courses')
@login_required
@admin_required
def manage_courses():
    # Filtrar los cursos que están en estado 'borrador' o 'publicado'
    cursos_pendientes = Course.query.filter(Course.status.in_(['borrador', 'publicado'])).all()
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




from flask_mail import Message
from app import mail

def send_payment_receipt(user, course, payment):
    try:
        msg = Message(
            subject="Confirmación de Pago - Antares",
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[user.email]
        )
        msg.html = render_template(
            'emails/payment_receipt.html',
            user=user,
            course=course,
            payment=payment
        )
        mail.send(msg)
        print(f"[✔] Correo de confirmación enviado a {user.email}")
    except Exception as e:
        print(f"[✘] Error al enviar el correo: {e}")




from app.models import Payment, User, Course

@admin_bp.route('/test/payment_email/<int:payment_id>')
@login_required
@admin_required
def test_send_payment_email(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    user = User.query.get(payment.student_id)
    course = Course.query.get(payment.course_id)

    success = send_payment_confirmation_email(user, course, payment)

    if success:
        flash(f"Correo enviado a {user.email} con éxito", "success")
    else:
        flash("Error al enviar el correo", "danger")

    return redirect(url_for('admin_bp.reports'))



def send_payment_confirmation_email(user, course, payment):
    sender_email = current_app.config['MAIL_USERNAME']
    sender_password = current_app.config['MAIL_PASSWORD']
    smtp_server = current_app.config['MAIL_SERVER']
    smtp_port = current_app.config['MAIL_PORT']

    message = MIMEMultipart("alternative")
    message["Subject"] = "Confirmación de Pago - Antares Academy"
    message["From"] = sender_email
    message["To"] = user.email

    html = render_template("emails/payments_receipt.html", user=user, course=course, payment=payment)
    message.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user.email, message.as_string())
        print(f"[✔] Correo enviado a {user.email}")
        return True
    except Exception as e:
        print(f"[✘] Error al enviar el correo: {e}")
        return False




@admin_bp.route('/admin/test_email_payment')
@login_required
@admin_required
def test_email_payment():
    # Reemplazo con IDs válidos que existan en la DDBB
    user = User.query.first()
    course = Course.query.first()
    payment = Payment.query.first()

    if not user or not course or not payment:
        flash("No hay datos de prueba disponibles.", "danger")
        return redirect(url_for('admin_bp.dashboard'))

    success = send_payment_confirmation_email(user, course, payment)
    if success:
        flash("Correo de prueba enviado correctamente.", "success")
    else:
        flash("Error al enviar el correo de prueba.", "danger")
    return redirect(url_for('admin_bp.dashboard'))
#==============================================


#--------------- REPORTES ---------------

@admin_bp.route('/reports')
def reports():
    # mostrar reportes y estadísticas
    return render_template('admin/reports.html')


#_--------------------- APROBAR CURSOS ----------------------
@admin_bp.route('/approve_course/<int:course_id>', methods=['POST'])
@login_required
@admin_required
def approve_course(course_id):
    course = Course.query.get_or_404(course_id)

    if course.status == 'aprobado':
        flash("Este curso ya está aprobado.", "info")
        return redirect(url_for('admin_bp.manage_courses'))

    try:
        course.status = 'aprobado'
        db.session.commit()

        tutor = User.query.get(course.tutor_id)
        if tutor:
            send_approval_email(tutor.email, course.title)

        flash("Curso aprobado correctamente y correo enviado al tutor.", "success")
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR APROBANDO CURSO] {e}")
        flash("Ocurrió un error al aprobar el curso.", "danger")

    return redirect(url_for('admin_bp.manage_courses'))
