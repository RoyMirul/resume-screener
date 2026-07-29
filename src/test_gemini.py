import os
from dotenv import load_dotenv
from google import genai

# Load the secret key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Create a client with our key (new SDK style)
client = genai.Client(api_key=api_key)

# Send a test message using a current model
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Say 'Hello, partner! Gemini is working.' if you can read this.",
)
print(response.text)