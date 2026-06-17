from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Property, Request, Review, User

admin_bp = Blueprint("admin", __name__)


def admin_required(f):
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash("Доступ только для администраторов.", "warning")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)

    return decorated


@admin_bp.route("/")
@login_required
@admin_required
def index():
    users = User.query.order_by(User.created_at.desc()).all()
    properties = Property.query.order_by(Property.created_at.desc()).all()
    reviews = Review.query.order_by(Review.created_at.desc()).all()

    stats = {
        "total_users": User.query.count(),
        "total_tenants": User.query.filter_by(role="tenant").count(),
        "total_landlords": User.query.filter_by(role="landlord").count(),
        "total_properties": Property.query.count(),
        "active_properties": Property.query.filter_by(status="active").count(),
        "total_requests": Request.query.count(),
        "pending_requests": Request.query.filter_by(status="pending").count(),
        "total_reviews": Review.query.count(),
    }

    return render_template(
        "admin/panel.html",
        users=users,
        properties=properties,
        reviews=reviews,
        stats=stats,
    )


@admin_bp.route("/user/<int:id>/ban", methods=["POST"])
@login_required
@admin_required
def ban_user(id):
    user = db.session.get(User, id)
    if user:
        user.is_banned = True
        db.session.commit()
        flash(f"Пользователь {user.name} забанен.", "warning")
    return redirect(url_for("admin.index"))


@admin_bp.route("/user/<int:id>/unban", methods=["POST"])
@login_required
@admin_required
def unban_user(id):
    user = db.session.get(User, id)
    if user:
        user.is_banned = False
        db.session.commit()
        flash(f"Пользователь {user.name} разбанен.", "success")
    return redirect(url_for("admin.index"))


@admin_bp.route("/property/<int:id>/hide", methods=["POST"])
@login_required
@admin_required
def hide_property(id):
    prop = db.session.get(Property, id)
    if prop:
        prop.status = "inactive"
        db.session.commit()
        flash(f'Объявление "{prop.title}" скрыто.', "warning")
    return redirect(url_for("admin.index"))


@admin_bp.route("/property/<int:id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_property(id):
    prop = db.session.get(Property, id)
    if prop:
        db.session.delete(prop)
        db.session.commit()
        flash("Объявление удалено.", "info")
    return redirect(url_for("admin.index"))


@admin_bp.route("/review/<int:id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_review(id):
    review = db.session.get(Review, id)
    if review:
        db.session.delete(review)
        db.session.commit()
        flash("Отзыв удалён.", "info")
    return redirect(url_for("admin.index"))
