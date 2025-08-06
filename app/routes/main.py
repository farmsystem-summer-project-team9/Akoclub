from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/questions/<int:number>')
def questions(number):
    return render_template(f'questions/question_{number}.html')

@main_bp.route('/result')
def result():
    return render_template('result.html')

@main_bp.route('/clubs')
def clubs():
    return render_template('clubs.html')

@main_bp.route('/detail_questions')
def detail_questions():
    return render_template('detail_questions.html')

@main_bp.route('/result_choice')
def result_choice():
    return render_template('result_choice.html')
