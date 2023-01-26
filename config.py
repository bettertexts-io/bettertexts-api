import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
API_KEY = os.environ.get("API_KEY")

config_env = {
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "API_KEY": API_KEY
}
