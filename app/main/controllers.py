from flask import Blueprint


apiv1 = Blueprint('apiv1', __name__)


@apiv1.route('/')
def index():
    return "Main"


@apiv1.route('/update')
def update():
    return "Ishaan"
