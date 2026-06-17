# RENTA — Маркетплейс аренды жилья

**RENTA** — это веб-платформа для поиска и сдачи в аренду квартир, домов и комнат. Проект реализован на Flask с серверным рендерингом и поддерживает три роли пользователей: арендаторы, арендодатели и администраторы.

---

## Содержание

- [Технологии](#технологии)
- [Функциональность](#функциональность)
- [Установка и запуск](#установка-и-запуск)
- [Наполнение базы данных](#наполнение-базы-данных)
- [Структура проекта](#структура-проекта)
- [Модели данных](#модели-данных)
- [Маршруты](#маршруты)
- [Учётные записи для тестирования](#учётные-записи-для-тестирования)

---

## Технологии

### Бэкенд
| Технология | Назначение |
|---|---|
| **Python 3.14** | Язык разработки |
| **Flask 3.1** | Веб-фреймворк |
| **Flask-SQLAlchemy** | ORM для работы с БД |
| **Flask-Login** | Управление сессиями пользователей |
| **Flask-WTF / WTForms** | Формы и CSRF-защита |
| **Werkzeug** | Хеширование паролей |
| **Jinja2** | Шаблонизатор |
| **Pillow** | Обработка изображений |
| **Faker** | Генерация тестовых данных |

### Фронтенд
| Технология | Назначение |
|---|---|
| **Bootstrap 5.3** | CSS-фреймворк |
| **Bootstrap Icons 1.11.3** | Иконки |
| **noUiSlider 15.8.1** | Ползунки диапазонов (цена, площадь) |
| **Leaflet.js 1.9.4** | Интерактивные карты |
| **Google Fonts (Inter, Montserrat)** | Шрифты |

### База данных
- **SQLite** (файл `instance/renta.db`)

---

## Функциональность

### Для всех пользователей (без регистрации)
- Просмотр каталога объявлений с фильтрацией (город, тип недвижимости, цена, площадь, этаж)
- Просмотр карточки объявления: фото, описание, карта, информация об арендодателе
- Поиск агентств недвижимости и просмотр их объявлений
- Интерактивная карта на странице контактов

### Для арендаторов
- Отправка заявок на аренду
- Добавление объявлений в избранное
- Управление профилем
- Просмотр статуса отправленных заявок
- Оценка арендодателей

### Для арендодателей
- Личный кабинет со статистикой (всего/активных объектов, заявок)
- Публикация, редактирование и удаление объявлений
- Загрузка фотографий к объявлениям
- Просмотр и обработка входящих заявок (одобрить / отклонить)
- Просмотр рейтинга и отзывов

### Для администраторов
- Панель управления со сводной статистикой
- Управление пользователями (блокировка / разблокировка)
- Управление объявлениями (скрытие / удаление)
- Управление отзывами (удаление)

---

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/username/renta.git
cd renta
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка конфигурации (опционально)

По умолчанию используется SQLite и dev-ключ. Можно переопределить через переменные окружения:

```bash
export SECRET_KEY="my-secret-key"
export DATABASE_URL="postgresql://user:password@localhost/renta"
```

### 5. Запуск

```bash
python run.py
```

Приложение будет доступно по адресу: `http://127.0.0.1:5000`

### 6. Наполнение базы тестовыми данными

```bash
python seed.py
```

---

## Наполнение базы данных

Скрипт `seed.py` создаёт:
- 1 администратора
- 3 арендодателей
- 5 арендаторов
- 4 агентства недвижимости
- 10 объявлений (по 3 изображения каждое)
- 8 заявок на аренду
- 12 избранных
- 4 отзыва

Изображения для наполнения находятся в папке `seed/img/` (файлы `prop1.jpg` – `prop40.jpg`).

---

## Структура проекта

```
RENT_site/
├── app/
│   ├── __init__.py          # Фабрика приложения, регистрация蓝图, обработчики ошибок
│   ├── forms.py             # WTForms формы
│   ├── models.py            # SQLAlchemy модели
│   ├── routes/
│   │   ├── admin.py         # Маршруты админ-панели
│   │   ├── auth.py          # Аутентификация (вход, регистрация, выход)
│   │   ├── dashboard.py     # Кабинет арендодателя
│   │   ├── main.py          # Публичные страницы
│   │   └── property.py      # CRUD объявлений и избранное
│   ├── static/
│   │   ├── css/style.css    # Пользовательские стили
│   │   ├── js/script.js     # Пользовательские скрипты
│   │   ├── bootstrap-5.3/   # Bootstrap (vendored)
│   │   ├── bootstrap-icons-1.11.3/  # Иконки Bootstrap (vendored)
│   │   ├── nouislider-15.8.1/       # noUiSlider (vendored)
│   │   ├── images/          # Статические изображения
│   │   └── uploads/         # Загруженные изображения объявлений
│   └── templates/
│       ├── base.html        # Базовый шаблон (навбар, футер, flash-сообщения)
│       ├── admin/panel.html
│       ├── auth/login.html, register.html
│       ├── errors/403.html, 404.html, 500.html
│       ├── landlord/dashboard.html
│       ├── main/index.html, catalog.html, about.html, contacts.html,
│       │      agencies.html, agency_detail.html
│       ├── property/detail.html, form.html
│       └── user/profile.html, favorites.html, requests.html
├── config.py                # Конфигурация Flask
├── run.py                   # Точка входа
├── seed.py                  # Скрипт наполнения БД
├── seed/
│   └── img/                 # Исходные изображения для наполнения
├── instance/
│   └── renta.db             # Файл БД SQLite
├── requirements.txt         # Зависимости Python
└── .gitignore
```

---

## Модели данных

### User (`users`)
| Поле | Тип | Описание |
|---|---|---|
| id | Integer (PK) | ID пользователя |
| email | String (unique) | Email |
| password_hash | String | Хеш пароля |
| role | String | `admin`, `landlord`, `tenant` |
| name | String | Имя |
| phone | String | Телефон |
| avatar | String | Аватар |
| is_banned | Boolean | Заблокирован ли |
| created_at | DateTime | Дата регистрации |

### Property (`properties`)
| Поле | Тип | Описание |
|---|---|---|
| id | Integer (PK) | ID объявления |
| landlord_id | Integer (FK) | ID арендодателя |
| agency_id | Integer (FK, nullable) | ID агентства |
| title | String | Заголовок |
| description | Text | Описание |
| price | Integer | Цена |
| price_type | String | `month`, `day`, `bed` |
| property_type | String | `apartment`, `house`, `room` |
| city | String | Город |
| address | String | Адрес |
| rooms | Integer | Кол-во комнат |
| area | Float | Площадь (м²) |
| floor / max_floor | Integer | Этаж / Этажность |
| lat / lng | Float | Координаты |
| status | String | `active`, `inactive` |

### PropertyImage (`property_images`)
- `id`, `property_id` (FK), `filename`, `is_main`

### Agency (`agencies`)
- `id`, `name`, `description`, `logo`, `city`, `phone`, `email`

### Request (`requests`)
- `id`, `tenant_id` (FK), `property_id` (FK), `message`, `status` (`pending`, `approved`, `rejected`)

### Favorite (`favorites`)
- `id`, `user_id` (FK), `property_id` (FK), unique(`user_id`, `property_id`)

### Review (`reviews`)
- `id`, `author_id` (FK), `landlord_id` (FK), `rating` (1–5), `text`, unique(`author_id`, `landlord_id`)

---

## Маршруты

### Публичные
| Маршрут | Описание |
|---|---|
| `GET /` | Главная страница |
| `GET /catalog` | Каталог с фильтрами и пагинацией |
| `GET /agencies` | Список агентств |
| `GET /agencies/<id>` | Карточка агентства |
| `GET /about` | О проекте |
| `GET /contacts` | Контакты и карта |

### Аутентификация
| Маршрут | Описание |
|---|---|
| `GET/POST /auth/login` | Вход |
| `GET/POST /auth/register` | Регистрация |
| `GET /auth/logout` | Выход |

### Объявления
| Маршрут | Описание |
|---|---|
| `GET/POST /property/<id>` | Детали объявления + заявка |
| `GET/POST /property/create` | Создание объявления |
| `GET/POST /property/<id>/edit` | Редактирование |
| `POST /property/<id>/delete` | Удаление |
| `POST /property/<id>/favorite` | Избранное (toggle) |

### Кабинет арендодателя
| Маршрут | Описание |
|---|---|
| `GET /dashboard/` | Статистика, заявки, объявления |
| `POST /dashboard/request/<id>/approve` | Одобрить заявку |
| `POST /dashboard/request/<id>/reject` | Отклонить заявку |

### Админ-панель
| Маршрут | Описание |
|---|---|
| `GET /admin/` | Панель управления |
| `POST /admin/user/<id>/ban` | Заблокировать пользователя |
| `POST /admin/user/<id>/unban` | Разблокировать пользователя |
| `POST /admin/property/<id>/hide` | Скрыть объявление |
| `POST /admin/property/<id>/delete` | Удалить объявление |
| `POST /admin/review/<id>/delete` | Удалить отзыв |

### Профиль и пользовательские страницы
| Маршрут | Описание |
|---|---|
| `GET/POST /profile` | Редактирование профиля |
| `GET /favorites` | Избранное (арендатор) |
| `GET /my-requests` | Мои заявки (арендатор) |

---

## Учётные записи для тестирования

| Роль | Email | Пароль |
|---|---|---|
| Администратор | `admin@renta.ru` | `admin123` |
| Арендодатель | `landlord1@renta.ru` | `landlord123` |
| Арендатор | `tenant1@renta.ru` | `tenant123` |

---

## Разработка

- При запуске через `python run.py` сервер работает в режиме **debug** с автоматической перезагрузкой.
- Шаблоны используют наследование от `base.html`, который включает навбар, футер и flash-сообщения.
- Загруженные изображения обрабатываются через Pillow: ресайз до 1200×1200, оптимизация JPEG с качеством 85.