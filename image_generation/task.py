from celery import shared_task
# import time
import requests
from dotenv import load_dotenv
from random import randint

import base64
import os

# Load environment variables from .env file
load_dotenv()

# Set the engine ID for the Stable Diffusion model, specifying the version to use.
engine_id = "stable-diffusion-v1-6"

# Retrieve the API host URL from the environment variables, defaulting to 'https://api.stability.ai' if not found.
api_host = os.getenv('API_HOST', 'https://api.stability.ai')

# Retrieve the base URL from the environment variables, defaulting to 'http://localhost:8000' if not found.
base_url = os.getenv('BASE_URL', 'http://localhost:8000')

# If the 'API_KEY' environment variable is not set, 'api_key' will be None, indicating that authentication is not possible.
api_key = os.getenv('API_KEY')

@shared_task(bind=True)
def generate_image_task(self):

    image_files = []
    prompt_images = ['A red flying dog', 'A piano ninja', 'A footballer kid']

    if api_key is None:
        raise Exception("Missing Stability API key.")
    
    for prompt in prompt_images:

        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": prompt
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()

        for _ , image in enumerate(data["artifacts"]):
            file_no = randint(1, 100)
            file_name = f'txt2img_{file_no}.png'
            file_location = f"media/images/{file_name}"
            with open(file_location, "wb") as f:
                f.write(base64.b64decode(image["base64"]))

            # Combine the base URL with the file location to create the full URL for the file.
            file_url = os.path.join(base_url, file_location)

            # Append the file name and its corresponding URL to the list of image files.
            image_files.append({"filename": file_name, "url": file_url})

    return image_files