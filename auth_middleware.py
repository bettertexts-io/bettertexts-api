import json
import requests
from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from config import config_env

api_key_header = APIKeyHeader(name="access_token", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == config_env["API_KEY"]:
        return api_key_header   
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )

def verify_captcha(captcha_solution):
    # Request friendlycaptcha API
    url = "https://api.friendlycaptcha.com/v1/siteverify"

    payload = {
        "solution": captcha_solution,
        "sitekey": config_env["CAPTCHA_SITEKEY"],
        "secret": config_env["CAPTCHA_SECRET"],
    }

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Return if response is valid
    return json.loads(response.text)["success"] == True

