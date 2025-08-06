# app/routes/main.py
# 메인 페이지 라우트

from flask import Blueprint, render_template, request
import os
import json

main_bp = Blueprint('main_bp', __name__)

# 메인 페이지
@main_bp.route('/')
def index():
    return render_template('index.html')

# 질문 1~6까지 출력
@main_bp.route('/questions/<int:num>')
def question(num):
    if 1 <= num <= 6:
        return render_template(f'questions/question_{num}.html')
    else:
        return "존재하지 않는 질문입니다.", 404

# 결과 선택지 라우트
@main_bp.route('/result_choice')
def result_choice():
    return render_template('result_choice.html')

# 분과 결정 결과  세부 질문으로 이동하는 페이지
@main_bp.route('/detail_questions/<category>')
def detail_questions(category):
    html_file_map = {
        "봉사": "volunteer/volunteer_dQ1.html",
        "공연": "performance/performance_dQ1.html",
        "체육": "sports/sports_dQ1.html",
        "학술": "study/study_dQ1.html",
        "예창": "art/art_dQ1.html",
        "사회": "social/social_dQ1.html"
    }

    template_path = html_file_map.get(category)
    if template_path:
        return render_template(f'detail_questions/{template_path}')
    else:
        return render_template('404.html'), 404
    


# 각 세부 질문에서 다음 질문으로 이동하는 페이지 
@main_bp.route('/detail_questions/<category>/<page>')
def render_detail_question(category, page):
    try:
        return render_template(f'detail_questions/{category}/{page}.html')
    except:
        return render_template('404.html'), 404
    



# 최종 결과 페이지
@main_bp.route('/result')
def result():
    question_id = request.args.get('question_id')
    option_index = request.args.get('option_index', type=int)

    # 유효성 검사
    if not question_id or option_index is None:
        return "잘못된 요청입니다.", 400

    # JSON 파일 경로 설정 (db 폴더가 app 밖에 있을 경우)
    try:
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        json_path = os.path.join(BASE_DIR, 'db', 'csvjson.json')

        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)

        # [질문 ID + 선택지] → 특정 club ID를 가져오는 매핑
        # 예시: volunteer_dQ1 → [클럽1, 클럽2, ...] 처럼 있다고 가정
        # 👉 실제 프로젝트에서는 아래 매핑을 따로 json이나 딕셔너리로 관리해야 합니다
        QUESTION_CLUB_MAP = {
            "volunteer_dQ1": [20, 21, 17],
            # 여기에 필요한 질문 ID 추가 가능
        }

        club_id = QUESTION_CLUB_MAP.get(question_id, [None])[option_index]

        # 클럽 ID가 유효하지 않은 경우
        if not club_id:
            return "클럽 정보를 찾을 수 없습니다.", 404

        # JSON 데이터에서 해당 ID의 클럽 정보 가져오기
        club_data = next((item for item in data if item['id'] == club_id), None)

        if not club_data:
            return "클럽 데이터를 찾을 수 없습니다.", 404

        return render_template('result.html', club=club_data)

    except Exception as e:
        print("JSON 파일 불러오기 실패:", e)
        return "데이터를 불러오는 중 오류가 발생했습니다.", 500
