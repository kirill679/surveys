from application import db


# Опросы
class Survey(db.Model):
    __tablename__ = 'surveys'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    is_available = db.Column(db.Boolean, nullable=False, default=False)
    survey = db.Column(db.JSON, nullable=False)
    emails = db.relationship('Email', backref='survey', cascade='all, delete')


# Email для доступа к опросам
class Email(db.Model):
    __tablename__ = 'emails'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id', ondelete='CASCADE'), nullable=False)


# Результаты опросов
class SurveyResult(db.Model):
    __tablename__ = 'survey_results'

    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.JSON, nullable=False)
    date = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    user = db.relationship('User', backref='survey_result', cascade='all, delete')


# Зарегистрированные пользователи и администраторы
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    survey_result_id = db.Column(db.Integer, db.ForeignKey('survey_results.id', ondelete='CASCADE'), nullable=True,
                                 default=None)
    register_date = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
