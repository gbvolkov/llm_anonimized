from dotenv import load_dotenv,dotenv_values
import os

from pathlib import Path


if os.path.exists("gv.env"):
    load_dotenv('./gv.env')
else:
    documents_path = Path.home() / ".env"
    load_dotenv(os.path.join(documents_path, 'gv.env'))

GIGA_CHAT_USER_ID=os.environ.get('GIGA_CHAT_USER_ID')
GIGA_CHAT_SECRET = os.environ.get('GIGA_CHAT_SECRET')
GIGA_CHAT_AUTH = os.environ.get('GIGA_CHAT_AUTH')
GIGA_CHAT_SCOPE = "GIGACHAT_API_PERS"

LANGCHAIN_API_KEY = os.environ.get('LANGCHAIN_API_KEY')
#LANGCHAIN_API_KEY_DEV = os.environ.get('LANGCHAIN_API_KEY_DEV')
LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

YA_API_KEY = os.environ.get('YA_API_KEY')
YA_FOLDER_ID = os.environ.get('YA_FOLDER_ID')
YA_AUTH_TOKEN = os.environ.get('YA_AUTH_TOKEN')

GEMINI_API_KEY=os.environ.get('GEMINI_API_KEY')

CRYPRO_KEY = os.environ.get('CRYPRO_KEY')
SECRET_APP_KEY = os.environ.get('SECRET_APP_KEY')

# Flask-Session: store session data in server files instead of cookies
SESSION_TYPE = 'filesystem'
# Directory to store session files; ensure this exists or adjust path
SESSION_FILE_DIR = os.path.join("./data/sessions/", 'flask_session')
SESSION_PERMANENT = False
SESSION_USE_SIGNER = True  # add HMAC to session cookie
# SECRET_KEY should be set elsewhere (environment or hardcoded)