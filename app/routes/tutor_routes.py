
# Para sincronizar ddbb
from sync.helpers import enqueue_sync



from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, send_from_directory, abort
)
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid
from functools import wraps

from app.ddbb.connection.conector import get_mysql_connection

tutor_bp = Blueprint('tutor', __name__, template_folder='../templates/tutor')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {
    'video': ['.mp4', '.mov', '.avi'],
    'image': ['.jpg', '.jpeg', '.png'],
    'pdf': ['.pdf'],
    'texto': ['.txt', '.md'],  # agregué extensiones de texto
}

# Decorador para login y roles
def login_required(role=None):
    def wrapper(view_func):
        @wraps(view_func)
        def decorated_view(*args, **kwargs):
            if 'user_id' not in session:
                flash("Iniciá sesión para continuar.", "danger")
                return redirect(url_for('auth.login'))
            if role and session.get('user_role') != role:
                flash("Acceso denegado.", "danger")
                return redirect(url_for('public.home'))
            return view_func(*args, **kwargs)
        return decorated_view
    return wrapper

def is_tutor_authorized(course_id, tutor_id, conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses WHERE id = %s AND tutor_id = %s", (course_id, tutor_id))
    return cursor.fetchone()

def is_student_enrolled(course_id, student_id, conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student_courses WHERE course_id = %s AND student_id = %s", (course_id, student_id))
    return cursor.fetchone()

def generate_unique_filename(filename):
    ext = os.path.splitext(filename)[1]
    return f"{uuid.uuid4().hex}{ext}"

# RUTA: Dashboard del tutor (para evitar error BuildError)
@tutor_bp.route('/dashboard')
@login_required(role='tutor')
def dashboard():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM courses WHERE tutor_id = %s", (session['user_id'],))
    courses = cursor.fetchall()
    return render_template('tutor/dashboard.html', courses=courses)


#==================================

# RUTA: Crear nuevo curso
from datetime import datetime

@tutor_bp.route('/create_course', methods=['GET', 'POST'])
@login_required(role='tutor')
def create_course():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '').strip()
        duration = request.form.get('duration', '').strip()

        # Validaciones
        if not title or not description or not price or not duration:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(request.url)

        try:
            price = float(price)
            duration = int(duration)
        except ValueError:
            flash("Precio o duración inválidos.", "danger")
            return redirect(request.url)

        if price <= 0 or duration <= 0:
            flash("Precio y duración deben ser mayores a 0.", "danger")
            return redirect(request.url)

        try:
            conn = get_mysql_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO courses (title, description, price, duration, tutor_id, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                title,
                description,
                price,
                duration,
                session['user_id'],
                'borrador'  # estado inicial
            ))

            conn.commit()

        except Exception as e:
            flash(f"Error al crear el curso: {e}", "danger")
            return redirect(request.url)

        finally:
            cursor.close()
            conn.close()

        flash("Curso creado correctamente. Queda pendiente de aprobación.", "success")
        return redirect(url_for('tutor.dashboard'))

    # GET: renderiza el formulario
    return render_template('tutor/create_course.html')

#==================================



# RUTA: Subir materiales
@tutor_bp.route('/upload_materials/<int:course_id>', methods=['GET', 'POST'])
@login_required(role='tutor')
def upload_materials(course_id):
    conn = get_mysql_connection()
    course = is_tutor_authorized(course_id, session['user_id'], conn)

    if not course:
        flash("Curso no encontrado o no autorizado.", "danger")
        return redirect(url_for('tutor.dashboard'))


    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        material_type = request.form.get('file_type')  # CORRECCIÓN: usar 'file_type'

        if not uploaded_file:
            flash("No se seleccionó ningún archivo.", "danger")
            return redirect(request.url)

        filename = secure_filename(uploaded_file.filename)
        ext = os.path.splitext(filename)[1].lower()

        if ext not in ALLOWED_EXTENSIONS.get(material_type, []):
            flash("Tipo de archivo no permitido para este material.", "danger")
            return redirect(request.url)

        # Crear carpeta del curso si no existe
        course_folder = os.path.join(UPLOAD_FOLDER, f"course_{course_id}")
        os.makedirs(course_folder, exist_ok=True)

        unique_filename = generate_unique_filename(filename)
        full_path = os.path.join(course_folder, unique_filename)
        uploaded_file.save(full_path)

        # Guardamos el nombre original y la ruta relativa para la descarga
        rel_path = os.path.join(f"course_{course_id}", unique_filename)

        # Insertar en base de datos
        cursor.execute("""
            INSERT INTO materials (course_id, file_name, file_path, file_type, uploaded_at)
            VALUES (%s, %s, %s, %s, %s)
        """, (course_id, filename, rel_path, material_type, datetime.now()))
        conn.commit()

        flash("Archivo subido correctamente.", "success")
        return redirect(request.url)

    # Obtener materiales existentes
    cursor.execute("SELECT * FROM materials WHERE course_id = %s ORDER BY uploaded_at DESC", (course_id,))
    materials = cursor.fetchall()

    return render_template('materials/upload.html', course=course, materials=materials, course_id=course_id)

# RUTA: Descargar material
@tutor_bp.route('/download_material/<int:course_id>/<filename>')
@login_required()
def download_material(course_id, filename):
    user_id = session.get('user_id')
    role = session.get('user_role')

    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    access_granted = False
    if role == 'tutor' and is_tutor_authorized(course_id, user_id, conn):
        access_granted = True
    elif role == 'student' and is_student_enrolled(course_id, user_id, conn):
        access_granted = True
    elif role == 'admin':
        access_granted = True

    if not access_granted:
        flash("No autorizado.", "danger")
        return redirect(url_for('public.home'))

    cursor.execute("SELECT * FROM materials WHERE course_id = %s AND file_name = %s", (course_id, filename))
    if not cursor.fetchone():
        abort(404)

    folder = os.path.join(UPLOAD_FOLDER, f'course_{course_id}')
    return send_from_directory(folder, filename, as_attachment=True)


@tutor_bp.route('/delete_material/<int:course_id>/<int:material_id>', methods=['POST'])
@login_required(role='tutor')
def delete_material(course_id, material_id):
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    # Verificar que el curso le pertenece al tutor
    course = is_tutor_authorized(course_id, session['user_id'], conn)
    if not course:
        flash("No autorizado para este curso.", "danger")
        return redirect(url_for('tutor.dashboard'))

    # Obtener material
    cursor.execute("SELECT * FROM materials WHERE id = %s AND course_id = %s", (material_id, course_id))
    material = cursor.fetchone()
    if not material:
        flash("Material no encontrado.", "danger")
        return redirect(url_for('tutor.upload_materials', course_id=course_id))

    # Borrar archivo físico
    file_path = os.path.join('uploads', f"course_{course_id}", material['file_path'].split('/')[-1])
    if os.path.exists(file_path):
        os.remove(file_path)

    # Eliminar de la base de datos
    cursor.execute("DELETE FROM materials WHERE id = %s", (material_id,))
    conn.commit()
    conn.close()

    flash("Material eliminado correctamente.", "success")
    return redirect(url_for('tutor.upload_materials', course_id=course_id))
