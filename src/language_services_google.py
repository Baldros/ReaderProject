
from langdetect import detect
import google.generativeai as genai

def detect_language(text):
    """
    Detects the language of the text.
    Returns language code (e.g., 'en', 'pt', 'es').
    Uses langdetect (local) for consistency and speed.
    """
    try:
        # Detect language of the first 500 characters to be fast
        return detect(text[:500])
    except:
        return 'unknown'

def translate_text(text, target_lang, api_key):
    """
    Translates text to target language using Google Gemini (via google-generativeai).
    """
    if not api_key:
        raise ValueError("Google API Key is required for translation.")
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"Translate the following text to {target_lang}. Return ONLY the translated text, no intro or outro. Text: \n\n{text}"
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Translation failed: {str(e)}")
