from langchain.agents import Tool, initialize_agent, AgentType

from src.pipeline.prompt_builder import PromptBuilder
from src.integrations.tools import AIATools
from src.pipeline.ai_generator import get_gemini_llm

metadata_json = {
    "structure": "blog", # blog, how-to, listicle, comparison, guide, faq
    "persona": "professional", # professional, academic, casual
    "topic": "AI in Healthcare",
    "tone": "informative", # informative, engaging, persuasive
    "keyword": "AI in Healthcare", # primary keyword to include naturally
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

def run_blog_generation() -> str:
    tools = initialize_ai_tools()
    prompt_builder = PromptBuilder(metadata_json)
    prompts = prompt_builder.build_prompt()
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

    blog_sections = []
    try:
        for section, prompt_template in prompts.items():
            formatted_prompt = prompt_template.format(**metadata_json)
            print(f"\n=== Generating: {section} ===")
            result = agent.invoke({"input": formatted_prompt})
            blog_sections.append(f"## {section}\n{result['output']}\n")

        full_blog = "\n".join(blog_sections)
        return full_blog

    except (KeyError, ValueError, ConnectionError, TimeoutError) as e:
        print(f"Error during blog generation: {str(e)}")
        return "Error processing the blog. Please check the logs."
