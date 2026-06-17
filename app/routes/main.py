from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Property, Review, User, Request
from app.forms import ProfileForm

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    popular = Property.query.filter_by(status='active').order_by(
        Property.created_at.desc()
    ).limit(6).all()
    return render_template('main/index.html', properties=popular)


@main_bp.route('/catalog')
def catalog():
    page = request.args.get('page', 1, type=int)
    city = request.args.get('city', '')
    property_type = request.args.get('property_type', '')
    price_min = request.args.get('price_min', 0, type=int)
    price_max = request.args.get('price_max', 0, type=int)

    query = Property.query.filter_by(status='active')

    if city:
        query = query.filter(Property.city.ilike(f'%{city}%'))
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if price_min:
        query = query.filter(Property.price >= price_min)
    if price_max:
        query = query.filter(Property.price <= price_max)

    properties = query.order_by(Property.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    return render_template('main/catalog.html', properties=properties)


@main_bp.route('/about')
def about():
    return render_template('main/about.html')


@main_bp.route('/contacts')
def contacts():
    return render_template('main/contacts.html')


@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Профиль обновлён.', 'success')
        return redirect(url_for('main.profile'))
    return render_template('user/profile.html', form=form)


@main_bp.route('/favorites')
@login_required
def favorites():
    if current_user.is_tenant():
        favs = current_user.favorites.all()
        return render_template('user/favorites.html', favorites=favs)
    flash('Доступно только арендаторам.', 'warning')
    return redirect(url_for('main.index'))


@main_bp.route('/my-requests')
@login_required
def my_requests():
    if current_user.is_tenant():
        requests_list = current_user.requests.order_by(
            Request.created_at.desc()
        ).all()
        return render_template('user/requests.html', requests=requests_list)
    flash('Доступно только арендаторам.', 'warning')
    return redirect(url_for('main.index'))
