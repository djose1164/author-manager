from flask_mail import Mail, Message
from flask import current_app

mail = Mail()


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[
            to,
        ],
        html=template,
    )
    mail.send(msg)
