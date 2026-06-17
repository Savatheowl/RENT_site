import os
import random
import requests
from datetime import datetime, timezone
from app import create_app, db
from app.models import User, Property, PropertyImage, Request, Favorite, Review, Agency
from faker import Faker

app = create_app()
fake = Faker('ru_RU')

CITIES = ['Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск', 'Екатеринбург',
          'Краснодар', 'Сочи', 'Нижний Новгород', 'Челябинск', 'Ростов-на-Дону']
STREETS = ['Ленина', 'Пушкина', 'Гагарина', 'Советская', 'Мира',
           'Кирова', 'Молодёжная', 'Комсомольская', 'Победы', 'Центральная']
PROPERTY_TYPES = ['apartment', 'house', 'room']
PRICE_TYPES = ['month', 'day', 'bed']

UPLOAD_DIR = os.path.join(app.root_path, 'static', 'uploads')


def download_image(filename, width=800, height=600):
    url = f'https://picsum.photos/{width}/{height}?random={random.randint(1, 10000)}'
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            path = os.path.join(UPLOAD_DIR, filename)
            with open(path, 'wb') as f:
                f.write(resp.content)
            return True
    except Exception as e:
        print(f'Failed to download {filename}: {e}')
    return False


def seed():
    print('Creating database tables...')
    with app.app_context():
        db.drop_all()
        db.create_all()

        print('Creating users...')
        admin = User(
            email='admin@renta.ru',
            role='admin',
            name='Администратор',
            phone='+7 (999) 000-00-00',
            is_banned=False,
        )
        admin.set_password('admin123')
        db.session.add(admin)

        landlords = []
        for i in range(3):
            landlord = User(
                email=f'landlord{i+1}@renta.ru',
                role='landlord',
                name=fake.name(),
                phone=f'+7 (9{random.randint(10,99)}) {random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}',
                avatar=None,
                is_banned=False,
            )
            landlord.set_password('landlord123')
            db.session.add(landlord)
            landlords.append(landlord)

        tenants = []
        for i in range(5):
            tenant = User(
                email=f'tenant{i+1}@renta.ru',
                role='tenant',
                name=fake.name(),
                phone=f'+7 (9{random.randint(10,99)}) {random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}',
                avatar=None,
                is_banned=False,
            )
            tenant.set_password('tenant123')
            db.session.add(tenant)
            tenants.append(tenant)

        db.session.commit()

        print('Creating agencies...')
        agencies = []
        agency_names = ['Городская Недвижимость', 'Этажи Плюс', 'Ключ-Аренда', 'ДомКомфорт']
        for name in agency_names:
            agency = Agency(
                name=name,
                description=f'{name} — надёжное агентство недвижимости с многолетним опытом работы на рынке аренды жилья.',
                city=random.choice(CITIES),
                phone=f'+7 (9{random.randint(10,99)}) {random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}',
                email=f'info@{name.lower().replace(" ", "")}.ru',
            )
            db.session.add(agency)
            agencies.append(agency)
        db.session.commit()

        print('Creating properties...')
        properties = []
        for i in range(10):
            city = random.choice(CITIES)
            street = random.choice(STREETS)
            price_type = random.choice(PRICE_TYPES)
            base_price = {
                'month': random.randint(15000, 80000),
                'day': random.randint(1500, 8000),
                'bed': random.randint(5000, 20000),
            }

            prop_type = random.choice(PROPERTY_TYPES)
            max_floor = random.randint(5, 25)
            floor = random.randint(1, max_floor) if prop_type == 'apartment' else None

            property_obj = Property(
                landlord_id=random.choice(landlords).id,
                agency_id=random.choice(agencies).id if random.random() > 0.5 else None,
                title=f'Уютная {random.choice(["студия", "квартира", "комната"])} на {street}, {random.randint(1, 150)}',
                description=f'Светлое уютное жильё в центре города. Рядом метро, магазины, парк. '
                            f'Идеально подходит для молодых людей и студентов. '
                            f'Полностью меблировано, есть вся необходимая техника.',
                price=base_price[price_type],
                price_type=price_type,
                property_type=prop_type,
                city=city,
                address=f'ул. {street}, д. {random.randint(1, 100)}, кв. {random.randint(1, 200)}',
                rooms=random.randint(1, 4) if random.random() > 0.3 else None,
                area=round(random.uniform(18, 120), 1),
                floor=floor,
                max_floor=max_floor if prop_type == 'apartment' else None,
                lat=random.uniform(55.5, 56.0) if 'Москв' in city else random.uniform(55.0, 60.0),
                lng=random.uniform(37.0, 38.0) if 'Москв' in city else random.uniform(30.0, 50.0),
                status='active',
            )
            db.session.add(property_obj)
            db.session.flush()
            properties.append(property_obj)

        db.session.commit()

        print('Downloading property images from picsum.photos...')
        for i, prop in enumerate(properties):
            for j in range(3):
                filename = f'prop_{prop.id}_{j}.jpg'
                print(f'  Downloading {filename}...', end=' ')
                if download_image(filename):
                    img = PropertyImage(
                        property_id=prop.id,
                        filename=filename,
                        is_main=(j == 0),
                    )
                    db.session.add(img)
                    print('OK')
                else:
                    print('FAILED')

        db.session.commit()

        print('Creating requests...')
        for _ in range(8):
            tenant = random.choice(tenants)
            property_obj = random.choice(properties)
            existing = Request.query.filter_by(
                tenant_id=tenant.id, property_id=property_obj.id
            ).first()
            if not existing:
                request_obj = Request(
                    tenant_id=tenant.id,
                    property_id=property_obj.id,
                    message=fake.text(max_nb_chars=200) if random.random() > 0.5 else None,
                    status=random.choice(['pending', 'approved', 'rejected']),
                )
                db.session.add(request_obj)

        db.session.commit()

        print('Creating favorites...')
        for _ in range(12):
            tenant = random.choice(tenants)
            property_obj = random.choice(properties)
            existing = Favorite.query.filter_by(
                user_id=tenant.id, property_id=property_obj.id
            ).first()
            if not existing:
                fav = Favorite(
                    user_id=tenant.id,
                    property_id=property_obj.id,
                )
                db.session.add(fav)

        db.session.commit()

        print('Creating reviews...')
        for tenant in tenants[:4]:
            landlord = random.choice(landlords)
            existing = Review.query.filter_by(
                author_id=tenant.id, landlord_id=landlord.id
            ).first()
            if not existing:
                review = Review(
                    author_id=tenant.id,
                    landlord_id=landlord.id,
                    rating=random.randint(3, 5),
                    text=fake.text(max_nb_chars=300) if random.random() > 0.3 else None,
                )
                db.session.add(review)

        db.session.commit()

        print()
        print('=== SEED COMPLETE ===')
        print(f'Admin:    admin@renta.ru / admin123')
        print(f'Landlord: landlord1@renta.ru / landlord123')
        print(f'Tenant:   tenant1@renta.ru / tenant123')
        print(f'Properties: {len(properties)}')
        print(f'Users: {User.query.count()}')


if __name__ == '__main__':
    seed()
