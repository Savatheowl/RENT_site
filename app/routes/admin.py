from flask import Blueprint

admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')


@admin_bp.route('/')
def index():
    return 'admin page'


@admin_bp.route('/user/<int:id>/ban', methods=['POST'])
def ban_user(id):
    return f'ban user {id}'


@admin_bp.route('/user/<int:id>/unban', methods=['POST'])
def unban_user(id):
    return f'unban user {id}'


@admin_bp.route('/property/<int:id>/hide', methods=['POST'])
def hide_property(id):
    return f'hide property {id}'


@admin_bp.route('/property/<int:id>/delete', methods=['POST'])
def delete_property(id):
    return f'delete property {id}'


@admin_bp.route('/review/<int:id>/delete', methods=['POST'])
def delete_review(id):
    return f'delete review {id}'
