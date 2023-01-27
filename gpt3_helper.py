import re
import openai

from config import config_env

openai.api_key = config_env["OPENAI_API_KEY"]

def get_gpt3_results(prompt: str):
    try:
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

        if generated_result != "" and re.match("^\s+$", generated_result) == None:
            generated_result = generated_result.replace("\n", "")
        cleaned_results.append(generated_result)
        return cleaned_results

    except Exception as e:
        print("Error: ", e)
        return []
