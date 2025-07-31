//socre.js
//점수 계산 로직 구현


// 사용자 답변 저장 배열
let userAnswers = JSON.parse(localStorage.getItem('userAnswers')) || {};

// 최종 점수를 저장할 객체
let finalScores = JSON.parse(localStorage.getItem('finalScores')) || {
    "공연": 0,
    "봉사": 0,
    "사회": 0,
    "학술": 0,
    "예창": 0, 
    "체육": 0
};


document.addEventListener('DOMContentLoaded', () => {
    const questionId = document.body.dataset.questionId;
    const questionIndex = parseInt(document.body.dataset.questionIndex || '1') - 1; 
    const optionButtons = document.querySelectorAll('.option-btn');
    const totalQuestions = quizData.length; 

    //선택지 개수가 6개일때 2*3으로 레이아웃 변경
    const optionsContainer = document.querySelector('.options');
    if (optionsContainer) {
        if (optionButtons.length == 6) {
            optionsContainer.classList.add('grid-2x3');
        } 
    }

    // 페이지 로드 시 현재 질문의 점(dot) 활성화
    const dots = document.querySelectorAll('.question-indicator .dot');
    if (dots.length > 0 && questionIndex >= 0 && questionIndex < dots.length) {
        dots.forEach(dot => dot.classList.remove('active'));
        dots[questionIndex].classList.add('active');
    }

    // 각 답변 버튼에 클릭 이벤트 리스너 추가
    optionButtons.forEach(button => {
        button.addEventListener('click', () => {
            // 모든 버튼에서 selected 클래스 제거
            optionButtons.forEach(btn => btn.classList.remove('selected'));
            // 클릭된 버튼에 selected 클래스 추가
            button.classList.add('selected');

            const selectedOptionIndex = parseInt(button.dataset.optionIndex);
            const previousAnswerIndex = userAnswers[questionId];

            const currentQuestionData = quizData.find(q => q.id === questionId);

            // 이전 답변의 점수를 제거
            if (previousAnswerIndex !== undefined && currentQuestionData) {
                const previousWeights = currentQuestionData.weights[previousAnswerIndex];
                for (const category in previousWeights) {
                    finalScores[category] -= previousWeights[category];
                }
            }

            // 새로운 답변의 점수를 추가
            if (currentQuestionData && currentQuestionData.weights[selectedOptionIndex]) {
                const newWeights = currentQuestionData.weights[selectedOptionIndex];
                for (const category in newWeights) {
                    finalScores[category] = (finalScores[category] || 0) + newWeights[category];
                }
            }

            userAnswers[questionId] = selectedOptionIndex;
            localStorage.setItem('userAnswers', JSON.stringify(userAnswers));
            localStorage.setItem('finalScores', JSON.stringify(finalScores));

            console.log(`[${questionId}] 선택: ${selectedOptionIndex}`);
            console.log("업데이트된 최종 점수:", finalScores);


            // 다음 페이지로 이동
            setTimeout(() => {
                if (questionIndex < totalQuestions - 1) {
                    // 다음 질문 페이지로 이동
                    const nextQuestionFileName = `question_${questionIndex + 2}.html`;
                    window.location.href = `/templates/${nextQuestionFileName}`;
                } else {
                    // 마지막 질문이라면 결과 선택 페이지로 이동
                    window.location.href = '/templates/result_choice.html';
                }
            }, 300); // 0.3초 후 이동
        });
    });
});


