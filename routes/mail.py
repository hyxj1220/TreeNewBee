# *Created by zxiaobai on 17/1/9.

from routes import *
from flask import Flask
from conf import MAIL_PASSWORD, MAIL_USERNAME
app = Flask(__name__)

main = Blueprint('mail', __name__)

app.config.update(
    MAIL_SERVER='smtp.sina.com',
    MAIL_PROT=587,
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_DEBUG=True,
    MAIL_USE_TLS=True,
)

mail = Mail(app)


@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    send_async_email(app, msg)


@main.route('/send', methods=['POST'])
def send_mail():
    subject, sender, recipients, check_code, text_body = sent_email_config()
    form = request.form
    recipients.append(form['email'])
    u = User.query.filter_by(email=form['email']).first()
    if u is None:
        u = User(form)
        u.code = check_code
        u.avatar = 'avatar%s.jpeg' % ''.join([str(i) for i in random.sample(range(0, 9), 1)])
        u.save()
        msg = '验证码已发送至邮箱'
        send_email(subject, sender, recipients, text_body)
        return api_response(True, message=msg)
    if u.password != '':
        msg = '该邮箱已被注册'
        return api_response(False, message=msg)
    u.code = check_code
    u.email = form['email']
    u.save()
    send_email(subject, sender, recipients, text_body)
    msg = '验证码已发送至邮箱'
    return api_response(True, message=msg)
