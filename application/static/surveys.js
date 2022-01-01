const $copySurveyLinkButtons = document.querySelectorAll('button[data-button-type="copy-link"]')
const $copySuccessAlertTemplate = document.querySelector('#copySuccessAlertTemplate')
const $alertFrame = document.querySelector('#alertFrame')

// Копирование ссылки на опрос
$copySurveyLinkButtons.forEach(button => button.addEventListener('click', async e => {
    const link = e.target.dataset.surveyLink
    await navigator.clipboard.writeText(link)

    document.querySelector('#copySuccessAlert')?.remove()

    const $alert = $copySuccessAlertTemplate.content.cloneNode(true)
    $alertFrame.appendChild($alert)
}))