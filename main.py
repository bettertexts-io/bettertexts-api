from fastapi import Depends, FastAPI
from fastapi.security.api_key import APIKey
from fastapi.middleware.cors import CORSMiddleware
import openai
from pydantic import BaseModel
import re
import auth_middleware as auth
from config import config_env

SPLIT_CHAR = "#+#"

openai.api_key = config_env["OPENAI_API_KEY"]

class RequestBody(BaseModel):
    input: str = ""
    style: str = "natural"
    medium: str = "text"

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to generate paraphrases
@app.post("/api/v1/paraphrase")
async def generate_paraphrases(body: RequestBody, api_key: APIKey = Depends(auth.get_api_key)):
    # print all three parameters
    print("Input: ", body.input)
    print("Style: ", body.style)
    print("Medium: ", body.medium)

    # if input is empty, return empty array
    if input == "":
        return {"results": []}
    else:
        try:
          # prompt = f"Paraphrase this input, intended for a {medium}, in two different ways in a {style} style, not identical, but keep meaning: '{input}'"
          # prompt = f"Rephrase the following text in a {body.style} tone for a {body.medium} in two different ways, return only the , while keeping the original meaning: {body.input}"
          prompt = f"Rephrase the following input, in a {body.style} tone for a {body.medium}, output only the raw generated paraphrase: {body.input}."
          
          response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=300,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
          )

          cleaned_results = []
          generated_result = response.choices[0].text
          print("Generated Result: ", generated_result)

          # splitted_vals = re.split(SPLIT_CHAR, generated_result, maxsplit=2)

          # for result in splitted_vals:
          #   result = re.sub(SPLIT_CHAR, "", result)
          #   # Check if result only contains \n characters with regex
          #   if result != "" and re.match("^\s+$", result) == None:
          #     result = result.replace("\n", "")
          #     cleaned_results.append(result)

          if generated_result != "" and re.match("^\s+$", generated_result) == None:
            generated_result = generated_result.replace("\n", "")
            cleaned_results.append(generated_result)

          return {"results": cleaned_results}

        except Exception as e:
          print("Error: ", e)
          return {"results": []}


# Endpoint to generate mock paraphrases
@app.post("/api/v1/mock/paraphrase")
async def generate_mock_paraphrases(body: RequestBody, api_key: APIKey = Depends(auth.get_api_key)):
   # print all three parameters
    print("Input: ", body.input)
    print("Style: ", body.style)
    print("Medium: ", body.medium)

    # if input is empty, return empty array
    if input == "":
        return {"results": []}
    else:
        return {"results": ["This is a mock result", "This is another mock result"]}
