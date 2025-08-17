from app.core_ai.openai_model import get_openai_model
import os
from dotenv import load_dotenv

load_dotenv()


class ModelConfig:
    """Centralized configuration of agent models (Singleton)."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelConfig, cls).__new__(cls)
            cls._instance._init_models()
        return cls._instance

    def _init_models(self):
        self.models = {
            "paints_expert": get_openai_model(
                model_name=os.getenv("MODEL_PAINTS", "gpt-4.1"),
                temperature=float(os.getenv("TEMPERATURE_PAINTS", 0.1)),
            ),
            "supervisor": get_openai_model(
                model_name=os.getenv("MODEL_SUPERVISOR", "gpt-4.1"),
                temperature=float(os.getenv("TEMPERATURE_SUPERVISOR", 0)),
            ),
        }


    def get_model(self, agent_type: str):
        """Returns the configured model for the agent type."""
        return self.models.get(agent_type)


# Utility function for quick access
def get_model(agent_type: str):
    return ModelConfig().get_model(agent_type)
