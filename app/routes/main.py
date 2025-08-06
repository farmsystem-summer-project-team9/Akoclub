# app/routes/main.py
from flask import Blueprint, render_template, request
from app.models import Club
#동아리 매핑 
from app.constants.club_mapping import QUESTION_CLUB_MAP


main_bp = Blueprint('main', __name__)


#메인페이지 
@main_bp.route('/')
def index():
    return render_template('index.html')


# 질문 페이지 동적 렌더링 (/questions/1 → question_1.html)
@main_bp.route('/questions/<int:number>')
def questions(number):
    return render_template(f'questions/question_{number}.html')


# 결과 선택 페이지
@main_bp.route('/result_choice')
def result_choice():
    return render_template('result_choice.html')


# 선택된 분과의 동아리 목록 페이지 (ex: /clubs/공연)
@main_bp.route('/clubs/<category>')
def clubs(category):
    return render_template('clubs.html', category=category)


# 선택된 분과에 따른 세부 질문 페이지
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


@main_bp.route('/detail_questions/<category>/<page>')
def render_detail_question(category, page):
    try:
        return render_template(f'detail_questions/{category}/{page}.html')
    except:
        return render_templage('404.html'), 404



#최종 결과 페이지
@main_bp.route('/result')
def result():
    question_id = request.args.get('question_id')
    option_index = request.args.get('option_index', type=int)

    if not question_id or option_index is None:
        return render_template('404.html'), 404

    club_id = QUESTION_CLUB_MAP.get(question_id, {}).get(option_index)

    if not club_id:
        return render_template('404.html'), 404

    club = Club.query.get(club_id)

    if not club:
        return render_template('404.html'), 404

    return render_template('result.html', club=club)


