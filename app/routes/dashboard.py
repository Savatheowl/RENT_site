from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Property, Request, Review

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def index():
    if not current_user.is_landlord():
        flash("Доступно только арендодателям.", "warning")
        return redirect(url_for("main.index"))

    properties = (
        Property.query.filter_by(landlord_id=current_user.id)
        .order_by(Property.created_at.desc())
        .all()
    )

    property_ids = [p.id for p in properties]
    requests = (
        Request.query.filter(Request.property_id.in_(property_ids))
        .order_by(Request.created_at.desc())
        .all()
        if property_ids
        else []
    )

    total_properties = len(properties)
    active_properties = sum(1 for p in properties if p.status == "active")
    total_requests = len(requests)
    pending_requests = sum(1 for r in requests if r.status == "pending")

    reviews = Review.query.filter_by(landlord_id=current_user.id).all()
    avg_rating = (
        round(sum(r.rating for r in reviews) / len(reviews), 1) if reviews else 0
    )

    return render_template(
        "landlord/dashboard.html",
        properties=properties,
        requests=requests,
        total_properties=total_properties,
        active_properties=active_properties,
        total_requests=total_requests,
        pending_requests=pending_requests,
        avg_rating=avg_rating,
        reviews_count=len(reviews),
    )


@dashboard_bp.route("/request/<int:id>/approve", methods=["POST"])
@login_required
def approve_request(id):
    req = db.session.get(Request, id)
    if not req:
        flash("Заявка не найдена.", "danger")
        return redirect(url_for("dashboard.index"))
    if req.property.landlord_id != current_user.id:
        flash("Это не ваше объявление.", "warning")
        return redirect(url_for("dashboard.index"))
    req.status = "approved"
    db.session.commit()
    flash("Заявка одобрена!", "success")
    return redirect(url_for("dashboard.index"))


@dashboard_bp.route("/request/<int:id>/reject", methods=["POST"])
@login_required
def reject_request(id):
    req = db.session.get(Request, id)
    if not req:
        flash("Заявка не найдена.", "danger")
        return redirect(url_for("dashboard.index"))
    if req.property.landlord_id != current_user.id:
        flash("Это не ваше объявление.", "warning")
        return redirect(url_for("dashboard.index"))
    req.status = "rejected"
    db.session.commit()
    flash("Заявка отклонена.", "info")
    return redirect(url_for("dashboard.index"))
