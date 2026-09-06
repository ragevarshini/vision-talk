import os
import base64
import requests

from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# OPENROUTER CONFIGURATION
# ============================================================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

MODEL = "google/gemini-2.5-flash"


# ============================================================
# CONVERT IMAGE TO BASE64 DATA URL
# ============================================================

def image_to_data_url(image_bytes, mime_type):

    encoded_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    return (
        f"data:{mime_type};base64,"
        f"{encoded_image}"
    )


# ============================================================
# ANALYZE IMAGE
# ============================================================

def analyze_image(
    image_bytes,
    mime_type="image/jpeg",
    prompt=None
):

    # --------------------------------------------------------
    # Check API key
    # --------------------------------------------------------

    if not OPENROUTER_API_KEY:

        raise ValueError(
            "OPENROUTER_API_KEY is not configured. "
            "Please add it to your .env file."
        )


    # --------------------------------------------------------
    # Default image analysis prompt
    # --------------------------------------------------------

    if prompt is None:

        prompt = """
You are VisionTalk, an AI assistant designed to
help visually impaired users understand images.

Analyze the image carefully.

Provide a clear description of:

1. What is shown in the image
2. Important objects
3. People, if present
4. What people are doing
5. Visible text
6. Surroundings
7. Important details that may help a visually
   impaired user understand the image

Use simple and easy-to-understand language.

Do not invent information that cannot be determined
from the image.
"""


    # --------------------------------------------------------
    # Convert image
    # --------------------------------------------------------

    image_url = image_to_data_url(
        image_bytes,
        mime_type
    )


    # --------------------------------------------------------
    # API PAYLOAD
    # --------------------------------------------------------

    payload = {

        "model": MODEL,

        "messages": [

            {
                "role": "user",

                "content": [

                    {
                        "type": "text",
                        "text": prompt
                    },

                    {
                        "type": "image_url",

                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],

        "temperature": 0.2,

        "max_tokens": 1000
    }


    # --------------------------------------------------------
    # HEADERS
    # --------------------------------------------------------

    headers = {

        "Authorization":
            f"Bearer {OPENROUTER_API_KEY}",

        "Content-Type":
            "application/json",

        "HTTP-Referer":
            "http://localhost:8501",

        "X-Title":
            "VisionTalk"
    }


    # --------------------------------------------------------
    # SEND REQUEST TO OPENROUTER
    # --------------------------------------------------------

    response = requests.post(

        OPENROUTER_URL,

        headers=headers,

        json=payload,

        timeout=120
    )


    # --------------------------------------------------------
    # HANDLE API ERRORS
    # --------------------------------------------------------

    if response.status_code != 200:

        try:

            error_message = response.json()

        except Exception:

            error_message = response.text

        raise RuntimeError(
            f"OpenRouter API Error: {error_message}"
        )


    # --------------------------------------------------------
    # READ RESPONSE
    # --------------------------------------------------------

    result = response.json()


    try:

        answer = (
            result["choices"][0]
            ["message"]["content"]
        )

    except (KeyError, IndexError):

        raise RuntimeError(
            "Unexpected response received from OpenRouter."
        )


    return answer