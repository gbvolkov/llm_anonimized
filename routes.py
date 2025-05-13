from flask import Blueprint, render_template, request, redirect, url_for, make_response
from llm import generate_answer

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    # Read system_prompt from cookie or use default
    default_prompt = request.cookies.get('system_prompt', 'Enter your system prompt here...')
    # Read user_request from query string on return or default greeting
    default_request = request.args.get('user_request', 'Привет!')
    return render_template('index.html', 
                           system_prompt=default_prompt, 
                           user_request=default_request)

@main_bp.route('/result', methods=['POST'])
def result():
    # Generate answer from submitted form
    system_prompt = request.form.get('system_prompt', '')
    user_request = request.form.get('user_request', '')
    answer, anonymized_request, llm_answer = generate_answer(system_prompt, user_request)

    # Render result.html with raw markdown and original request
    # Optionally set system_prompt cookie for next time
    #response = make_response(
    #    render_template('result.html', 
    #                    llm_response=answer, 
    #                    user_request=user_request)
    #)
    response = make_response(render_template(
        'result.html',
        llm_response=answer,
        anonymized_request=anonymized_request,
        llm_answer=llm_answer,
        user_request=user_request,
    ))
    # Uncomment to persist system_prompt:
    # response.set_cookie('system_prompt', system_prompt)
    return response