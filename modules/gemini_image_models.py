
from io import BytesIO
from dotenv import load_dotenv
import google.generativeai as genai
from google.genai import types


load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))


def get_image_description(image):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        
        prompt = f"""
        You are a highly observant AI with strong visual reasoning capabilities.

        Given the image provided, describe in rich detail what you see. Focus on:
        - The objects and people in the image
        - The setting and environment
        - Activities or actions taking place
        - Emotions, mood, or tone of the scene
        - Any notable details or unique features
        - Style, aesthetics, or visual themes (if applicable)

        Be factual but vivid, and avoid guessing beyond what is visually evident.

        Image: {image}

        Task: Generate a comprehensive and accurate description of the image.

        """


        
        # Generate content with temperature set to 1.5
        generation_config = genai.types.GenerationConfig(temperature=0.1)
        response = model.generate_content(
            [prompt, image],
            generation_config=generation_config
        )
        return response.text
    
    except Exception as e:
        return f"Error generating roast: {str(e)}"