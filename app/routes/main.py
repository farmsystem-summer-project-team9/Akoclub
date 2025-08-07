# app/routes/main.py
# 메인 페이지 및 결과 처리 라우트

from flask import Blueprint, render_template, request
import os
import json
from app.constants.club_mapping import QUESTION_CLUB_MAP
from app.models import Club
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


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



# 결과 선택 페이지
@main_bp.route('/result_choice')
def result_choice():
    return render_template('result_choice.html')


#분과 내 전체 동아리 리스트 페이지
@main_bp.route('/clubs/<string:department>')
def show_clubs_by_department(department):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    json_path = os.path.join(BASE_DIR, 'db', 'csvjson.json')

    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)

    # department 포함된 동아리들 필터링
    clubs = [club for club in data if department in club['department']]

    if not clubs:
        return render_template('404.html', message=f"{department} 분과에 해당하는 동아리가 없습니다."), 404

    return render_template('club_list.html', department=department, clubs=clubs)


#각 동아리 세부사항 페이지 
@main_bp.route('/club/<int:club_id>')
def show_club_detail(club_id):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    json_path = os.path.join(BASE_DIR, 'db', 'csvjson.json')

    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)

    # club_id로 해당 동아리 찾기
    club = next((club for club in data if club['id'] == club_id), None)

    if not club:
        return render_template('404.html', message=f"{club_id}번 동아리를 찾을 수 없습니다."), 404

    # 이미지 자동 설정
    img_extensions = ['.jpg', '.png', '.jpeg']
    for ext in img_extensions:
        image_path = os.path.join(BASE_DIR, 'static', 'images', 'clubs', f'club{club_id}{ext}')
        if os.path.exists(image_path):
            club['club_logo'] = f'images/clubs/club{club_id}{ext}'
            break
    else:
        club['club_logo'] = 'images/default.png'

    return render_template('club_detail.html', club=club)



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
                
        # 로고 삽입 코드
        img_extensions = ['.jpg', '.png', '.jpeg']
        for ext in img_extensions:
            image_path = os.path.join(BASE_DIR, 'static', 'images', 'clubs', f'club{club_data["id"]}{ext}')
            if os.path.exists(image_path):
                # club_data에 이미지 경로 저장
                club_data['club_logo'] = f'images/clubs/club{club_data["id"]}{ext}'
                break
        else:
            # 이미지 못 찾으면 기본 이미지로 설정
            club_data['club_logo'] = 'images/default.png'


        return render_template('result.html', club=club_data)

    except Exception as e:
        print("JSON 파일 불러오기 실패:", e)
        return "서버 내부 오류입니다.", 500