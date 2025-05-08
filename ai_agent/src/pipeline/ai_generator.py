from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import settings


def get_gemini_llm(model: str = settings.LLM_MODEL, **kwargs):
    return ChatGoogleGenerativeAI(model=model, **kwargs)
