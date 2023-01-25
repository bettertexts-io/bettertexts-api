from fastapi import FastAPI
import os
import openai
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = FastAPI()

# get query parameter q
@app.post("/api/v1/paraphrase")
def generate_prompt(input: str = "", style: str = "natural", medium: str = "text"):
    # print all three parameters
    print("Input: ", input)
    print("Style: ", style)
    print("Medium: ", medium)

    # if input is empty, return empty array
    if input == "":
        return {"status": 200, "results": []}
    else:
        try:
          # prompt = f"Paraphrase this input, intended for a {medium}, in two different ways in a {style} style, not identical, but keep meaning: '{input}'"
          prompt = f"Rephrase the following text in a {style} tone for a {medium} while maintaining the original meaning: {input}"
          
          response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=250,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
          )

          generated_result = response.choices[0].text

          return {"status": 200, "results": [generated_result]}

        except Exception as e:
          print("Error: ", e)
          return {"status": 500, "results": []}


