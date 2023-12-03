import os
from dotenv import load_dotenv

load_dotenv()

TG_BOT_API_KEY = os.environ.get('TG_BOT_API_KEY')
API_URL = os.environ.get('API_URL')
USERS_ID = [eval(i) for i in os.environ.get('USERS_ID').split(',')]