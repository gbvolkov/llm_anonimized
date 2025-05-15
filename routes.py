from flask import (
    Blueprint, render_template, request,
    redirect, url_for, session
)
from llm import generate_answer, get_llm_parameters

main_bp = Blueprint('main_bp', __name__)
available_models = list(get_llm_parameters('').keys())

@main_bp.before_app_request
def load_defaults():
    # Ensure default keys exist in session
    session.setdefault('llm_params', {})
    session.setdefault('system_prompt', 'Ты полезный помощник.')
    session.setdefault('user_request', 'Привет!')
    session.setdefault('model', 'OpenAI')

@main_bp.route('/', methods=['GET'])
def index():
    # Retrieve from session instead of cookies/args
    system_prompt = session.get('system_prompt')
    user_request = session.get('user_request')
    selected_model = request.args.get('model') or session.get('model')

    # Load saved LLM parameters for this model
    llm_params = session['llm_params'].get(selected_model, {})

    return render_template(
        'index.html',
        system_prompt=system_prompt,
        user_request=user_request,
        available_models=available_models,
        selected_model=selected_model,
        llm_params=llm_params
    )

@main_bp.route('/config', methods=['GET', 'POST'])
def config():
    model = request.values.get('model') or session.get('model')

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

        # Merge into session map
        llm_map = session['llm_params']
        llm_map[model] = params
        session['llm_params'] = llm_map
        session['model'] = model

        return redirect(url_for('main_bp.index'))

    # GET: show form with defaults & saved overrides
    parameters = get_llm_parameters(model)
    llm_map = session.get('llm_params', {})

    return render_template(
        'config.html',
        model=model,
        available_models=available_models,
        parameters=parameters,
        llm_params=llm_map
    )

@main_bp.route('/result', methods=['POST'])
def result():
    # Save prompts
    session['system_prompt'] = request.form.get('system_prompt', '')
    session['user_request'] = request.form.get('user_request', '')
    model = request.form.get('model')
    session['model'] = model

    # Load params & generate
    llm_params = session['llm_params'].get(model, {})
    try:
        answer, anonymized_request, llm_answer = generate_answer(
            system_prompt=session['system_prompt'],
            user_request=session['user_request'],
            llm_provider=model,
            llm_parameters=llm_params
        )
    except Exception as e:
        error_msg = str(e)
        return render_template(
            'error.html',
            error=error_msg,
            selected_model=model
        ), 500

    # Optionally store answer
    session['llm_answer'] = llm_answer

    return render_template(
        'result.html',
        llm_response=answer,
        anonymized_request=anonymized_request,
        llm_answer=llm_answer,
        user_request=session['user_request']
    )