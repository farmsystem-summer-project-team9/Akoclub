# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from urllib.parse import quote_plus

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='../static')

    pw = quote_plus('sewon0812^^')  # ^^ -> %5E%5E
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://root:{pw}@localhost:3306/akoclub?charset=utf8mb4"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    db.init_app(app)

    # 페이지 라우트
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    # API 라우트
    # from app.routes.department import club_bp
    from app.routes.search import search_bp
    # app.register_blueprint(club_bp, url_prefix='/api')
    app.register_blueprint(search_bp)


    return app

