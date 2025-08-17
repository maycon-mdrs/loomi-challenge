
import os
from decouple import config
from passlib.context import CryptContext


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
DATABASE_URL = config("DATABASE_URL")
OPENAI_API_KEY = config("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Model configs
MODEL_PAINTS = config("MODEL_PAINTS", default="gpt-4.1")
TEMPERATURE_PAINTS = config("TEMPERATURE_PAINTS", default=0.1, cast=float)
MODEL_SUPERVISOR = config("MODEL_SUPERVISOR", default="gpt-4.1")
TEMPERATURE_SUPERVISOR = config("TEMPERATURE_SUPERVISOR", default=0, cast=float)

crypt_context = CryptContext(schemes=["sha256_crypt"])
