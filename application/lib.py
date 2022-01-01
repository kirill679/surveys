from application import generate_password_hash, check_password_hash, User, db, session, EmailNotFoundException, \
    PasswordIncorrectException, Survey, Email, json, uuid, SurveyResult, url_for, pytz


# Сохранить администратора в бд
def save_admin(form):
    try:
        name = form.name.data
        email = form.email.data
        password = generate_password_hash(form.password.data)

        user = User(name=name, email=email, password=password, is_admin=True)
        db.session.add(user)
        db.session.commit()

        return True
    except:
        db.session.rollback()

        return False


# Получить список всех администраторов
def get_all_admins():
    try:
        admins = User.query.filter_by(is_admin=True).order_by(User.id.desc()).all()
        return admins
    except:
        return []


# Проверить, является ли пользователь администратором
def check_user_is_admin(id):
    user = User.query.filter_by(id=id).first()
    return user.is_admin


# Удалить пользователя
def delete_user(id):
    try:
        User.query.filter_by(id=id).delete()
        db.session.commit()
        return True
    except:
        return False


# Проверить данные для входа в аккаунт
def check_credentials(form):
    email = form['email']
    password = form['password']

    user = User.query.filter_by(email=email).first()

    if user:
        password_hash = user.password

        if check_password_hash(password_hash, password):
            session['is_logged_in'] = True
            session['is_admin'] = user.is_admin
            session['name'] = user.name

            return True
        else:
            raise PasswordIncorrectException('Неверный пароль')
    else:
        raise EmailNotFoundException('Пользователь с таким email не найден')


# Получить список всех пользователей
def get_all_users():
    return User.query.filter_by(is_admin=False).all()


# Получить всех пользователей с результатами опросов
def get_all_users_with_result_ids():
    return User.query.filter_by(is_admin=False).join(SurveyResult).order_by(User.id.desc()).all()


# Преобразовать пользователей для вывода
def transform_users_for_admin(users):
    def transform_user(user):
        user.survey_result_link = get_survey_result_link(user.survey_result_id)
        user.survey_result_title = get_survey_result_title(user.survey_result_id)
        user.formatted_register_date = convert_date_for_template(user.register_date)
        return user

    return list(map(transform_user, users))


# Преобразовать администраторов для вывода
def transform_admins_for_admin(admins):
    def transform_admin(admin):
        admin.formatted_register_date = convert_date_for_template(admin.register_date)
        return admin

    return list(map(transform_admin, admins))


# Получить ссылку на результат опроса
def get_survey_result_link(survey_result_id):
    return url_for('survey_result', id=survey_result_id, _external=True)


# Получить название опроса
def get_survey_result_title(survey_result_id):
    survey_result = json.loads(SurveyResult.query.filter_by(id=survey_result_id).first().result)
    return survey_result['surveyTitle']


# Сохранить опрос в БД
def save_survey(survey_json):
    try:
        title = survey_json['title']
        is_available = survey_json['isAvailable']
        emails = survey_json['emails']

        survey = json.dumps({'questions': survey_json['questions']})

        survey = Survey(title=title, is_available=is_available, survey=survey)
        db.session.add(survey)
        db.session.commit()

        survey_id = survey.id

        for email in emails:
            email = Email(email=email, survey_id=survey_id)
            db.session.add(email)

        db.session.commit()
    except:
        db.session.rollback()


# Сохранить изменения в опросе
def update_survey(survey_id, survey_json):
    title = survey_json['title']
    is_available = survey_json['isAvailable']
    emails = survey_json['emails']

    survey = json.dumps({'questions': survey_json['questions']})

    Survey.query.filter_by(id=survey_id).update({
        'title': title,
        'is_available': is_available,
        'survey': survey
    })

    Email.query.filter_by(survey_id=survey_id).delete()

    for email in emails:
        email = Email(email=email, survey_id=survey_id)
        db.session.add(email)

    db.session.commit()


# Получить все опросы
def get_all_surveys():
    surveys = Survey.query.with_entities(Survey.id, Survey.title, Survey.is_available).order_by(
        Survey.is_available.desc()).all()
    return surveys


# Получить опрос
def get_survey_by_id(id):
    survey_from_db = Survey.query.filter_by(id=id).first()

    survey = {
        'title': survey_from_db.title,
        'questions': get_questions_from_survey(survey_from_db.survey),
        'emails': get_emails_for_survey(id),
        'is_available': survey_from_db.is_available
    }

    return survey


# Преобразовать опрос для вывода на странице редактирования
def transform_survey_for_edit(survey: dict):
    question_types_map = {
        'text': 'Свободный ответ',
        'radio': 'Выбрать один',
        'checkbox': 'Выбрать несколько'
    }

    def transform_question(question):
        question['label'] = question_types_map[question['type']]
        return question

    questions = list(map(transform_question, survey['questions']))
    survey.update({'questions': questions})

    return survey


# Преобразовать опрос для прохождения
def transform_survey_for_pass(survey):
    types_labels_map = {
        'text': 'Введите свой ответ',
        'radio': 'Выберите один вариант',
        'checkbox': 'Выберите несколько вариантов'
    }

    types_errors_map = {
        'tel': 'Пожалуйста, введите корректный телефон',
        'email': 'Пожалуйста, введите корректный email',
        'string': 'Пожалуйста, введите свой ответ',
        'radio': 'Пожалуйста, выберите один из вариантов',
        'checkbox': 'Пожалуйста, выберите один или несколько вариантов'
    }

    text_types_map = {
        'tel': 'tel',
        'email': 'email',
        'string': 'text'
    }

    def transform_question(question):
        question['label'] = types_labels_map[question['type']]

        if question['type'] == 'text':
            error_message = types_errors_map[question['validateAs']]
            question['type'] = text_types_map[question['validateAs']]
        else:
            error_message = types_errors_map[question['type']]

        if question['type'] == 'tel':
            question['pattern'] = '[0-9]{1}-[0-9]{3}-[0-9]{3}-[0-9]{4}'

        question['errorMessage'] = error_message
        question['id'] = uuid.uuid4()

        return question

    questions = list(map(transform_question, survey['questions']))
    survey.update({'questions': questions})

    return survey


# Проверить, доступен ли опрос для прохождения
def check_survey_availability(id):
    survey = Survey.query.filter_by(id=id).first()

    if survey:
        return survey.is_available
    else:
        return False


# Получить все email участников данного опроса
def get_emails_for_survey(survey_id):
    survey = Survey.query.filter_by(id=survey_id).first()
    return list(map(lambda e: e.email, survey.emails))


# Получить массив вопросов из JSON документа
def get_questions_from_survey(survey_json):
    survey = json.loads(survey_json)
    return survey['questions']


# Удалить опрос
def delete_survey_by_id(id):
    Survey.query.filter_by(id=id).delete()
    db.session.commit()


# Проверить, есть ли email среди участников опроса
def check_survey_access(survey_id, email):
    survey = Survey.query.filter_by(id=survey_id).first()
    if survey:
        allowed_emails = list(map(lambda e: e.email, survey.emails))

        return True if email in allowed_emails else False

    return False


# Проверить, существует ли опрос
def check_survey_existence(id):
    survey = Survey.query.filter_by(id=id).first()
    return True if survey else False


# Сохранить результат опроса
def save_survey_result(survey_id, survey_result):
    try:
        survey = get_survey_by_id(survey_id)

        survey_title = survey['title']
        survey_result['surveyTitle'] = survey_title

        survey_result_json = json.dumps(survey_result)

        result = SurveyResult(result=survey_result_json)
        db.session.add(result)
        db.session.commit()

        return result.id
    except:
        db.session.rollback()


# Получить результат опроса
def get_survey_result_by_id(id):
    return SurveyResult.query.filter_by(id=id).first()


# Разрешить регистрацию пользователю
def allow_registration(survey_result_id):
    session['survey_result_id'] = survey_result_id
    session['allow_registration'] = True


# Сохранить пользователя в БД
def save_user(form):
    try:
        name = form.name.data
        email = form.email.data
        password = generate_password_hash(form.password.data)
        survey_result_id = session['survey_result_id']

        user = User(name=name, email=email, password=password, survey_result_id=survey_result_id)
        db.session.add(user)
        db.session.commit()

        return True
    except:
        db.session.rollback()
        return False


# Проверить, что email свободен
def check_email_is_free(email):
    user = User.query.filter_by(email=email).first()
    return False if user else True


# Преобразовать дату в нужную временную зону
def convert_date_for_template(date):
    timezone = pytz.timezone('Europe/Moscow')
    offset = timezone.utcoffset(date)
    date += offset

    return date


# Преобразовать json результата опроса
def parse_result_from_survey_result(survey_result):
    return json.loads(survey_result.result)
