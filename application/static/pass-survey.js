// Bootstrap validation
(function () {
    const forms = document.querySelectorAll('.needs-validation')

    Array.prototype.slice.call(forms).forEach(form => form.addEventListener('submit', event => {
        if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
        }

        form.classList.add('was-validated')
    }, false))
})()


const $requiredCheckboxGroupFieldsets = document.querySelectorAll('fieldset[data-fieldset-type="checkbox-group"][data-required]')

// Проверка, что выбран хотя бы один вариант в обязательных вопросах с выбором нескольких вариантов
$requiredCheckboxGroupFieldsets.forEach(fieldset => {
    const $checkboxes = fieldset.querySelectorAll('input[type="checkbox"]')
    $checkboxes.forEach(checkbox => checkbox.addEventListener('change', e => {
        if (e.target.checked) {
            $checkboxes.forEach(c => c.required = false)
        } else {
            const $otherCheckboxes = Array.from($checkboxes).filter(c => c !== checkbox)
            if ($otherCheckboxes.every(c => !c.checked)) {
                $checkboxes.forEach(c => c.required = true)
            }
        }
    }))
})


const $surveyForm = document.querySelector('#surveyForm')

class SurveyResult {
    constructor(surveyForm) {
        this.result = this.#assembleResult(surveyForm)
    }

    #assembleResult(surveyForm) {
        const answerGroups = Array.from(surveyForm.querySelectorAll('div[data-group-type="answer"]'))
        return {answers: this.#getAnswers(answerGroups)}
    }

    #getAnswers(answerGroups) {
        const answers = []
        answerGroups.forEach(answerGroup => answers.push(this.#assembleAnswer(answerGroup)))
        return answers
    }

    #assembleAnswer(answerGroup) {
        const questionTitle = answerGroup.querySelector('span[data-span-type="question-title"]').innerText
        const questionType = answerGroup.dataset.questionType
        const questionRequired = answerGroup.dataset.questionRequired.toLowerCase() === 'true'

        const answer = {questionTitle, questionType, questionRequired}

        if (questionType === 'text') {
            answer.answer = answerGroup.querySelector('input[data-input-type="answer"]').value
        } else if (['radio', 'checkbox'].includes(questionType)) {
            const $answerOptions = Array.from(answerGroup.querySelectorAll('input[data-input-type="answer-option"]'))
            answer.answerOptions = $answerOptions.map(o => o.value)

            answer.answer = questionType === 'radio' ? $answerOptions.find(o => o.checked)?.value || '' : $answerOptions.filter(o => o.checked).map(o => o.value) || []
        }

        return answer
    }

    async submit(url = $surveyForm.action) {
        try {
            return await fetch(url, {
                method: $surveyForm.method || 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(this.result)
            })
        } catch (e) {
            console.error(e)
        }
        return {}
    }
}

$surveyForm?.addEventListener('submit', async e => {
    e.preventDefault()

    if ($surveyForm.checkValidity()) {
        const result = new SurveyResult($surveyForm)
        const res = await result.submit()

        if (res.redirected) {
            window.location.href = res.url
        }
    }
})

const result = {
    questions: [
        {
            title: 'question title',
            type: 'text',
            isRequired: true,
            answer: 'shdfjh'
        },
        {
            title: 'question title',
            type: 'radio',
            isRequired: true,
            answerOptions: ['sdf', 'sdf', 'sdf'],
            answer: 'sdf'
        },
        {
            title: 'question title',
            type: 'checkbox',
            isRequired: true,
            answerOptions: ['sdf', 'sdf', 'sdf'],
            answer: ['sdf', 'sdf']
        }
    ]
}