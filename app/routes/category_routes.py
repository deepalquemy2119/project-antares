from flask import Blueprint, render_template, session, redirect, url_for, flash
from flask_login import login_required, current_user
from app.ddbb.connection.conector import get_mysql_connection

category_bp = Blueprint('category', __name__, url_prefix='/categories')


@category_bp.route('/<int:category_id>')
@login_required
def show_category(category_id):
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener nombre de la categoría
    cursor.execute("SELECT name FROM categories WHERE id = %s", (category_id,))
    category = cursor.fetchone()

    if not category:
        flash("Categoría no encontrada.", "danger")
        return redirect(url_for('public.home'))

    # Mostrar cursos según rol
    if current_user.role == 'tutor':
        cursor.execute("""
            SELECT courses.*, users.full_name AS tutor_name
            FROM courses
            JOIN users ON courses.tutor_id = users.id
            WHERE category_id = %s AND tutor_id = %s
        """, (category_id, current_user.id))

    elif current_user.role == 'admin':
        cursor.execute("""
            SELECT courses.*, users.full_name AS tutor_name
            FROM courses
            JOIN users ON courses.tutor_id = users.id
            WHERE category_id = %s
        """, (category_id,))

    else:  # Alumno
        cursor.execute("""
            SELECT courses.*, users.full_name AS tutor_name
            FROM courses
            JOIN users ON courses.tutor_id = users.id
            WHERE category_id = %s AND status = 'aprobado'
        """, (category_id,))

    courses = cursor.fetchall()

    return render_template("categories/category_list.html", courses=courses, category=category)
