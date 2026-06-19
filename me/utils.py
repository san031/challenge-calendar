import google.generativeai as genai
from django.conf import settings
genai.configure(api_key =  settings.GEMINI_API_KEY)
def detect_mood(content: str) -> str:
    """
    Sends journal content to Gemini and returns a detected mood.
    """
    model = genai.GenerativeModel('gemini-2.5-flash-lite')

    prompt = f"""Analyze the mood of this journal entry and respond with exactly one word from this list only:

happy, sad, anxious, angry, calm, excited, grateful, frustrated, neutral

Journal entry:
{content}

Respond with one word only, nothing else."""

    response = model.generate_content(prompt)
    mood = response.text.strip().lower()

    allowed_moods = ['happy', 'sad', 'anxious', 'angry', 'calm', 'excited', 'grateful', 'frustrated', 'neutral']
    return mood if mood in allowed_moods else 'neutral'