from flask import Blueprint

main_bp = Blueprint('main', __name__, template_folder='../templates/main')


@main_bp.route('/')
def index():
    return 'index page'


@main_bp.route('/catalog')
def catalog():
    return 'catalog page'


@main_bp.route('/about')
def about():
    return 'about page'


@main_bp.route('/contacts')
def contacts():
    return 'contacts page'
