from fastapi import FastAPI
import os
import openai
from os.path import join, dirname
from dotenv import load_dotenv
from pydantic import BaseModel
import re

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

openai.api_key = os.environ.get("OPENAI_API_KEY")

class RequestBody(BaseModel):
    input: str = ""
    style: str = "natural"
    medium: str = "text"

app = FastAPI()

# get query parameter q
@app.post("/api/v1/paraphrase")
def generate_prompt(body: RequestBody):
    # print all three parameters
    print("Input: ", body.input)
    print("Style: ", body.style)
    print("Medium: ", body.medium)

    # if input is empty, return empty array
    if input == "":
        return {"status": 200, "results": []}
    else:
        try:
          # prompt = f"Paraphrase this input, intended for a {medium}, in two different ways in a {style} style, not identical, but keep meaning: '{input}'"
          prompt = f"Rephrase the following text in a {body.style} tone for a {body.medium} in two utter different options and seperate them by a %|%, while maintaining the original meaning: {body.input}"
          
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

          results = generated_result.split("%|%")
          cleaned_results = []

          for result in results:
            result = re.sub("Option [0-9]: ", "", result)
            # Check if result only contains \n characters with regex
            if result != "" and re.match("^\s+$", result) == None:
              result.replace("\n\n", "")
              cleaned_results.append(result)

          return {"status": 200, "results": cleaned_results}

        except Exception as e:
          print("Error: ", e)
          return {"status": 500, "results": []}


