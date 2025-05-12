from flask import Blueprint, render_template, request, session, redirect, url_for
from llm import generate_answer
#from anonimizer import TextProcessor

from utils.prepare_text import strip_markdown_fences, escape_backticks
main_bp = Blueprint('main', __name__)

#anonimizer, deanonimizer = anonimizer_factory()
#processor = TextProcessor()

# Make sure you have set:
# app.secret_key = "a random secret string"

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    data = {
        'system_prompt': "Ты полезный помощник.",
        'user_request': "Привет!",
        'llm_response': "",
    }

    if request.method == 'POST':
        action = request.form.get('action')
        data['system_prompt']       = request.form.get('system_prompt', '')
        data['user_request']        = request.form.get('user_request', '')
        data['anonymized_request']  = request.form.get('anonymized_request', '')

        if action == 'go':
            answer = generate_answer(data['system_prompt'], data['user_request'])
            data['llm_response'] = answer
            #data['llm_response'] = answer


    return render_template('index.html', **data)
