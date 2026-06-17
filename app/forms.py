from flask_wtf import FlaskForm
from wtforms import (
    FileField,
    FloatField,
    HiddenField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    Optional,
)


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    name = StringField("Имя", validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField(
        "Подтверждение пароля", validators=[DataRequired(), EqualTo("password")]
    )
    role = SelectField(
        "Роль", choices=[("tenant", "Арендатор"), ("landlord", "Арендодатель")]
    )
    submit = SubmitField("Зарегистрироваться")


class ProfileForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField("Телефон", validators=[Optional(), Length(max=20)])
    avatar = FileField("Аватар")
    submit = SubmitField("Сохранить")


class PropertyForm(FlaskForm):
    title = StringField("Заголовок", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Описание", validators=[DataRequired()])
    price = IntegerField("Цена", validators=[DataRequired(), NumberRange(min=1)])
    price_type = SelectField(
        "Тип оплаты",
        choices=[("month", "в месяц"), ("day", "в сутки"), ("bed", "койко-место")],
    )
    property_type = SelectField(
        "Тип жилья",
        choices=[("apartment", "Квартира"), ("house", "Дом"), ("room", "Комната")],
    )
    city = StringField("Город", validators=[DataRequired(), Length(max=100)])
    address = StringField("Адрес", validators=[DataRequired(), Length(max=255)])
    rooms = IntegerField("Количество комнат", validators=[Optional()])
    area = FloatField("Площадь (м²)", validators=[Optional()])
    floor = IntegerField("Этаж", validators=[Optional()])
    max_floor = IntegerField("Всего этажей", validators=[Optional()])
    lat = FloatField("Широта", validators=[Optional()])
    lng = FloatField("Долгота", validators=[Optional()])
    images = FileField("Фотографии (можно выбрать несколько)")
    submit = SubmitField("Сохранить")


class RequestForm(FlaskForm):
    message = TextAreaField(
        "Сообщение арендодателю", validators=[Optional(), Length(max=500)]
    )
    submit = SubmitField("Отправить заявку")


class ReviewForm(FlaskForm):
    rating = SelectField(
        "Оценка", choices=[(5, "5"), (4, "4"), (3, "3"), (2, "2"), (1, "1")], coerce=int
    )
    text = TextAreaField("Отзыв", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Оставить отзыв")
