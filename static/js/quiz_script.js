document.addEventListener('DOMContentLoaded', function () {
    const quizForm = document.querySelector('#quiz-form');  // Using the specific ID
    console.log('Form:', quizForm);
    console.log('Quiz id:', quizId);

    if (!quizForm) {
        console.log('No quiz form found');
        return;
    }

    quizForm.addEventListener('change', function (event) {
        console.log('Change event triggered on form:', event.target);
        if (event.target.matches('.ajax-save')) {
            const questionId = event.target.getAttribute('data-question-id');
            const value = event.target.value;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            console.log('Data to save:', {questionId, value, quizId});

            fetch('/save-answer/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    question_id: questionId,
                    answer: value,
                    quiz_id: quizId
                })
            }).then(response => response.json())
                .then(data => {
                    console.log('Answer saved:', data);
                }).catch(error => console.log('Error saving answer:', error));
        }
    });
});