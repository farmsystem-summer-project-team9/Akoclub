#app/__init__.py
# Flask 앱 객체를 생성
# Flask 설정값 등록
# 확장 기능 초기화 

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()  # db 객체 생성 (여기선 초기화만)

def create_app():
    app = Flask(
        __name__,
        static_folder='../static'         # 정적 파일 경로
    )

    #DB설정
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:비밀번호@localhost/akoclub'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)   # 프론트에서 주소 요청해도 오류 없이 연결
    db.init_app(app) # Flask 앱에 db 연결

#메인 페이지 라우트 블루프린트 등록
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
 
 # 블루프린트 등록
    from app.routes.department import club_bp
    app.register_blueprint(club_bp)

    return app

