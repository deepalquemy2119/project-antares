from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flask_login import login_user, logout_user
import bcrypt
from app.models import User   # Importo la base de datos de SQLAlchemy
from firebase.firebase_init import get_firebase_db
from app.extensions import db


auth_bp = Blueprint('auth', __name__)

# --------------------- UTILS ---------------------

def generate_serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

def send_reset_email(to_email, reset_url):
    msg = Message(
        subject="Recuperación de contraseña - Antares",
        sender=("Antares", current_app.config['MAIL_USERNAME']),
        recipients=[to_email]
    )
    msg.body = f"""Hola,

Has solicitado restablecer tu contraseña.

Haz clic en el siguiente enlace para crear una nueva contraseña:
{reset_url}

Este enlace expirará en 1 hora.

Si no lo solicitaste, simplemente ignora este correo.
"""
    from app import mail
    mail.send(msg)

# --------------------- REGISTER ---------------------

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('rol', '').strip().lower()

        if not all([username, full_name, email, password, role]):
            error = "Por favor, completá todos los campos obligatorios."
            flash("Todos los campos son obligatorios", "danger")
            return render_template('auth/register.html', error=error)

        # Verificar duplicados
        existing_user = User.query.filter(
            (User.email == email) | (User.username == username)
        ).first()
        if existing_user:
            flash("El correo o el nombre de usuario ya están registrados", "warning")
            return render_template('auth/register.html')

        try:
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = User(
                username=username,
                full_name=full_name,
                email=email,
                password_hash=hashed_pw,
                role=role
            )
            db.session.add(new_user)
            db.session.commit()

            # Sincronizar con Firebase
            ref = get_firebase_db().reference(f"users/{new_user.id}")
            ref.set({
                "full_name": full_name,
                "email": email,
                "role": role
            })

            flash("Registro exitoso. Inicia sesión.", "success")
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            print(f"[ERROR REGISTER] {e}")
            error = "Error en el registro"
            flash(error, "danger")
            return render_template('auth/register.html', error=error)

    return render_template('auth/register.html', error=error)

# --------------------- LOGIN ---------------------

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not user_input or not password:
            flash("Completa todos los campos", "danger")
            return render_template('auth/login.html')

        # Buscar el usuario por email o username
        user_obj = User.query.filter(
            (User.email == user_input) | (User.username == user_input)
        ).first()

        # Validar contraseña
        if user_obj and bcrypt.checkpw(password.encode('utf-8'), user_obj.password_hash.encode('utf-8')):
            # Login exitoso
            login_user(user_obj)
            session['user_id'] = user_obj.id
            session['user_name'] = user_obj.full_name
            session['user_role'] = user_obj.role

            flash(f"Bienvenido, {user_obj.full_name}", "success")
            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)
            elif user_obj.role == 'tutor':
                return redirect(url_for('tutor.dashboard'))
            elif user_obj.role == 'admin':
                return redirect(url_for('admin_bp.dashboard'))
            else:
                return redirect(url_for('user.dashboard'))
        else:
            flash("Credenciales inválidas", "danger")
            return render_template('auth/login.html')

    # Si es GET, solo muestra el formulario
    return render_template('auth/login.html')


# --------------------- FORGOT PASSWORD ---------------------

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if not email:
            flash("Por favor ingresa tu correo electrónico", "warning")
            return render_template('auth/forgot_password.html')

        try:
            user_obj = User.query.filter_by(email=email).first()
            if user_obj:
                serializer = generate_serializer()
                token = serializer.dumps(email, salt='password-reset-salt')
                reset_url = url_for('auth.reset_password', token=token, _external=True)
                send_reset_email(email, reset_url)
                flash("Te hemos enviado un correo con el enlace de recuperación.", "info")
            else:
                flash("Ese correo no está registrado.", "danger")

        except Exception as e:
            print(f"[ERROR FORGOT PASSWORD] {e}")
            flash("Ocurrió un error procesando tu solicitud.", "danger")

    return render_template('auth/forgot_password.html')

# --------------------- RESET PASSWORD ---------------------

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Si es POST, el token puede venir también en el formulario (campo oculto)
    if request.method == 'POST':
        token = request.form.get('token') or token

    serializer = generate_serializer()
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception as e:
        print(f"[TOKEN ERROR] {e}")
        flash("El enlace de recuperación ha expirado o es inválido.", "danger")
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('password', '').strip()
        if not new_password:
            flash("La nueva contraseña no puede estar vacía", "warning")
            return render_template('auth/reset_password.html', token=token)

        try:
            hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            user_obj = User.query.filter_by(email=email).first()
            if user_obj:
                user_obj.password_hash = hashed_pw
                db.session.commit()
                flash("Contraseña actualizada correctamente. Ahora podés iniciar sesión.", "success")
                return redirect(url_for('auth.login'))
            else:
                flash("Usuario no encontrado", "danger")
        except Exception as e:
            db.session.rollback()
            print(f"[ERROR RESET PASSWORD] {e}")
            flash("Ocurrió un error actualizando la contraseña.", "danger")

    # En GET o en POST fallido mostramos el formulario, pasando token para que el formulario lo incluya
    return render_template('auth/reset_password.html', token=token)

# --------------------- LOGOUT ---------------------

@auth_bp.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for('public.home'))
