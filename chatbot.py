import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

def get_response(user_prompt):

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt
    )

    return response.text


