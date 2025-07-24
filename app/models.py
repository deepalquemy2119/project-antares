from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum, CheckConstraint
from datetime import datetime


from flask_login import UserMixin

db = SQLAlchemy()

# =========================
# Tabla: users
# =========================
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    role = db.Column(Enum('admin', 'tutor', 'alumno'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    courses = db.relationship('Course', backref='tutor', foreign_keys='Course.tutor_id')
    admin_courses = db.relationship('Course', backref='admin', foreign_keys='Course.admin_id')


# =========================
# Tabla: courses
# =========================
class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10,2), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(Enum('borrador', 'publicado', 'con reseñas'), default='borrador')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('price > 0', name='chk_price_positive'),
        CheckConstraint('duration > 0', name='chk_duration_positive'),
    )


# =========================
# Tabla: course_files
# =========================
class CourseFile(db.Model):
    __tablename__ = 'course_files'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    file_type = db.Column(Enum('video', 'pdf', 'image', 'texto'), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


# =========================
# Tabla: materials
# =========================
class Material(db.Model):
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    file_name = db.Column(db.String(255))
    file_path = db.Column(db.Text)
    file_type = db.Column(db.String(50))


# =========================
# Tabla: student_courses
# =========================
class StudentCourse(db.Model):
    __tablename__ = 'student_courses'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    payment_status = db.Column(Enum('pendiente', 'verificado'), default='pendiente')
    payment_date = db.Column(db.DateTime)
    payment_receipt_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# =========================
# Tabla: payments
# =========================
class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    payment_method = db.Column(Enum('tarjeta', 'paypal', 'transferencia'))
    receipt_url = db.Column(db.String(255))
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('amount > 0', name='chk_amount_positive'),
    )


# =========================
# Tabla: messages
# =========================
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(100))
    body = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)


# =========================
# Tabla: certificados
# =========================
class Certificado(db.Model):
    __tablename__ = 'certificados'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    certificate_code = db.Column(db.String(50), unique=True, nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('student_id', 'course_id', name='chk_certificate_unique'),
    )


# =========================
# Tabla: reviews
# =========================
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='chk_rating_range'),
        db.UniqueConstraint('student_id', 'course_id', name='chk_review_unique'),
    )


# =========================
# Tabla: payment_history
# =========================
class PaymentHistory(db.Model):
    __tablename__ = 'payment_history'

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)
    old_status = db.Column(Enum('pendiente', 'verificado'), nullable=False)
    new_status = db.Column(Enum('pendiente', 'verificado'), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


# =========================
# Tabla: audit_log
# =========================
class AuditLog(db.Model):
    __tablename__ = 'audit_log'

    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(100), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    action = db.Column(Enum('INSERT', 'UPDATE', 'DELETE'), nullable=False)
    old_data = db.Column(db.Text)
    new_data = db.Column(db.Text)
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)


# =========================
# Tabla: sync_queue
# =========================
class SyncQueue(db.Model):
    __tablename__ = 'sync_queue'

    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(255), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    action = db.Column(Enum('INSERT', 'UPDATE', 'DELETE'), nullable=False)
    processed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

