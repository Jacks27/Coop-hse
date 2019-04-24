from app.v1.views import auth
from flask import Blueprint
my_v1 = Blueprint('my_v1', __name__)
my_v1.add_url_rule('/signup', view_func=auth.signup, methods=['POST'])
my_v1.add_url_rule('/login', view_func=auth.login, methods=['POST'])
