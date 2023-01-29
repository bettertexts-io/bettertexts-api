import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
API_KEY = os.environ.get("API_KEY")
CAPTCHA_SITEKEY = os.environ.get("CAPTCHA_SITEKEY")
CAPTCHA_SECRET = os.environ.get("CAPTCHA_SECRET")

config_env = {
    "OPENAI_API_KEY": OPENAI_API_KEY,
    "API_KEY": API_KEY,
    "CAPTCHA_SITEKEY": CAPTCHA_SITEKEY,
    "CAPTCHA_SECRET": CAPTCHA_SECRET
}
