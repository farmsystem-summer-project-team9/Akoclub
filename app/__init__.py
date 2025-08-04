# Flask 앱 객체를 생성
# Flask 설정값 등록
# 확장 기능 초기

from flask import Flask
from app.models import db

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sewon0812^^@localhost/akoclub'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(main_bp)

    return app
