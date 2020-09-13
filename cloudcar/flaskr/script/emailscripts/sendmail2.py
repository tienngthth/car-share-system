from flask import Flask, render_template, redirect, url_for
from flask_mail import Mail,  Message
app = Flask(__name__)
app.config.update(
MAIL_SERVER = 'smtp.gmail.com',
MAIL_PORT = 465,
MAIL_USE_SSL = True,
MAIL_USERNAME = 'testcloudcartest@gmail.com',
MAIL_PASSWORD = 'acNDDd3C7LafxzLp',
)

mail = Mail(app)

@app.route('/send-mail/')
def send_mail():
    msg = mail.send_message(
        'Send Mail tutorial!',
        sender='testcloudcartest@gmail.com',
        recipients=['sean.a.boyce@gmail.com'],
        body="Congratulations you've succeeded!"
    )
    return 'Mail sent'

