
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from flask_mail import Message
from flask_login import login_required, current_user
from datetime import datetime
from app.models import db, Certificado, User, Course, StudentCourse, Payment, Category
from app.extensions import mail
from app.services.email_service import send_payment_receipt

from sqlalchemy import text

from sqlalchemy.sql.expression import func

bp = Blueprint('user', __name__, url_prefix='/user')

# ===========================
# DASHBOARD DEL ALUMNO
# ===========================

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'alumno':
        return "Acceso no autorizado", 403

    courses = []
    for sc in current_user.student_courses:
        has_certificate = Certificado.query.filter_by(
            student_id=current_user.id,
            course_id=sc.course_id
        ).first() is not None

        courses.append({
            "course_id": sc.course_id,
            "title": sc.course.title,
            "description": sc.course.description,
            "duration": sc.course.duration,
            "payment_status": sc.payment_status,
            "has_certificate": has_certificate,
            "progress": 0  # o el valor real si lo calculás
        })

    return render_template('user/dashboard.html', user=current_user, courses=courses)


# ===========================
# PERFIL DEL ALUMNO
# ===========================
@bp.route('/profile')
@login_required
def profile():
    if current_user.role != 'alumno':
        flash("Solo los alumnos pueden ver este perfil.", "danger")
        return redirect(url_for('user.dashboard'))

    user = current_user

    # cursos sugeridos (ejemplo: cursos que no está inscrito el alumno)
    # ejemplo, todos los cursos que NO estén en student_courses del usuario

    student_course_ids = [sc.course_id for sc in user.student_courses]
    suggested_courses = Course.query.filter(~Course.id.in_(student_course_ids)).limit(5).all()



    return render_template('user/profile.html', user=user, fecha_hoy=datetime.today(),  suggested_courses=suggested_courses)

# ===========================
# CURSOS DEL ALUMNO
# ===========================
@bp.route('/courses')
@login_required
def courses():
    # cargar cursos de la BD si queremos despues
    return render_template('user/courses.html', user=current_user)


# ===========================
# CONFIGURACIONES DEL ALUMNO
# ===========================
@bp.route('/settings')
@login_required
def settings():
    return render_template('user/settings.html')


# ===========================
# MATERIALES DE UN CURSO
# ===========================
@bp.route('/materials/<int:course_id>')
@login_required
def view_materials(course_id):
    #hacer una consulta para verificar que el alumno está inscripto
    # y devolver los materiales del curso
    # Ejemplo básico:
    flash(f"Materiales del curso {course_id} aún no implementados.", "info")
    return redirect(url_for('user.dashboard'))


# ===========================
# DESCARGAR CERTIFICADO
# ===========================
@bp.route('/certificate/download/<int:course_id>')
@login_required
def download_certificate(course_id):
    # verificar si current_user tiene un certificado para ese curso
    # y devolver un archivo PDF o algo similar
    flash(f"Descarga de certificado del curso {course_id} aún no implementada.", "info")
    return redirect(url_for('user.dashboard'))




# ===========================
# COMPRA CURSOS
# ===========================
@bp.route('/shop')
@login_required
def shop():
    if current_user.role != 'alumno':
        flash("No tienes permiso para acceder a esta sección.", "warning")
        return redirect(url_for('user.dashboard'))

    # Verificar estado
    if not getattr(current_user, 'is_verified', True):
        flash("Tu cuenta no está verificada. No puedes comprar cursos aún.", "danger")
        return redirect(url_for('user.dashboard'))

    categories = Category.query.order_by(Category.name).all()
    category_id = request.args.get('category', type=int)

    if category_id:
        courses = Course.query.filter_by(category_id=category_id).order_by(Course.title.asc()).all()
    else:
        courses = Course.query.order_by(Course.title.asc()).all()

    return render_template('course/shop.html', categories=categories, courses=courses, selected_category=category_id)

@bp.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)

    # comprobar si ya está inscrito
    already_bought = StudentCourse.query.filter_by(
        student_id=current_user.id,
        course_id=course.id
    ).first() is not None

    return render_template('course/detail.html',
                           course=course,
                           already_bought=already_bought)





# ================= BUY COURSE =============


# @bp.route('/course/<int:course_id>/buy', methods=['GET', 'POST'])
# @login_required
# def buy_course(course_id):
#     course = Course.query.get_or_404(course_id)

#     # Verificar si ya está inscrito
#     already_bought = StudentCourse.query.filter_by(
#         student_id=current_user.id,
#         course_id=course.id
#     ).first()
#     if already_bought:
#         flash("Ya estás inscrito en este curso.", "info")
#         return redirect(url_for('user.course_detail', course_id=course.id))

#     payment_method = request.form.get('payment_method')

#     # Validar método de pago
#     valid_methods = ['tarjeta', 'paypal', 'transferencia']
#     if payment_method not in valid_methods:
#         flash("Por favor, seleccioná un método de pago válido.", "warning")
#         return redirect(url_for('user.course_detail', course_id=course.id))

#     # Lógica para calcular precio, etc.
#     amount = course.price

#     # Crear registro de pago
#     payment = Payment(
#         student_id=current_user.id,
#         course_id=course.id,
#         amount=amount,
#         payment_method=payment_method,
#         verified=True  # cambiar según proceso real de verificación
#     )
#     db.session.add(payment)
#     db.session.commit()

#     # Crear inscripción
#     student_course = StudentCourse(
#         student_id=current_user.id,
#         course_id=course.id,
#         payment_status='verificado'  # o 'pendiente' según lógica
#     )
#     db.session.add(student_course)
#     db.session.commit()

#     # Enviar correo con plantilla HTML
#     msg = Message(
#         subject=f"Confirmación de compra: {course.title}",
#         sender=current_app.config['MAIL_DEFAULT_SENDER'],
#         recipients=[current_user.email]
#     )

#     # Opción: podés generar una URL para el recibo si lo subís a Firebase o lo guardás
#     receipt_url = payment.receipt_url if hasattr(payment, 'receipt_url') else None

#     msg.html = render_template(
#         'emails/payments_receipt.html',
#         user=current_user,
#         course=course,
#         payment=payment,
#         receipt_url=receipt_url
#     )

#     mail.send(msg)
  

#     flash("Compra realizada con éxito. ¡Te enviamos un comprobante por correo!", "success")
#     return redirect(url_for('user.dashboard'))
  

@bp.route('/course/<int:course_id>/buy', methods=['GET', 'POST'])
@login_required
def buy_course(course_id):
    course = Course.query.get_or_404(course_id)

    # Verificar si ya está inscrito
    already_bought = StudentCourse.query.filter_by(
        student_id=current_user.id,
        course_id=course.id
    ).first()
    if already_bought:
        flash("Ya estás inscrito en este curso.", "info")
        return redirect(url_for('user.course_detail', course_id=course.id))

    if request.method == 'GET':
        return render_template('user/buy_course.html', course=course)

    # POST: Proceso de compra
    payment_method = request.form.get('payment_method')
    valid_methods = ['tarjeta', 'paypal', 'transferencia']
    if payment_method not in valid_methods:
        flash("Por favor, seleccioná un método de pago válido.", "warning")
        return redirect(url_for('user.buy_course', course_id=course.id))

    amount = course.price
    payment = Payment(
        student_id=current_user.id,
        course_id=course.id,
        amount=amount,
        payment_method=payment_method,
        verified=True  # o False si requiere validación posterior
    )
    db.session.add(payment)
    db.session.commit()

    student_course = StudentCourse(
        student_id=current_user.id,
        course_id=course.id,
        payment_status='verificado'
    )
    db.session.add(student_course)
    db.session.commit()

    msg = Message(
        subject=f"Confirmación de compra: {course.title}",
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[current_user.email]
    )
    receipt_url = getattr(payment, 'receipt_url', None)

    msg.html = render_template(
        'emails/payments_receipt.html',
        user=current_user,
        course=course,
        payment=payment,
        receipt_url=receipt_url
    )
    mail.send(msg)

    flash("Compra realizada con éxito. ¡Te enviamos un comprobante por correo!", "success")
    return redirect(url_for('user.dashboard'))





@bp.route('/payment/confirm/<int:payment_id>', methods=['POST'])
@login_required
def confirm_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    payment.verified = True
    db.session.commit()

    # Obtener usuario y curso asociados
    user = User.query.get(payment.student_id)
    course = Course.query.get(payment.course_id)

    # Enviar correo de confirmación
    send_payment_receipt(user, course, payment)

    flash("Pago confirmado y correo enviado.", "success")
    return redirect(url_for('user.profile'))  # o a donde quieras redirigir
