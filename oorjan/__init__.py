from flask import Flask
from oorjan.data.models import db
from oorjan.apiv1.controllers import apiv1
from config import configure_app
from flask_apscheduler import APScheduler
from flask_mail import Mail

app = Flask(__name__)

configure_app(app)
db.init_app(app)
as_mail = Mail()
as_mail.init_app(app)
scheduler = APScheduler()
scheduler.init_app(app)


app.register_blueprint(apiv1, url_prefix='/apiv1')
