from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/questions')
def questions():
    return render_template('questions/question_1.html')

@main_bp.route('/result')
def result():
    return render_template('result.html')

@main_bp.route('/clubs')
def clubs():
    return render_template('clubs.html')

@main_bp.route('/detail_questions')
def detail_questions():
    return render_template('detail_questions.html')
