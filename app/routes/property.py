import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from PIL import Image
from app import db
from app.models import Property, PropertyImage, Request, Favorite, Review
from app.forms import PropertyForm, RequestForm, ReviewForm

property_bp = Blueprint('property', __name__)


def save_images(files, property_obj):
    upload_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    for i, file in enumerate(files):
        if file and file.filename:
            ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
            filename = f'prop_{property_obj.id}_{uuid.uuid4().hex[:8]}.{ext}'
            filepath = os.path.join(upload_dir, filename)
            img = Image.open(file)
            img.thumbnail((1200, 1200), Image.LANCZOS)
            img.save(filepath, optimize=True, quality=85)
            img = PropertyImage(
                property_id=property_obj.id,
                filename=filename,
                is_main=(i == 0 and property_obj.images.count() == 0),
            )
            db.session.add(img)


@property_bp.route('/<int:id>', methods=['GET', 'POST'])
def detail(id):
    prop = db.session.get(Property, id)
    if not prop or prop.status == 'inactive':
        flash('Объявление не найдено.', 'danger')
        return redirect(url_for('main.catalog'))

    request_form = RequestForm()
    review_form = ReviewForm()

    if request_form.validate_on_submit() and current_user.is_authenticated and current_user.is_tenant():
        existing = Request.query.filter_by(
            tenant_id=current_user.id, property_id=prop.id
        ).first()
        if existing:
            flash('Вы уже отправляли заявку на это жильё.', 'warning')
        else:
            req = Request(
                tenant_id=current_user.id,
                property_id=prop.id,
                message=request_form.message.data,
            )
            db.session.add(req)
            db.session.commit()
            flash('Заявка отправлена!', 'success')
        return redirect(url_for('property.detail', id=prop.id))

    if review_form.validate_on_submit() and current_user.is_authenticated and current_user.is_tenant():
        existing_review = Review.query.filter_by(
            author_id=current_user.id, landlord_id=prop.landlord_id
        ).first()
        if existing_review:
            flash('Вы уже оставляли отзыв этому арендодателю.', 'warning')
        else:
            review = Review(
                author_id=current_user.id,
                landlord_id=prop.landlord_id,
                rating=review_form.rating.data,
                text=review_form.text.data,
            )
            db.session.add(review)
            db.session.commit()
            flash('Отзыв добавлен!', 'success')
        return redirect(url_for('property.detail', id=prop.id))

    images = prop.images.order_by(PropertyImage.is_main.desc()).all()
    landlord_reviews = Review.query.filter_by(landlord_id=prop.landlord_id).all()
    avg_rating = round(sum(r.rating for r in landlord_reviews) / len(landlord_reviews), 1) if landlord_reviews else 0
    is_favorite = False
    if current_user.is_authenticated and current_user.is_tenant():
        is_favorite = Favorite.query.filter_by(
            user_id=current_user.id, property_id=prop.id
        ).first() is not None

    return render_template('property/detail.html',
                           property=prop, images=images,
                           request_form=request_form, review_form=review_form,
                           landlord_reviews=landlord_reviews, avg_rating=avg_rating,
                           is_favorite=is_favorite)


@property_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not current_user.is_landlord() and not current_user.is_admin():
        flash('Доступ только для арендодателей.', 'warning')
        return redirect(url_for('main.index'))

    form = PropertyForm()
    if form.validate_on_submit():
        prop = Property(
            landlord_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            price_type=form.price_type.data,
            property_type=form.property_type.data,
            city=form.city.data,
            address=form.address.data,
            rooms=form.rooms.data,
            area=form.area.data,
            floor=form.floor.data,
            max_floor=form.max_floor.data,
            lat=form.lat.data,
            lng=form.lng.data,
        )
        db.session.add(prop)
        db.session.flush()

        files = request.files.getlist('images')
        if files and files[0].filename:
            save_images(files, prop)
        else:
            img = PropertyImage(property_id=prop.id, filename='placeholder.jpg', is_main=True)
            db.session.add(img)

        db.session.commit()
        flash('Объявление создано!', 'success')
        return redirect(url_for('property.detail', id=prop.id))

    return render_template('property/form.html', form=form, title='Новое объявление')


@property_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    prop = db.session.get(Property, id)
    if not prop:
        flash('Объявление не найдено.', 'danger')
        return redirect(url_for('main.catalog'))
    if prop.landlord_id != current_user.id and not current_user.is_admin():
        flash('Это не ваше объявление.', 'warning')
        return redirect(url_for('main.index'))

    form = PropertyForm(obj=prop)
    if form.validate_on_submit():
        prop.title = form.title.data
        prop.description = form.description.data
        prop.price = form.price.data
        prop.price_type = form.price_type.data
        prop.property_type = form.property_type.data
        prop.city = form.city.data
        prop.address = form.address.data
        prop.rooms = form.rooms.data
        prop.area = form.area.data
        prop.floor = form.floor.data
        prop.max_floor = form.max_floor.data
        prop.lat = form.lat.data
        prop.lng = form.lng.data

        files = request.files.getlist('images')
        if files and files[0].filename:
            save_images(files, prop)

        db.session.commit()
        flash('Объявление обновлено!', 'success')
        return redirect(url_for('property.detail', id=prop.id))

    return render_template('property/form.html', form=form, title='Редактировать объявление', property=prop)


@property_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    prop = db.session.get(Property, id)
    if not prop:
        flash('Объявление не найдено.', 'danger')
        return redirect(url_for('main.catalog'))
    if prop.landlord_id != current_user.id and not current_user.is_admin():
        flash('Это не ваше объявление.', 'warning')
        return redirect(url_for('main.index'))

    for img in prop.images.all():
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], img.filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    db.session.delete(prop)
    db.session.commit()
    flash('Объявление удалено.', 'info')
    return redirect(url_for('main.catalog'))


@property_bp.route('/<int:id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(id):
    if not current_user.is_tenant():
        flash('Доступно только арендаторам.', 'warning')
        return redirect(request.referrer or url_for('main.index'))

    fav = Favorite.query.filter_by(user_id=current_user.id, property_id=id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        flash('Удалено из избранного.', 'info')
    else:
        fav = Favorite(user_id=current_user.id, property_id=id)
        db.session.add(fav)
        db.session.commit()
        flash('Добавлено в избранное!', 'success')

    return redirect(request.referrer or url_for('property.detail', id=id))
