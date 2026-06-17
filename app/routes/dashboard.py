from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates/landlord')


@dashboard_bp.route('/')
def index():
    return 'dashboard page'


@dashboard_bp.route('/request/<int:id>/approve', methods=['POST'])
def approve_request(id):
    return f'approve {id}'


@dashboard_bp.route('/request/<int:id>/reject', methods=['POST'])
def reject_request(id):
    return f'reject {id}'
