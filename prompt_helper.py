def generate_prompt(input: str, style: str, medium: str, langCode: str):
    language = "German" if langCode == "de" else "English"
    prompt = f"Rephrase the following input, in a {style} tone. Input: {input}. Output only the raw generated content in {language}."

    if medium == "email":
        prompt = f"Rephrase the following input to compose an email for the following recipient and purpose:\nInput: [input]\nRecipient: [Recipient's name and email address]\nSubject: [Email subject]\nBody: [Email body]\nPlease include a {style} tone, and make sure to address the recipient by name.\nFeel free to add any necessary details or information to complete the email and write it in {language}."
    elif medium == "bulletpoints":
        prompt = f"Summarize the following input in a bullet point list in a {style} tone. Input: {input}. The output should be in {language}."
    elif medium == "letter":
        prompt = f"Compose a letter in {language} addressed to [Recipient's Name] at [Recipient's Address]. The purpose of the letter is: {input}. Please include a {style} tone and make sure to address the recipient by name. Feel free to add any necessary details or information to complete the letter."
    elif medium == "joke":
        prompt = f"Generate a joke in {language} about the following topic: {input}. The joke should be appropriate for all audiences and should aim to make people laugh."
    elif medium == "tweet":
        prompt = f"Rephrase the following input to a tweet without hashtags that is no more than 280 characters. Make sure to include a {style} tone. Input: {input}. The output should be in {language}."

    return prompt

