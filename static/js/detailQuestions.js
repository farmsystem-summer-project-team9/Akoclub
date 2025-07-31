//detailQuestions.js
//세부질문 다음으로 넘어가는 로직

document.addEventListener('DOMContentLoaded', () => {
    const optionButtons = document.querySelectorAll('.option-btn');

    optionButtons.forEach(button => {
        button.addEventListener('click', () => {
            optionButtons.forEach(btn => btn.classList.remove('selected'));
            button.classList.add('selected');

            // 클릭한 버튼의 data-href 속성 읽어서 이동
            const nextHref = button.dataset.href;
            if (nextHref) {
                setTimeout(() => {
                    window.location.href = nextHref;
                }, 300);
            }
        });
    });
});
