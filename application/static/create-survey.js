const $surveyForm = document.querySelector('#surveyForm')
const $addQuestionButtons = document.querySelectorAll('button[data-button-type="add-question"]')
const $textQuestionTemplate = document.querySelector('#textQuestion')
const $radioQuestionTemplate = document.querySelector('#radioQuestion')
const $checkboxQuestionTemplate = document.querySelector('#checkboxQuestion')
const $questionOptionTemplate = document.querySelector('#questionOption')
const $emailInput = document.querySelector('#emailInput')
const $addParticipantEmailButton = document.querySelector('#addParticipantEmailButton')
const $saveSurveyButton = document.querySelector('#saveSurveyButton')
const $participantEmails = document.querySelector('#participantEmails')
const $emailBadgeTemplate = document.querySelector('#emailBadge')
const $participantEmailsPlaceholder = document.querySelector('#participantEmailsPlaceholder')
const $isAvailableSurvey = document.querySelector('#isAvailable')
const $addQuestionOptionButtons = document.querySelectorAll('button[data-button-type="add-question-option"]')
const $removeEmailButtons = document.querySelectorAll('button[data-button-type="remove-email"]')
const $removeQuestionButtons = document.querySelectorAll('button[data-button-type="remove-question"]')
const $removeQuestionOptionsButtons = document.querySelectorAll('button[data-button-type="remove-question-option"]')

class Survey {
    constructor(form) {
        this.survey = this.#assembleSurvey(form)
    }

    // Собрать опрос
    #assembleSurvey(form) {
        // Группы input, которые относятся к одному вопросу
        const questionsGroups = Array.from(form.querySelectorAll('.form-group[data-group-type="question"]'))

        const title = form.querySelector('#surveyTitleInput').value || 'Новый опрос'
        const questions = this.#getQuestions(questionsGroups)
        const emails = this.#getEmails()
        const isAvailable = $isAvailableSurvey.checked

        return {title, questions, emails, isAvailable}
    }

    // Собрать вопрос из группы input
    #assembleQuestion(inputsGroup) {
        const question = {}

        const $questionTitleInput = inputsGroup.querySelector('input[data-input-type="question-title"]')
        const $questionIsRequiredInput = inputsGroup.querySelector('input[data-input-type="question-required"]')


        question.title = $questionTitleInput.value
        question.type = $questionTitleInput.dataset.questionType
        question.isRequired = $questionIsRequiredInput.checked

        // Если вопрос с вариантами ответа
        if (['radio', 'checkbox'].includes(question.type)) {
            question.answerOptions = []

            // Варианты ответа
            const options = Array.from(inputsGroup.querySelectorAll('input[data-input-type="question-option"]'))
                .map(optEl => optEl.value)

            options.forEach(o => question.answerOptions.push(o))
        }

        // Если вопрос с вводом пользователя
        if (question.type === 'text') {
            question.validateAs = inputsGroup.querySelector('select[data-select-type="validate-as"]').value || 'string'
        }

        return question
    }

    // Получить массив вопросов
    #getQuestions(questionsGroups) {
        const questions = []

        questionsGroups.forEach(group => {
            const question = this.#assembleQuestion(group)
            questions.push(question)
        })

        return questions
    }

    // Получить массив email участников
    #getEmails() {
        const $emailSpans = $participantEmails.querySelectorAll('span[data-span-type="email"]')
        return Array.from($emailSpans).map(emailSpan => emailSpan.innerText)
    }

    // Отправить опрос
    async submit(url = window.location.href) {
        try {
            return await fetch(url, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(this.survey)
            })
        } catch (e) {
            console.error(e)
        }
    }
}

const addQuestion = e => {
    const $button = e.target

    const templatesTypesMap = {
        text: $textQuestionTemplate,
        radio: $radioQuestionTemplate,
        checkbox: $checkboxQuestionTemplate
    }

    const questionType = $button.dataset.buttonCreatedQuestionType

    const $template = templatesTypesMap[questionType].content.cloneNode(true)

    const $removeQuestionButton = $template.querySelector('button[data-button-type="remove-question"]')
    $removeQuestionButton.addEventListener('click', removeQuestion)

    // Кнопка добавления варианта ответа
    const $addQuestionOptionButton = $template.querySelector('button[data-button-type="add-question-option"]')

    // Проверка, что это вопрос с вариантами ответа
    if ($addQuestionOptionButton) {
        const $removeQuestionOptionButtons = $template.querySelectorAll('button[data-button-type="remove-question-option"]')

        $removeQuestionOptionButtons.forEach(button => button.addEventListener('click', removeQuestionOption))
        $addQuestionOptionButton.addEventListener('click', addQuestionOption)
    }

    // Кнопка создания вопроса в форме
    const $openModalButton = $surveyForm.querySelector('button[data-button-type="open-add-question-modal"]')

    // Элемент перед которым добавляются вопросы
    const $beforeEl = $openModalButton.parentElement

    // Элемент в который добавляются вопросы
    const $inEl = $openModalButton.parentElement.parentElement

    $inEl.insertBefore($template, $beforeEl)
}

const removeQuestion = e => {
    const $questionEl = e.target.parentElement.parentElement
    $questionEl.remove()
}

const addQuestionOption = e => {
    // Элемент вопроса целиком
    const $questionEl = e.target.parentElement

    const $addQuestionOptionButton = e.target

    // Шаблон варианта ответа
    const $optionTemplate = $questionOptionTemplate.content.cloneNode(true)

    // Кнопка для удаления этого варианта
    const $removeQuestionOptionButton = $optionTemplate.querySelector('button[data-button-type="remove-question-option"]')
    $removeQuestionOptionButton.addEventListener('click', removeQuestionOption)

    // Вставить новый вариант перед кнопкой добавления варианта
    $questionEl.insertBefore($optionTemplate, $addQuestionOptionButton)
}

const removeQuestionOption = e => {
    // Вариант ответа, который нужно удалить
    const $answerOption = e.target.parentElement
    $answerOption.remove()
}

const addParticipantEmailHandler = e => {
    e.preventDefault()

    if (e.type === 'keyup') {
        if (e.key === 'Enter') {
            addParticipantEmail(e)
        }
    } else if (e.type === 'click') {
        addParticipantEmail(e)
    }
}

const addParticipantEmail = e => {
    const newEmail = $emailInput.value.trim().toLowerCase()

    const $placeholder = $participantEmails.querySelector('label[data-span-type="placeholder"]')
    if ($placeholder) {
        $placeholder.remove()
    }

    const $emailBadge = $emailBadgeTemplate.content.cloneNode(true)
    const $emailBadeTitle = $emailBadge.querySelector('span[data-span-type="email"]')
    $emailBadeTitle.innerText = newEmail

    const $removeEmailButton = $emailBadge.querySelector('button[data-button-type="remove-email"]')
    $removeEmailButton.addEventListener('click', removeParticipantEmail)

    $participantEmails.appendChild($emailBadge)

    // Очистить input
    e.target.type === 'button'
        ? e.target.parentElement.querySelector('#emailInput').value = ''
        : e.target.value = ''
}

const removeParticipantEmail = e => {
    const $emailBadge = e.target.parentElement
    $emailBadge.remove()

    // Если все теги удалены, добавить заполнитель
    if ($participantEmails.innerHTML.trim() === '') {
        const $placeholder = $participantEmailsPlaceholder.content.cloneNode(true)
        $participantEmails.appendChild($placeholder)
    }
}


$addQuestionButtons.forEach(button => button.addEventListener('click', addQuestion))
$addQuestionOptionButtons.forEach(button => button.addEventListener('click', addQuestionOption))
$removeEmailButtons.forEach(button => button.addEventListener('click', removeParticipantEmail))
$removeQuestionButtons.forEach(button => button.addEventListener('click', removeQuestion))
$removeQuestionOptionsButtons.forEach(button => button.addEventListener('click', removeQuestionOption))

$emailInput.addEventListener('keyup', addParticipantEmailHandler)
$addParticipantEmailButton.addEventListener('click', addParticipantEmailHandler)

$saveSurveyButton.addEventListener('click', async () => {
    const survey = new Survey($surveyForm)
    const res = await survey.submit()
    if (res.redirected) {
        window.location.href = res.url
    }
})