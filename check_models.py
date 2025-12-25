import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your keys.env file
load_dotenv("keys.env")

# Configure the API
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("Checking available models...")
try:
    for m in genai.list_models():
        # Only show models that can generate text
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error: {e}")