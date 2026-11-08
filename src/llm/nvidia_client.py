from langchain_nvidia_ai_endpoints import ChatNVIDIA
from src.config import NVIDIA_API_KEY


def lister_modeles():
    client = ChatNVIDIA(api_key=NVIDIA_API_KEY)
    return [m.id for m in client.get_available_models()]


def creer_client(model_id: str, temperature: float = 0.2, max_tokens: int = 1024):
    return ChatNVIDIA(
        model=model_id,
        api_key=NVIDIA_API_KEY,
        temperature=temperature,
        max_tokens=max_tokens,
    )