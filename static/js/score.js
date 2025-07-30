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

    // 페이지 로드 시 현재 질문의 점(dot) 활성화
    const dots = document.querySelectorAll('.question-indicator .dot');
    if (dots.length > 0 && questionIndex >= 0 && questionIndex < dots.length) {
        dots.forEach(dot => dot.classList.remove('active'));
        dots[questionIndex].classList.add('active');
    }

    // 이전에 선택된 답변이 있다면 해당 버튼에 'selected' 클래스 추가
    if (userAnswers[questionId] !== undefined) {
        const selectedIndex = userAnswers[questionId];
        if (optionButtons[selectedIndex]) {
            optionButtons[selectedIndex].classList.add('selected');
        }
    }

    // 각 답변 버튼에 클릭 이벤트 리스너 추가
    optionButtons.forEach(button => {
        button.addEventListener('click', () => {
            optionButtons.forEach(btn => btn.classList.remove('selected'));
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

            // 다음 페이지로 이동 로직
            setTimeout(() => {
                if (questionIndex < totalQuestions - 1) {
                    // 다음 질문 페이지로 이동
                    const nextQuestionFileName = `question_${questionIndex + 2}.html`;
                    window.location.href = `/templates/${nextQuestionFileName}`;
                } else {
                    // 마지막 질문이라면 결과 페이지로 이동
                    window.location.href = '/templates/result.html';
                }
            }, 300); // 0.3초 후 이동
        });
    });
});

// 결과 페이지 (result.html)에서 점수를 표시하는 함수
function displayResults() {
    const resultsContainer = document.getElementById('results-container');
    if (!resultsContainer) {
        console.error("결과 컨테이너를 찾을 수 없습니다.");
        return;
    }

    // 로컬 스토리지에서 최종 점수 불러오기
    const storedFinalScores = JSON.parse(localStorage.getItem('finalScores')) || {
        "공연": 0, "봉사": 0, "사회": 0, "학술": 0, "예창": 0, "체육": 0
    };

    let resultsHTML = '<h2 class="result-title">당신의 결과</h2>';
    resultsHTML += '<ul class="score-list">';
    for (const category in storedFinalScores) {
        resultsHTML += `<li>${category}: <span>${storedFinalScores[category]}</span>점</li>`;
    }
    resultsHTML += '</ul>';

    // 가장 높은 점수를 받은 카테고리 찾기
    let maxScore = -1;
    let topCategories = [];
    let allCategories = Object.keys(storedFinalScores);

    // 점수 합계가 0인 경우 (아무것도 선택 안 했을 때) 예외 처리
    const totalSum = Object.values(storedFinalScores).reduce((sum, score) => sum + score, 0);

    if (totalSum === 0) {
        resultsHTML += '<p class="no-result">아직 퀴즈를 완료하지 않았거나, 점수가 계산되지 않았습니다.</p>';
    } else {
        for (const category of allCategories) {
            const score = storedFinalScores[category];
            if (score > maxScore) {
                maxScore = score;
                topCategories = [category];
            } else if (score === maxScore && score > 0) { // 점수가 0이 아닌 동점일 경우
                topCategories.push(category);
            }
        }

        if (topCategories.length > 0) {
            resultsHTML += `<p class="top-category-text">가장 높은 점수를 받은 분야: <strong>${topCategories.join(', ')}</strong></p>`;
            // 각 분야에 대한 설명 추가
            resultsHTML += '<div class="category-descriptions">';
            topCategories.forEach(category => {
                resultsHTML += `<h3>${category} 분야 설명</h3>`;
                switch (category) {
                    case '공연':
                        resultsHTML += '<p>당신은 무대 위에서 빛나거나 창의적인 표현을 즐기는군요. 예술적 감각과 끼가 많습니다!</p>';
                        break;
                    case '봉사':
                        resultsHTML += '<p>타인을 돕고 공동체에 기여하는 데서 큰 만족감을 느낍니다. 따뜻한 마음을 가진 분이군요.</p>';
                        break;
                    case '사회':
                        resultsHTML += '<p>사회 문제에 관심이 많고, 사람들과 소통하며 관계를 형성하는 것을 중요하게 생각합니다.</p>';
                        break;
                    case '학술':
                        resultsHTML += '<p>지식을 탐구하고 논리적으로 사고하는 것을 좋아합니다. 깊이 있는 분석과 학습에 능합니다.</p>';
                        break;
                    case '예창':
                        resultsHTML += '<p>예술적 감수성과 창의성을 통해 자신을 표현하는 것을 즐깁니다. 미적 감각이 뛰어납니다.</p>';
                        break;
                    case '체육':
                        resultsHTML += '<p>활동적이고 경쟁을 즐기며, 신체 단련을 통해 스트레스를 해소하는 편입니다. 강한 승부욕을 가지고 있습니다.</p>';
                        break;
                    default:
                        resultsHTML += '<p>이 분야에 대한 설명입니다.</p>';
                }
            });
            resultsHTML += '</div>';
        } else {
            resultsHTML += '<p class="no-result">어떤 분야도 특별히 두드러지지 않습니다. 다양한 분야에 관심이 많으시군요!</p>';
        }
    }

    resultsContainer.innerHTML = resultsHTML;
}