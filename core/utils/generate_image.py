from django.core.files.base import ContentFile
from django.conf import settings
import io


# from openai import OpenAI
# client = OpenAI(api_key=settings.OPENAI_API_KEY)

# def generate_image(prompt: str, size="1024x1024"):
#     response = client.images.generate(
#         model="gpt-image-1-mini",
#         prompt=prompt,
#         size=size,
#         quality="low",
#         n=1,
#     )

#     image_url = response.data[0].url
#     image_response = requests.get(image_url)
    
#     return ContentFile(image_response.content, name=f"ai_{hash(prompt)}.png")

from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="hf-inference",
    api_key=settings.HUGGINGFACE_API_KEY
)

def generate_image_from_prompt(prompt: str):
    """
    Generate image using Hugging Face (Flux.1-schnell)
    """
    try:
        # Generate image (returns PIL Image)
        image = client.text_to_image(
            prompt=prompt,
            model="black-forest-labs/FLUX.1-schnell",
            width=1024,
            height=1024,
            num_inference_steps=20,
        )
        
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Return as Django ContentFile
        filename = f"ai_generated_{hash(prompt) % 100000}.png"
        return ContentFile(img_byte_arr, name=filename)
        
    except Exception as e:
        raise Exception(f"AI Image Generation failed: {str(e)}")