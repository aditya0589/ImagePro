from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

def edit_image(image, edit_prompt):
    """
    Edit an image based on a given prompt using Google Generative AI.
    
    Args:
        image: PIL.Image object to be edited
        edit_prompt: String prompt describing the desired edit
    
    Returns:
        tuple: (edited_image: PIL.Image or None, generated_text: str or None, error: str or None)
    """
    try:
        # Initialize Google genai client
        client = genai.Client()
        
        # Call the generate_content API with image and edit prompt
        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=[edit_prompt, image],
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )

        # Process the response
        edited_image = None
        generated_text = None
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                generated_text = part.text
            elif part.inline_data is not None:
                try:
                    # Convert inline data to image
                    edited_image = Image.open(BytesIO(part.inline_data.data))
                except Exception as e:
                    return None, None, f"Error processing edited image: {e}"

        if edited_image is None:
            return None, None, "No edited image was generated in the response."
        
        return edited_image, generated_text, None

    except Exception as e:

        return None, None, f"Error editing image: {e}"
