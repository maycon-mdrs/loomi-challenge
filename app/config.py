import os
from dotenv import load_dotenv
from decouple import config
from passlib.context import CryptContext

load_dotenv()

API_PREFIX = "/api/v1"

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
DATABASE_URL = config("DATABASE_URL")
OPENAI_API_KEY = config("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Model configs
MODEL_VIZUALIZER = os.getenv("MODEL_VIZUALIZER", "gpt-4.1")
TEMPERATURE_VIZUALIZER = os.getenv("TEMPERATURE_VIZUALIZER", 0.1)

MODEL_PAINTS = os.getenv("MODEL_PAINTS", "gpt-4.1")
TEMPERATURE_PAINTS = float(os.getenv("TEMPERATURE_PAINTS", 0.1))

MODEL_SUPERVISOR = os.getenv("MODEL_SUPERVISOR", "gpt-4.1")
TEMPERATURE_SUPERVISOR = float(os.getenv("TEMPERATURE_SUPERVISOR", 0))

crypt_context = CryptContext(schemes=["sha256_crypt"])
