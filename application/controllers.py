from application import app, render_template, RegisterForm, request, flash, redirect, url_for, lib, session, \
    EmailNotFoundException, PasswordIncorrectException, LoginForm, SurveyRedirectForm, wraps


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Пожалуйста, войдите в аккаунт', 'danger')
            return redirect(url_for('login'))

    return wrap


def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return f(*args, **kwargs)
        else:
            flash('Вы уже вошли в аккаунт', 'success')
            return redirect(url_for('home'))

    return wrap


def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session.get('is_admin'):
            return f(*args, **kwargs)
        else:
            flash('Для этого действия необходимо быть администратором', 'danger')
            return redirect(url_for('login'))

    return wrap


# Главная
@app.route('/')
def home():
    return render_template('home.html')


# Информация
@app.route('/about')
def about():
    return render_template('about.html')


# Панель управления
@app.route('/dashboard')
@is_admin
def dashboard():
    return render_template('dashboard.html')


# Список всех администраторов
@app.route('/admins')
@is_admin
def all_admins():
    admins = lib.get_all_admins()
    admins = lib.transform_admins_for_admin(admins)

    if admins:
        return render_template('admins.html', admins=admins)
    else:
        msg = 'Администраторы не найдены'
        return render_template('admins.html', msg=msg)


# Регистрация нового администратора
@app.route('/register_admin', methods=['GET', 'POST'])
@is_admin
def register_admin():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        if lib.save_admin(form):
            flash('Администратор успешно зарегистрирован', 'success')
            return redirect(url_for('dashboard'))
        else:
            error = 'Ошибка при регистрации администратора'
            return render_template('register_admin.html', error=error, form=form)

    return render_template('register_admin.html', form=form)


# Удаление администратора
@app.route('/delete_user/<string:id>', methods=['POST'])
@is_admin
def delete_user_route(id):
    if lib.check_user_is_admin(id):
        url = url_for('all_admins')
        user_category = 'Администратор'
    else:
        url = url_for('users')
        user_category = 'Пользователь'

    if lib.delete_user(id):
        flash(f'{user_category} удален', 'success')
        return redirect(url)

    else:
        flash('Ошибка при удалении', 'danger')
        return redirect(url)


# Все пользователи
@app.route('/users')
@is_admin
def users():
    users = lib.get_all_users_with_result_ids()
    users = lib.transform_users_for_admin(users)

    print(list(users))

    if users:
        return render_template('users.html', users=users)
    else:
        msg = 'Пользователи не найдены'
        return render_template('users.html', msg=msg)


# Создание опроса
@app.route('/add_survey', methods=['GET', 'POST'])
@is_admin
def add_survey():
    if request.method == 'POST':
        survey_json = request.json
        lib.save_survey(survey_json)
        return redirect(url_for('all_surveys'))

    return render_template('add_survey.html')


# Список всех опросов
@app.route('/surveys')
@is_admin
def all_surveys():
    surveys = lib.get_all_surveys()

    if surveys:
        return render_template('surveys.html', surveys=surveys)
    else:
        msg = 'Опросы не найдены'
        return render_template('surveys.html', msg=msg)


# Редактирование опроса
@app.route('/edit-survey/<string:id>', methods=['GET', 'POST'])
@is_admin
def edit_survey(id):
    survey = lib.get_survey_by_id(id)
    survey = lib.transform_survey_for_edit(survey)

    if request.method == 'POST':
        survey_json = request.json
        lib.update_survey(id, survey_json)
        return redirect(url_for('all_surveys'))

    return render_template('edit_survey.html', survey=survey)


# Удаление опроса
@app.route('/delete-survey/<string:id>', methods=['POST'])
@is_admin
def delete_survey_and_emails(id):
    lib.delete_survey_by_id(id)

    flash('Опрос удален', 'success')
    return redirect(url_for('all_surveys'))


# Регистрация пользователя
@app.route('/register', methods=['GET', 'POST'])
@not_logged_in
def register():
    if session.get('allow_registration'):
        form = RegisterForm(request.form)
    else:
        form = SurveyRedirectForm(request.form)

    if request.method == 'POST' and form.validate():
        if lib.save_user(form):
            session.pop('allow_registration')
            session.pop('allowed_survey')

            flash('Вы успешно зарегистрировались, можете войти в аккаунт', 'success')
            return redirect(url_for('login'))
        else:
            error = 'Ошибка при регистрации, попробуйте очистить куки'
            return render_template('register.html', error=error, form=form)

    return render_template('register.html', form=form)


# Вход в аккаунт
@app.route('/login', methods=['GET', 'POST'])
@not_logged_in
def login():
    form = LoginForm(request.form)

    if request.method == 'POST':
        try:
            lib.check_credentials(request.form)
            session['logged_in'] = True

            flash('Вы вошли в аккаунт', 'success')

            if session['is_admin']:
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('home'))

        except EmailNotFoundException as error:
            return render_template('login.html', error=error, form=form)
        except PasswordIncorrectException as error:
            return render_template('login.html', error=error, form=form)

    return render_template('login.html', form=form)


# Прохождение опроса
@app.route('/survey/<string:id>', methods=['GET', 'POST'])
@not_logged_in
def survey(id):
    if request.method == 'POST':
        survey_result = request.json
        survey_result_id = lib.save_survey_result(id, survey_result)
        lib.allow_registration(survey_result_id)
        flash('Вы успешно прошли опрос, теперь можно зарегистрироваться', 'success')
        return redirect(url_for('register'))

    if not lib.check_survey_availability(id):
        flash('Данный опрос недоступен для прохождения', 'danger')
        return redirect(url_for('home'))

    if session.get('allowed_survey') == id:
        survey = lib.get_survey_by_id(id)
        survey = lib.transform_survey_for_pass(survey)

        return render_template('survey.html', survey_id=id, survey=survey)
    else:
        return render_template('survey.html', survey_id=id)


# Проверка доступа к опросу
@app.route('/survey-access', methods=['POST'])
@not_logged_in
def survey_access():
    survey_id = request.form.get('survey_id')
    email = request.form.get('email')

    if lib.check_survey_access(survey_id, email):
        session['allowed_survey'] = survey_id
        return redirect(request.referrer)
    else:
        flash('Такого email нет в списке', 'danger')
        return redirect(request.referrer)


# Перенаправление на опрос
@app.route('/survey-redirect', methods=['POST'])
@not_logged_in
def survey_redirect():
    form = SurveyRedirectForm(request.form)

    if form.validate():
        survey_id = form.survey_id.data
        survey = lib.check_survey_existence(survey_id)

        if survey:
            return redirect(url_for('survey', id=survey_id))
        else:
            flash('Такого опроса нет', 'danger')
            return redirect(request.referrer)
    else:
        return redirect(request.referrer)


# Результат прохождения опроса
@app.route('/survey-result/<string:id>')
@is_admin
def survey_result(id):
    survey_result = lib.get_survey_result_by_id(id)
    result = lib.parse_result_from_survey_result(survey_result)
    user = survey_result.user[0]
    date = lib.convert_date_for_template(survey_result.date)

    return render_template('survey_result.html', result=result, user=user, date=date)


# Выход из аккаунта
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('login'))
