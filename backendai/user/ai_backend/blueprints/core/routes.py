from flask import Blueprint

core = Blueprint('core',__name__,template_folder='templates')


@core.route('/')
def index():
    return "That a index ai backend endpoint"
