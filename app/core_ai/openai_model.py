from langchain_openai import ChatOpenAI

def get_openai_model(model_name="gpt-4o-mini", temperature=0.1):
    """Flexible model factory."""
    return ChatOpenAI(model=model_name, temperature=temperature)
