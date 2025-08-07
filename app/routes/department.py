# app/routes/department.py
# 추천된 분과의 동아리 리스트 출력 

from flask import Blueprint, jsonify
from app.models import Club


club_bp = Blueprint('club_bp', __name__)

@club_bp.route('/department/<string:department>', methods=['GET'])
def get_clubs_by_department(department):
    # 공백 제거, 대소문자 구분 없이 비교하려면 .ilike 사용
    clubs = Club.query.filter(Club.department.ilike(f'%{department}%')).all()

    if not clubs:
        return jsonify({'message': f'"{department}" 분과의 동아리를 찾을 수 없습니다.'}), 404

    result = [{
        'id': c.id,
        'name': c.name,
        'department': c.department,
        'description': c.description,
        'tags': c.tags,
        'sns_link': c.sns_link,
        'application_period': c.application_period,
        'application_form': c.application_form,
        'booth_location': c.booth_location,
        'club_logo': c.club_logo
    } for c in clubs]

    return jsonify(result)



# 특정 동아리 ID로 동아리 1개 정보 조회 API
@club_bp.route('/club/<int:club_id>', methods=['GET'])
def get_club_by_id(club_id):
    club = Club.query.get(club_id)

    if not club:
        return jsonify({'message': f'{club_id}번 ID의 동아리를 찾을 수 없습니다.'}), 404

    result = {
        'id': club.id,
        'name': club.name,
        'department': club.department,
        'description': club.description,
        'tags': club.tags,
        'sns_link': club.sns_link,
        'application_period': club.application_period,
        'application_form': club.application_form,
        'booth_location': club.booth_location,
        'club_logo': club.club_logo
    }

    return jsonify(result)