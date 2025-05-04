import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
from pipeline.prompt_builder import PromptBuilder
from pipeline.ai_generator import GeminiLLMChain

metadata_json = {
    "structure": "blog",
    "persona": "professional",
    "topic": "Education Loan for Study is USA",
    "tone": "professional",
    "keyword": "Education Loan for Study is USA",
    "goal": "Education Loan for Study is USA"
}

prompt_builder = PromptBuilder(metadata_json)
prompt = prompt_builder.build_prompt()

llm_chain = GeminiLLMChain(prompt=prompt, model=settings.LLM_MODEL)

result = llm_chain.run(metadata_json)
print(result)
