from fastapi import Depends, FastAPI
from fastapi.security.api_key import APIKey
import openai
from pydantic import BaseModel
import re
import auth_middleware as auth
from config import config_env

openai.api_key = config_env["OPENAI_API_KEY"]

class RequestBody(BaseModel):
    input: str = ""
    style: str = "natural"
    medium: str = "text"

app = FastAPI()

# Endpoint to generate paraphrases
@app.post("/api/v1/paraphrase")
async def generate_prompt(body: RequestBody, api_key: APIKey = Depends(auth.get_api_key)):
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
          prompt = f"Rephrase the following text in a {body.style} tone for a {body.medium} in two different options, while keeping the original meaning: {body.input}"
          
          response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=300,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
          )

          generated_result = response.choices[0].text
          print("Generated Result: ", generated_result)

          splitted_vals = re.split("Option [0-9]: ", generated_result, maxsplit=3)
          splitted_vals = splitted_vals[1:]
          cleaned_results = []

          for result in splitted_vals:
            result = re.sub("Option [0-9]: ", "", result)
            # Check if result only contains \n characters with regex
            if result != "" and re.match("^\s+$", result) == None:
              result = result.replace("\n", "")
              cleaned_results.append(result)

          return {"results": cleaned_results}

        except Exception as e:
          print("Error: ", e)
          return {"results": []}


