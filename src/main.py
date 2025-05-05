import sys
import os
from langchain.agents import Tool, initialize_agent, AgentType

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from pipeline.prompt_builder import PromptBuilder
from integrations.tools import AIATools
from pipeline.ai_generator import get_gemini_llm

metadata_json = {
    "structure": "blog",
    "persona": "professional",
    "topic": "AI in Healthcare",
    "tone": "informative",
    "keyword": "AI in Healthcare",
    "goal": "Informative blog post about AI in Healthcare"
}

def initialize_ai_tools():
    ai_tools_instance = AIATools(metadata_json)
    trends_data = Tool(
        name="fetch_google_trends_data",
        func=lambda x: ai_tools_instance.get_raw_trends(),
        description='''Fetches Google Trends data for the blog topic, including interest 
        over time, regional interest, and related queries.'''
    )
    return [trends_data]

def run_blog_generation():
    tools = initialize_ai_tools()
    prompt_builder = PromptBuilder(metadata_json)
    prompt_template = prompt_builder.build_prompt()
    formatted_prompt = prompt_template.format(**metadata_json)
    llm_chain = get_gemini_llm()

    agent = initialize_agent(
        tools=tools,
        llm=llm_chain,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=False,
        max_iterations=3,
        early_stopping_method="generate",
    )

    try:
        result = agent.invoke({"input": formatted_prompt})
        return result["output"]
    except Exception as e:
        print(f"Error during blog generation: {str(e)}")
        return "Error processing the blog. Please check the logs."

if __name__ == "__main__":
    print(run_blog_generation())
