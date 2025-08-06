# app/routes/main.py
# 메인 페이지 및 결과 처리 라우트

from flask import Blueprint, render_template, request
import os
import json
from app.constants.club_mapping import QUESTION_CLUB_MAP

# 블루프린트 설정
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



# 분과 결정 결과 → 세부 질문 시작 페이지
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
        return "페이지를 찾을 수 없습니다.", 404



# 세부 질문의 각 단계별 라우트
@main_bp.route('/detail_questions/<category>/<page>')
def render_detail_question(category, page):
    try:
        return render_template(f'detail_questions/{category}/{page}.html')
    except:
        return "페이지를 찾을 수 없습니다.", 404



# 최종 결과 페이지
@main_bp.route('/result')
def result():
    question_id = request.args.get('question_id')
    option_index = request.args.get('option_index', type=int)

    if not question_id or option_index is None:
        return "잘못된 요청입니다.", 400

    try:
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        json_path = os.path.join(BASE_DIR, 'db', 'csvjson.json')

        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)

        club_id = QUESTION_CLUB_MAP.get(question_id, {}).get(option_index)

        if not club_id:
            return "추천된 클럽이 없습니다.", 404

        club_data = next((club for club in data if club['id'] == club_id), None)

        if not club_data:
            return "해당 클럽 데이터를 찾을 수 없습니다.", 404

        return render_template('result.html', club=club_data)

    except Exception as e:
        print("JSON 파일 불러오기 실패:", e)
        return "서버 내부 오류입니다.", 500