from flask_mail import Message
from oorjan import app, as_mail


def job2(t, j):
    with app.app_context():
        msg = Message('Oorjan Alerting Service', recipients=[
                      'ishaansutaria@gmail.com'])
        msg.body = 'Oorjan Flask App Cha'
        as_mail.send(msg)
    print 'mail sent'
