from langdetect import detect
from openai import OpenAI

def detect_language(text):
    """
    Detects the language of the text.
    Returns language code (e.g., 'en', 'pt', 'es').
    """
    try:
        # Detect language of the first 500 characters to be fast
        return detect(text[:500])
    except:
        return 'unknown'

def translate_text(text, target_lang, api_key):
    """
    Translates text to target language using OpenAI GPT-4o-mini.
    """
    if not api_key:
        raise ValueError("API Key is required for translation.")
        
    client = OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are a professional translator. Translate the user text to {target_lang}. Return ONLY the translated text. Do not add any introductory or concluding remarks. Maintain the original formatting."},
                {"role": "user", "content": text}
            ],
            temperature=0
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")

def chuncksize(text, chunk_size=1000):
    for i in range(0, len(text), chunk_size):
        yield text[i:i + chunk_size]