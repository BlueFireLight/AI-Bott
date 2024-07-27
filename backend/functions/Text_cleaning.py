import re

def clean_text_for_audio(response_text):
    
    # Remove asterisks and other unwanted characters
    cleaned_text = re.sub(r'[*]', '', response_text)
    cleaned_text = re.sub(r'[^\w\s,.!?]', '', cleaned_text)  # Keep alphanumeric and punctuation
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Remove extra whitespace
    cleaned_text = cleaned_text.strip()  # Remove leading and trailing whitespace
    
    # Additional formatting for audio clarity
    cleaned_text = re.sub(r'\.\s*', '. ', cleaned_text)  # Ensure space after periods
    cleaned_text = re.sub(r',\s*', ', ', cleaned_text)  # Ensure space after commas
    
    return cleaned_text
