from dotenv import load_dotenv
import os
import openai

load_dotenv() 


openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_assistant(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]
