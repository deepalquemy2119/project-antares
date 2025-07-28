
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from app.models import db, Certificado, User, Course, StudentCourse, Payment, Category

from sqlalchemy import text



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

    return render_template('user/profile.html', user=user, fecha_hoy=datetime.today())

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
        courses = Course.query.filter_by(category_id=category_id).all()
    else:
        courses = Course.query.all()

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










@bp.route('/course/<int:course_id>/buy', methods=['POST'])
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

    payment_method = request.form.get('payment_method')

    # lógica para calcular precio, etc.
    amount = 100.00  # ejemplo fijo

    # Crear registro de pago
    payment = Payment(
        student_id=current_user.id,
        course_id=course.id,
        amount=amount,
        payment_method=payment_method,
        verified=True  # o False si primero verificas
    )
    db.session.add(payment)
    db.session.commit()

    # Crear inscripción
    student_course = StudentCourse(
        student_id=current_user.id,
        course_id=course.id,
        payment_status='pagado'
    )
    db.session.add(student_course)
    db.session.commit()

    flash("Compra realizada con éxito. ¡Ya estás inscrito!", "success")
    return redirect(url_for('user.dashboard'))
