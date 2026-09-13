import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def understand_request(user_request):
    prompt = f"""
You are OmniAI, an intelligent dress recommendation agent.

Understand the user's shopping requirement and extract:

- occasion
- dress type
- budget
- preferred brand
- preferred shopping platform
- preferred color
- preferred style
- gender

User request:
{user_request}

Return the information clearly.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text