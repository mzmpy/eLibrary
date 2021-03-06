# -*- coding: utf-8 -*-

from flask_mail import Message
from app import mail
from threading import Thread
from app import app
from flask import render_template

# def send_async_email(app, msg):
#     with app.app_context():
#         mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # 在 pythonanywhere 上无法使用多线程
    # Thread(target=send_async_email, args=(app, msg)).start()
    with app.app_context():
        mail.send(msg)

def send_register_verification_email(user):
    token = user.get_register_verification_token()
    send_email('Register Verification',
            sender=app.config['ADMINS'][0],
            recipients=[user.email],
            text_body=render_template('email/verification_email.txt', user=user, token=token), 
            html_body=render_template('email/verification_email.html', user=user, token=token))
