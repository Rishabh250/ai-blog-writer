from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import settings


class GeminiLLMChain(LLMChain):
    def __init__(self, prompt: PromptTemplate, model: str = settings.LLM_MODEL, **kwargs):
        llm = ChatGoogleGenerativeAI(model=model, **kwargs)
        super().__init__(llm=llm, prompt=prompt, verbose=True)
