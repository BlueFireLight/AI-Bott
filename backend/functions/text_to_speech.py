from gtts import gTTS
import io


def convert_text_to_speech_gtts(message):
    try:
        # Create a gTTS object
        tts = gTTS(text=message, lang='en',tld='co.in')
        
        # Save the speech to a BytesIO object
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        
        # Seek to the beginning of the BytesIO object
        audio_buffer.seek(0)
        
        return audio_buffer
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    