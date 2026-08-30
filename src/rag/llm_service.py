import google.genai as genai

from config.settings import settings

client = genai.Client(
    api_key=settings.GOOGLE_API_KEY
)

def generate_answer(prompt):
    response = client.models.generate_content(
        model = settings.MODEL_NAME, contents=prompt
    )
    # config = {
    #     "system_instruction": "You are an Enterprise AI Assistant.",
    #         "temperature": 0.2
    # }
    
    return response.text