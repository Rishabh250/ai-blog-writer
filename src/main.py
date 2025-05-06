from src.pipeline.prompt_builder import PromptBuilder
from src.integrations.tools import FetchGoogleTrendsDataTool, ResearchTool
from src.pipeline.ai_generator import get_gemini_llm
from src.utils.helpers import Helpers

metadata_json = {
    "structure": "blog", # blog, how-to, listicle, comparison, guide, faq
    "persona": "professional", # professional, academic, casual
    "topic": "AI in Healthcare",
    "tone": "informative", # informative, engaging, persuasive
    "keyword": "AI in Healthcare", # primary keyword to include naturally
    "goal": "Informative blog post about AI in Healthcare"
}

def initialize_ai_tools():
    fetch_trends_tool  = FetchGoogleTrendsDataTool(metadata_json)
    research_tool = ResearchTool(metadata_json)

    trends_data = fetch_trends_tool.get_raw_trends()
    research_data = research_tool.get_research()

    return trends_data, research_data

def run_blog_generation() -> bool:
    trends_data, research_data = initialize_ai_tools()

    prompt_builder = PromptBuilder(metadata_json, trends_data=trends_data, research_data=research_data)
    prompts = prompt_builder.build_prompt()

    llm_chain = get_gemini_llm()

    blog_sections = []

    try:
        for prompt_template in prompts.values():
            formatted_prompt = prompt_template.format(**metadata_json)
            result = llm_chain.invoke(formatted_prompt)
            blog_sections.append(f"{result.content}\n")

        full_blog = "\n".join(blog_sections)
        # full_blog_text, full_blog_html = Helpers.markdown_to_text(full_blog)
        print(full_blog)
        return True

    except (KeyError, ValueError, ConnectionError, TimeoutError) as e:
        print(f"Error during blog generation: {str(e)}")
        return False
