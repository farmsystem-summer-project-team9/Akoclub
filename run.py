# 앱 실행 파일
# 실행 방법 : $ python run.py 입력

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)