


from app.extensions import db
from flask_login import UserMixin
from sqlalchemy import Enum, CheckConstraint
from datetime import datetime


# =========================
# USER
# =========================
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100))
    role = db.Column(db.Enum('admin', 'tutor', 'alumno'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    tutor_courses = db.relationship('Course', backref='tutor', foreign_keys='Course.tutor_id', lazy='dynamic')
    admin_courses = db.relationship('Course', backref='admin', foreign_keys='Course.admin_id', lazy='dynamic')
    student_courses = db.relationship('StudentCourse', back_populates='student', lazy='dynamic')
    certificados = db.relationship('Certificado', back_populates='student', lazy='dynamic')
    payments = db.relationship('Payment', backref='student', lazy='dynamic')
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')
    payment_history_changes = db.relationship(
    'PaymentHistory',
    foreign_keys='PaymentHistory.changed_by',
    backref='changed_by_user_payment_history',
    lazy='dynamic')
    audit_logs = db.relationship(
    'AuditLog',
    foreign_keys='AuditLog.changed_by',
    backref='changed_by_user_audit_logs',
    lazy='dynamic'
)

    def __repr__(self):
        return f"<User {self.username}>"


# =========================
# CATEGORY
# =========================
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    courses = db.relationship('Course', backref='category', lazy='dynamic')


# =========================
# COURSE
# =========================
class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    tutor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    status = db.Column(db.Enum('borrador', 'publicado', 'con reseñas', 'aprobado'),
    nullable=False,
    default='borrador'
)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    students = db.relationship('StudentCourse', back_populates='course', lazy='dynamic')
    certificados = db.relationship('Certificado', back_populates='course', lazy='dynamic')
    reviews = db.relationship('Review', back_populates='course', lazy='dynamic')
    payments = db.relationship('Payment', backref='course', lazy='dynamic')
    course_files = db.relationship('CourseFile', backref='course', lazy='dynamic')
    materials = db.relationship('Material', backref='course', lazy='dynamic')

    __table_args__ = (
        CheckConstraint('price > 0', name='chk_price_positive'),
        CheckConstraint('duration > 0', name='chk_duration_positive'),
    )

    def __repr__(self):
        return f"<Course {self.title}>"


# =========================
# COURSE FILES
# =========================
class CourseFile(db.Model):
    __tablename__ = 'course_files'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    file_type = db.Column(db.Enum('video', 'pdf', 'image', 'texto'), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


# =========================
# MATERIALS
# =========================
class Material(db.Model):
    __tablename__ = 'materials'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    file_name = db.Column(db.String(255))
    file_path = db.Column(db.Text)
    file_type = db.Column(db.String(50))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


# =========================
# STUDENT_COURSES (pivot)
# =========================
class StudentCourse(db.Model):
    __tablename__ = 'student_courses'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    payment_status = db.Column(db.Enum('pendiente', 'verificado'), default='pendiente')
    payment_date = db.Column(db.DateTime)
    payment_receipt_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('User', back_populates='student_courses')
    course = db.relationship('Course', back_populates='students')

    def __repr__(self):
        return f"<StudentCourse student={self.student_id} course={self.course_id}>"


# =========================
# PAYMENTS
# =========================
class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.Enum('tarjeta', 'paypal', 'transferencia'))
    receipt_url = db.Column(db.String(255))
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('amount > 0', name='chk_amount_positive'),
    )


# =========================
# MESSAGES
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
# CERTIFICADOS
# =========================
class Certificado(db.Model):
    __tablename__ = 'certificados'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    certificate_code = db.Column(db.String(50), unique=True, nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('User', back_populates='certificados')
    course = db.relationship('Course', back_populates='certificados')

    __table_args__ = (
        db.UniqueConstraint('student_id', 'course_id', name='chk_certificate_unique'),
    )

    def __repr__(self):
        return f"<Certificado student={self.student_id} course={self.course_id}>"


# =========================
# REVIEWS
# =========================
class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship('User', backref='reviews', lazy='select')
    course = db.relationship('Course', back_populates='reviews')

    __table_args__ = (
        CheckConstraint('rating >= 1 AND rating <= 5', name='chk_rating_range'),
        db.UniqueConstraint('student_id', 'course_id', name='chk_review_unique'),
    )


# =========================
# PAYMENT_HISTORY
# =========================
class PaymentHistory(db.Model):
    __tablename__ = 'payment_history'

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False)
    old_status = db.Column(db.Enum('pendiente', 'verificado'), nullable=False)
    new_status = db.Column(db.Enum('pendiente', 'verificado'), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    changed_by_user = db.relationship('User', foreign_keys=[changed_by])


# =========================
# AUDIT_LOG
# =========================
class AuditLog(db.Model):
    __tablename__ = 'audit_log'

    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(100), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.Enum('INSERT', 'UPDATE', 'DELETE'), nullable=False)
    old_data = db.Column(db.Text)
    new_data = db.Column(db.Text)
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)

    changed_by_user = db.relationship('User', foreign_keys=[changed_by])


# =========================
# SYNC_QUEUE
# =========================
class SyncQueue(db.Model):
    __tablename__ = 'sync_queue'

    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(255), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.Enum('INSERT', 'UPDATE', 'DELETE'), nullable=False)
    processed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
