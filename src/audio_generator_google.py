
from gtts import gTTS
import os
import uuid

def generate_audio(text, api_key=None, lang='pt'):
    """
    Converts text to speech using Google's gTTS library.
    Note: api_key is unused for gTTS (it's free/tokenless), but kept for interface consistency if needed.
    """
    try:
        # gTTS doesn't support massive texts in one go perfectly sometimes, but it handles basic segmentation internally.
        # However, for very large texts, it might be safer to use our own segmentation if needed.
        # For now, we rely on gTTS internal handling which is usually robust for decent lengths.
        
        # Determine language code for gTTS (simple mapping)
        # gTTS uses 2-letter codes mostly. 
        # lang input might be 'Postuguês' or 'pt'.
        
        lang_code = 'pt' # Default
        if lang.lower().startswith('en') or 'inglês' in lang.lower():
            lang_code = 'en'
        elif lang.lower().startswith('es') or 'espanhol' in lang.lower():
            lang_code = 'es'
        elif lang.lower().startswith('fr') or 'francês' in lang.lower():
            lang_code = 'fr'
        elif lang.lower().startswith('de') or 'alemão' in lang.lower():
            lang_code = 'de'
        elif lang.lower().startswith('it') or 'italiano' in lang.lower():
            lang_code = 'it'
            
        tts = gTTS(text, lang=lang_code)
        
        # Ensure assets directory exists
        os.makedirs("assets", exist_ok=True)
        
        # Create a unique filename
        filename = f"assets/audio_google_{uuid.uuid4()}.mp3"
        
        tts.save(filename)
        return filename
        
    except Exception as e:
        raise Exception(f"Audio generation failed: {str(e)}")
