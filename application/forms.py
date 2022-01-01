import application
from application import Form, StringField, PasswordField, DataRequired, Length, Email, ValidationError, IntegerField


class RegisterForm(Form):
    name = StringField('Имя', validators=[
        DataRequired(message='Введите имя'),
        Length(min=1, max=50, message='Максимальная длина имени - 50 символов')
    ], description='Ваше имя')
    email = StringField('Email', validators=[
        DataRequired(message='Введите email'),
        Length(min=1, max=50, message='Максимальная длина email - 50 символов'),
        Email(message='Некорректный email')
    ], description='Ваш email')
    password = PasswordField('Пароль (не менее 6 символов)', validators=[
        DataRequired(message='Введите пароль'),
        Length(min=6, max=30, message='Допустимая длина пароля - от 6 до 30 символов')
    ], description='Ваш пароль')

    @staticmethod
    def validate_email(self, field):
        if not application.lib.check_email_is_free(field.data):
            raise ValidationError('Пользователь с таким email уже существует')


class LoginForm(Form):
    email = StringField('Email', validators=[
        DataRequired(message='Введите email'),
        Email(message='Некорректный email')
    ], description='Ваш email')
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Введите пароль'),
    ], description='Ваш пароль')


class SurveyRedirectForm(Form):
    survey_id = IntegerField('Введите номер опроса', validators=[
        DataRequired(message='Введите номер опроса'),
    ], description='Номер опроса')
