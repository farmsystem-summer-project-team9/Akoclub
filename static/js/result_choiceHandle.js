 //result_choiceHandle.js
 // 페이지 로드 시 최고 점수 분과 확인
 
        window.addEventListener('load', () => {
            const finalScores = JSON.parse(localStorage.getItem('finalScores')) || {};
            
            // 가장 높은 점수를 받은 카테고리 찾기
            let maxScore = -1;
            let topCategory = '';
            
            for (const category in finalScores) {
                if (finalScores[category] > maxScore) {
                    maxScore = finalScores[category];
                    topCategory = category;
                }
            }
            
            // 결과 메시지에 분과명 표시
            if (topCategory) {
                const messageElement = document.querySelector('.result-message');
                messageElement.innerHTML = `와우! 너의 취향이 이제 좀 보여!<br><span class="category-highlight">${topCategory}</span> 분과가 가장 잘 맞아!!`;
                
                // 분과 정보를 로컬 스토리지에 저장
                localStorage.setItem('selectedCategory', topCategory);
            }
        });
        
        function viewAllClubs() {
            // 분과 내 모든 동아리 보기 페이지로 이동
            const selectedCategory = localStorage.getItem('selectedCategory');
            if (selectedCategory) {
                // 여기에 분과별 동아리 목록 페이지로 이동하는 로직 추가
                window.location.href = `/clubs/${selectedCategory}`;
            } else {
                alert('분과 정보를 찾을 수 없습니다. 다시 테스트를 진행해주세요.');
                window.location.href = '/templates/index.html';
            }
        }
        
        function detailedQuestions() {
            const selectedCategory = localStorage.getItem('selectedCategory');

            const detailPageMap = {
                "봉사": "volunteer/volunteer_dQ1.html",
                "공연": "performance/performance_dQ1.html",
                "체육": "sports/sports_dQ1.html",
                "학술": "study/study_dQ1.html",
                "예창": "art/art_dQ1.html",
                "사회": "social/social_dQ1.html"
            };

        if (selectedCategory && detailPageMap[selectedCategory]) {
            window.location.href = `/detail_questions/${selectedCategory}`;
        } else {
            alert('세부 질문 페이지를 찾을 수 없습니다. 다시 테스트를 진행해주세요.');
            window.location.href = '/templates/index.html';
        }
}


        function retryQuiz() {
            // 로컬 스토리지 초기화
            localStorage.removeItem('userAnswers');
            localStorage.removeItem('finalScores');
            // 첫 번째 질문으로 이동 (올바른 경로로 수정)
            window.location.href = '/templates/questionforSection/question_1.html';
        }