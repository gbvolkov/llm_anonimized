from flask import Blueprint, render_template, request, redirect, url_for, make_response, session, current_app
import json

from llm import generate_answer, get_llm_parameters

main_bp = Blueprint('main_bp', __name__)

def get_available_models():
    defaults_map = get_llm_parameters('')
    return list(defaults_map.keys())

available_models = get_available_models()

@main_bp.before_app_request
def load_llm_params():
    if 'llm_params' not in session:
        params_cookie = request.cookies.get('llm_params')
        if params_cookie:
            try:
                session['llm_params'] = json.loads(params_cookie)
            except json.JSONDecodeError:
                session['llm_params'] = {}
        else:
            session['llm_params'] = {}

@main_bp.route('/', methods=['GET'])
def index():
    # Read system_prompt from cookie or use default
    default_prompt = request.cookies.get('system_prompt', 'Ты полезный помощник.')
    # Read user_request from query string on return or default greeting
    default_request = request.args.get('user_request', 'Привет!')
    # Restore last-used model or default to OpenAI
    selected_model = request.args.get('model') or request.cookies.get('model', 'OpenAI')

    # Load saved LLM parameters for the selected model only
    all_params = session.get('llm_params', {})
    llm_params = all_params.get(selected_model, {})

    return render_template('index.html', 
                           system_prompt=default_prompt, 
                           user_request=default_request,
                           available_models=available_models,
                           selected_model=selected_model,
                           llm_params=llm_params)

@main_bp.route('/config', methods=['GET', 'POST'])
def config():
    # Determine model to configure, falling back to cookie
    model = request.values.get('model') or request.cookies.get('model', available_models[0])

    if request.method == 'POST':
        defaults = get_llm_parameters(model)
        params = {}
        for name, default in defaults.items():
            raw = request.form.get(name, default)
            try:
                if isinstance(default, bool):
                    value = raw.lower() in ['true', '1', 'yes']
                elif isinstance(default, int):
                    value = int(raw)
                elif isinstance(default, float):
                    value = float(raw)
                else:
                    value = raw
            except Exception:
                value = raw
            params[name] = value

        # Merge this model's overrides into the session map
        all_params = session.get('llm_params', {})
        all_params[model] = params
        session['llm_params'] = all_params

        # Persist updated map in cookie
        resp = make_response(redirect(url_for('main_bp.index')))
        resp.set_cookie('model', model)
        resp.set_cookie('llm_params', json.dumps(all_params), max_age=30*24*3600)
        return resp

    # GET: render form with defaults and current session params
    parameters = get_llm_parameters(model)
    all_params = session.get('llm_params', {})
    return render_template(
        'config.html', model=model,
        parameters=parameters, llm_params=all_params
    )

@main_bp.route('/result', methods=['POST'])
def result():
    # Generate answer from submitted form
    system_prompt = request.form.get('system_prompt', '')
    user_request = request.form.get('user_request', '')
    model = request.form.get('model', 'OpenAI')
    
    # Load saved parameters for this model
    all_params = session.get('llm_params', {})
    llm_params = all_params.get(model, {})

    answer, anonymized_request, llm_answer = generate_answer(
        system_prompt=system_prompt, 
        user_request=user_request, 
        llm_provider=model,
        llm_parameters=llm_params
    )

    response = make_response(render_template(
        'result.html',
        llm_response=answer,
        anonymized_request=anonymized_request,
        llm_answer=llm_answer,
        user_request=user_request
    ))
    response.set_cookie('system_prompt', system_prompt)
    response.set_cookie('model', model)
    return response
