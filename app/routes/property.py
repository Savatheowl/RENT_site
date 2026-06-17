from flask import Blueprint

property_bp = Blueprint('property', __name__, template_folder='../templates/property')


@property_bp.route('/<int:id>')
def detail(id):
    return f'property {id}'


@property_bp.route('/create', methods=['GET', 'POST'])
def create():
    return 'create property'


@property_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    return f'edit property {id}'


@property_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    return f'delete property {id}'


@property_bp.route('/<int:id>/favorite', methods=['POST'])
def toggle_favorite(id):
    return f'toggle favorite {id}'


@property_bp.route('/<int:id>/request', methods=['POST'])
def send_request(id):
    return f'send request {id}'
