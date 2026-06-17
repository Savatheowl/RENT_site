from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import func
from app import db
from app.models import Property, Review, User, Request, Agency
from app.forms import ProfileForm

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    popular = Property.query.filter_by(status='active').order_by(
        Property.created_at.desc()
    ).limit(6).all()
    return render_template('main/index.html', properties=popular)


@main_bp.route('/agencies')
def agencies():
    all_agencies = Agency.query.order_by(Agency.name).all()
    return render_template('main/agencies.html', agencies=all_agencies)


@main_bp.route('/agencies/<int:id>')
def agency_detail(id):
    agency = Agency.query.get_or_404(id)
    properties = Property.query.filter_by(agency_id=id, status='active').all()
    return render_template('main/agency_detail.html', agency=agency, properties=properties)


@main_bp.route('/catalog')
def catalog():
    page = request.args.get('page', 1, type=int)
    city = request.args.get('city', '')
    property_type = request.args.get('property_type', '')
    price_min = request.args.get('price_min', 0, type=int)
    price_max = request.args.get('price_max', 0, type=int)
    area_min = request.args.get('area_min', 0, type=float)
    area_max = request.args.get('area_max', 0, type=float)
    floor_min = request.args.get('floor_min', 0, type=int)
    floor_max = request.args.get('floor_max', 0, type=int)

    agg = db.session.query(
        func.min(Property.price).label('min_price'),
        func.max(Property.price).label('max_price'),
        func.min(Property.area).label('min_area'),
        func.max(Property.area).label('max_area'),
    ).filter(Property.status == 'active').first()

    min_price = agg.min_price or 0
    max_price = agg.max_price or 100000
    min_area = agg.min_area or 0
    max_area = agg.max_area or 200

    query = Property.query.filter_by(status='active')

    if city:
        query = query.filter(Property.city.ilike(f'%{city}%'))
    if property_type:
        query = query.filter(Property.property_type == property_type)
    if price_min:
        query = query.filter(Property.price >= price_min)
    if price_max:
        query = query.filter(Property.price <= price_max)
    if area_min:
        query = query.filter(Property.area >= area_min)
    if area_max:
        query = query.filter(Property.area <= area_max)
    if floor_min:
        query = query.filter(Property.floor >= floor_min)
    if floor_max:
        query = query.filter(Property.floor <= floor_max)

    properties = query.order_by(Property.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    return render_template('main/catalog.html', properties=properties,
                           min_price=min_price, max_price=max_price,
                           min_area=min_area, max_area=max_area)


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
