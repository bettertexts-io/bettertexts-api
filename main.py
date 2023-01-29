from fastapi import Depends, FastAPI
from fastapi.security.api_key import APIKey
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
import re

import auth_middleware as auth
from gpt3_helper import get_gpt3_results
from prompt_helper import generate_prompt

class ParaphraseRequestBody(BaseModel):
    input: str = ""
    style: str = "natural"
    medium: str = "text"
    langCode: str = "en"

class ParaphraseRequestBodyDemo(BaseModel):
    input: str = ""
    style: str = "natural"
    medium: str = "text"
    langCode: str = "en"
    captcha_solution: str = ""

class CorrectSpellingRequestBody(BaseModel):
    input: str = ""
    langCode: str = "en"


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://bettertexts.io",
    "https://www.bettertexts.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to generate paraphrase
@app.post("/api/v1/paraphrase")
async def generate_paraphrase(body: ParaphraseRequestBody, _: APIKey = Depends(auth.get_api_key)):
    input, style, medium, langCode = body.input, body.style, body.medium, body.langCode

    # if input is empty, return empty array
    if input == "":
        return {"results": []}
    else:
        prompt = generate_prompt(input, style, medium, langCode)

        results = get_gpt3_results(prompt)
        return {"results": results}


# Endpoint to generate paraphrase
@app.post("/api/v1/paraphrase/demo")
async def generate_paraphrase_demo(body: ParaphraseRequestBodyDemo, _: APIKey = Depends(auth.get_api_key)):
    input, style, medium, langCode, captcha_solution = body.input, body.style, body.medium, body.langCode, body.captcha_solution

    # if input is empty, return empty array
    if input == "" or captcha_solution == "":
        return {"results": []}
    else:
        prompt = generate_prompt(input, style, medium, langCode)

        # Verify captcha solution
        if not auth.verify_captcha(captcha_solution):
            return {"results": []}

        results = get_gpt3_results(prompt)
        return {"results": results}


# Endpoint to generate mock paraphrases
@app.post("/api/v1/mock/paraphrase")
async def generate_mock_paraphrase(_: ParaphraseRequestBody, __: APIKey = Depends(auth.get_api_key)):
    # if input is empty, return empty array
    if input == "":
        return {"results": []}
    else:
        return {"results": ["This is a mock result", "This is another mock result"]}


# Endpoint to correct spelling
@app.post("/api/v1/correct")
async def correct_spelling(body: CorrectSpellingRequestBody, _: APIKey = Depends(auth.get_api_key)):
    input, langCode = body.input, body.langCode

    # if input is empty, return empty array
    if input == "":
        return {"results": []}
    else:
        lang = "German" if langCode == "de" else "English"
        prompt = f"Correct the spelling of the following input and return the output in {lang}. Input: {input}."
        
        results = get_gpt3_results(prompt)

        return {"results": results}
