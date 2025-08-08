# app/routes/search.py
# 동아리 검색 API (name / tags / description 대상) - JSON 기반 버전
from flask import Blueprint, jsonify, request
import os, json

search_bp = Blueprint('search_bp', __name__)

# JSON 파일 경로
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
JSON_PATH = os.path.join(BASE_DIR, 'db', 'csvjson.json')

def _load_data():
    with open(JSON_PATH, encoding='utf-8') as f:
        return json.load(f)  # 리스트[dict, dict, ...]

def _field_text(club, key):
    val = club.get(key)
    if val is None:
        return ""
    return str(val)

def _matches(club, tokens, mode):
    # name / tags / description 에 토큰이 포함되는지 (대소문자 무시)
    name = _field_text(club, 'name').lower()
    tags = _field_text(club, 'tags').lower()
    desc = _field_text(club, 'description').lower()

    def hit(tok):
        t = tok.lower()
        return (t in name) or (t in tags) or (t in desc)

    if mode == 'or':
        return any(hit(t) for t in tokens)
    # 기본 and
    return all(hit(t) for t in tokens)

def _club_to_dict(c):
    # JSON에 없는 키가 있어도 터지지 않도록 .get 사용
    return {
        'id': c.get('id'),
        'name': c.get('name'),
        'department': c.get('department'),
        'description': c.get('description'),
        'tags': c.get('tags'),
        'sns_link': c.get('sns_link'),
        'application_period': c.get('application_period'),
        'application_form': c.get('application_form'),
        'booth_location': c.get('booth_location'),
        'club_logo': c.get('club_logo')  # 없으면 None
    }

@search_bp.route('/clubs/search', methods=['GET'])
def search_clubs():
    """
    예) GET /api/clubs/search?q=밴드 음악&mode=and&page=1&pageSize=20
        - q: 검색어(띄어쓰기로 여러 단어)
        - mode: and|or (기본 and)
        - page / pageSize: 페이지네이션 (기본 1 / 20, 최대 50)
        - 선택: department=공연분과 (분과로 먼저 필터링하고 검색)
    """
    q = (request.args.get('q') or '').strip()
    if not q:
        return jsonify({'message': '검색어(q)를 입력해주세요.'}), 400

    mode = (request.args.get('mode') or 'and').lower()
    page = max(int(request.args.get('page', 1)), 1)
    size = min(max(int(request.args.get('pageSize', 20)), 1), 50)
    offset = (page - 1) * size

    tokens = [t for t in q.split() if t.strip()]
    if not tokens:
        return jsonify({'items': [], 'total': 0, 'page': page, 'pageSize': size})

    department = (request.args.get('department') or '').strip()

    data = _load_data()

    # 1) 분과로 1차 필터(옵션)
    if department:
        data = [c for c in data if department in _field_text(c, 'department')]

    # 2) 토큰 매칭
    filtered = [c for c in data if _matches(c, tokens, mode)]

    # 3) 정렬(이름 오름차순) + 페이지네이션
    filtered.sort(key=lambda c: _field_text(c, 'name'))
    total = len(filtered)
    rows = filtered[offset:offset+size]

    return jsonify({
        'items': [_club_to_dict(c) for c in rows],
        'total': total,
        'page': page,
        'pageSize': size,
        'query': q,
        'mode': mode,
        'department': department or None
    }), 200
@search_bp.route("/search")
def search_page():
    return render_template("search.html")

