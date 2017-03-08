from flask import Flask
from main.controllers import apiv1

app = Flask(__name__)

app.register_blueprint(apiv1, url_prefix='/')
