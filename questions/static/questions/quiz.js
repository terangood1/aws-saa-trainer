const quizForm = document.querySelector('#quiz-form');
const requiredCount = Number(quizForm.dataset.requiredCount);
const submitButton = quizForm.querySelector('button[type="submit"]');

function selectedCount() {
    return quizForm.querySelectorAll('input[name="answers"]:checked').length;
}

function updateSubmitButton() {
    submitButton.disabled = requiredCount < 1 || selectedCount() !== requiredCount;
}

quizForm.addEventListener('change', (event) => {
    const input = event.target;
    if (input.type === 'checkbox' && input.checked && selectedCount() > requiredCount) {
        input.checked = false;
    }
    updateSubmitButton();
});

quizForm.addEventListener('submit', (event) => {
    if (submitButton.disabled) {
        event.preventDefault();
    }
});

window.addEventListener('pageshow', updateSubmitButton);
updateSubmitButton();
