import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Read required variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")

# Model Routing
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
