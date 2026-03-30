from google import genai
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Initialize the Gemini Client
# Make sure your .env has GEMINI_API_KEY
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
