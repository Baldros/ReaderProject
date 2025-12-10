from openai import OpenAI
import os
import uuid


def segment_text(text, max_length=4096):
    """
    Segments text into chunks smaller than max_length, respecting sentence boundaries.
    """
    if len(text) <= max_length:
        return [text]

    segments = []
    while len(text) > max_length:
        # Initial cut at max_length
        cut_index = max_length
        
        # Try to find the last sentence ending punctuation before the cut
        # We look for ., !, ? allowed by a space or newline
        last_punct = -1
        for punct in ['. ', '? ', '! ', '.\n', '?\n', '!\n']:
            pos = text.rfind(punct, 0, cut_index)
            if pos > last_punct:
                last_punct = pos + 1 # Include the punctuation
        
        if last_punct != -1:
            cut_index = last_punct
        else:
            # If no punctuation found, try to cut at the last newline
            last_newline = text.rfind('\n', 0, cut_index)
            if last_newline != -1:
                cut_index = last_newline + 1
            else:
                 # If no newline, try to cut at the last space
                last_space = text.rfind(' ', 0, cut_index)
                if last_space != -1:
                    cut_index = last_space + 1
                # If still nothing (one giant word?), force cut at max_length (default)

        segments.append(text[:cut_index].strip())
        text = text[cut_index:].strip()
    
    if text:
        segments.append(text)
        
    return segments

def generate_audio(text, api_key, voice='alloy'):
    """
    Converts text to speech using OpenAI API.
    Handles long texts by segmentation and concatenation.
    Returns: Path to the generated audio file.
    """
    if not api_key:
        raise ValueError("API Key is required for audio generation.")

    client = OpenAI(api_key=api_key)
    
    
    try:
        segments = segment_text(text)
        combined_audio = b""
        
        for segment in segments:
            if not segment: continue
            
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=segment
            )
            # OpenAI returns raw binary for audio
            combined_audio += response.content

        # Ensure assets directory exists
        os.makedirs("assets", exist_ok=True)
        
        # Create a unique filename
        filename = f"assets/audio_{uuid.uuid4()}.mp3"
        
        with open(filename, "wb") as f:
            f.write(combined_audio)
            
        return filename
        
    except Exception as e:
        raise Exception(f"Audio generation failed: {str(e)}")
        
    except Exception as e:
        raise Exception(f"Audio generation failed: {str(e)}")
