from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return 'login page'


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return 'register page'


@auth_bp.route('/logout')
def logout():
    return 'logout'
