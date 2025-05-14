from flask import Flask
from flask_session import Session
import config
#import os
#os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
#os.environ["LANGCHAIN_TRACING_V2"] = "true"

from routes import main_bp
from palimpsest.logger_factory import setup_logging

def create_app():
    app = Flask(__name__)
    # Load settings from config.py
    app.secret_key = config.SECRET_APP_KEY
    app.config.from_object('config')

    # Enable server-side sessions
    Session(app)

    # Register blueprints
    from routes import main_bp
    app.register_blueprint(main_bp)

    return app

if __name__ == '__main__':
    import logging
    setup_logging("anonimizer_web", project_console_level=logging.DEBUG, other_console_level=logging.DEBUG)
    app = create_app()
    app.run(host='0.0.0.0', port=5002, debug=False)