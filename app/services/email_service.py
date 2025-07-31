from flask_mail import Message
from flask import current_app, render_template, url_for
from app import mail 

def send_payment_receipt(user, course, payment):
    course_url = url_for('user.course_detail', course_id=course.id, _external=True)
    msg = Message(
        subject="Comprobante de Pago - Antares",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user.email]
    )
    msg.html = render_template(
        "emails/payment_receipt.html",
        user=user,
        course=course,
        payment=payment
    )
    mail.send(msg)
