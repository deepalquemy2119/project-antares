from flask import Blueprint, render_template, session
from datetime import datetime
from app.models import Course

public_bp = Blueprint('public', __name__, template_folder='../templates')


@public_bp.route('/')
def home():
    fecha_actual = datetime.now().strftime('%Y')
    
    # Si el usuario está logueado, obtener los cursos que ha comprado
    user_courses = []
    if 'user_id' in session:
        # Aquí asumimos que los cursos comprados están en una relación Many-to-Many
        user_courses = [course.id for course in session.get('user_courses', [])]  #cursos obtenidos correctamente
    
    # Obtener todos los cursos disponibles (ajustar si es necesario para filtrarlos)
    courses = Course.query.all()  # Aquí obtenemos todos los cursos disponibles
    
    return render_template('public/home.html', 
        fecha_completa=fecha_actual, 
        courses=courses,  
        user_courses=user_courses)
