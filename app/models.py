from datetime import datetime, timezone
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='tenant')
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    is_banned = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    properties = db.relationship('Property', backref='landlord', lazy='dynamic')
    requests = db.relationship('Request', backref='tenant', lazy='dynamic',
                               foreign_keys='Request.tenant_id')
    reviews_given = db.relationship('Review', backref='author', lazy='dynamic',
                                    foreign_keys='Review.author_id')
    reviews_received = db.relationship('Review', backref='landlord_rel', lazy='dynamic',
                                       foreign_keys='Review.landlord_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def is_landlord(self):
        return self.role == 'landlord'

    def is_tenant(self):
        return self.role == 'tenant'


class Property(db.Model):
    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    price_type = db.Column(db.String(20), nullable=False)
    property_type = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    rooms = db.Column(db.Integer, nullable=True)
    area = db.Column(db.Float, nullable=True)
    floor = db.Column(db.Integer, nullable=True)
    max_floor = db.Column(db.Integer, nullable=True)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    images = db.relationship('PropertyImage', backref='property', lazy='dynamic',
                             cascade='all, delete-orphan')
    requests = db.relationship('Request', backref='property', lazy='dynamic',
                               cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', backref='property', lazy='dynamic',
                                cascade='all, delete-orphan')

    def main_image(self):
        img = self.images.filter_by(is_main=True).first()
        if img:
            return img.filename
        first = self.images.first()
        return first.filename if first else None


class PropertyImage(db.Model):
    __tablename__ = 'property_images'

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    is_main = db.Column(db.Boolean, default=False)


class Request(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('user_id', 'property_id'),)


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (db.UniqueConstraint('author_id', 'landlord_id'),)
