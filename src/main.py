from typing import Any, Dict, Tuple

from src.integrations.tools import FetchGoogleTrendsDataTool, ResearchTool
from src.pipeline.ai_generator import get_gemini_llm
from src.pipeline.prompt_builder import PromptBuilder
from src.utils.helpers import Helpers


def initialize_ai_tools(metadata: Dict[str, Any]):
    fetch_trends_tool = FetchGoogleTrendsDataTool(metadata)
    research_tool = ResearchTool(metadata)

    trends_data = fetch_trends_tool.get_raw_trends()
    research_data = research_tool.get_research()

    return trends_data, research_data


def run_blog_generation(metadata: Dict[str, Any] = None) -> Tuple[str, str, bool]:
    metadata_json = metadata

    try:
        trends_data, research_data = initialize_ai_tools(metadata_json)

        prompt_builder = PromptBuilder(
            metadata_json, trends_data=trends_data, research_data=research_data
        )

        prompts = prompt_builder.build_prompt()

        llm_chain = get_gemini_llm()

        blog_sections = []

        for prompt_template in prompts.values():
            formatted_prompt = prompt_template.format(**metadata_json)
            result = llm_chain.invoke(formatted_prompt)
            blog_sections.append(f"{result.content}\n")

        full_blog = "\n".join(blog_sections)
        html = Helpers.markdown_to_text(full_blog)

        return full_blog, html, True

    except (KeyError, ValueError, ConnectionError, TimeoutError) as e:
        error_message = f"Error during blog generation: {str(e)}"
        print(error_message)
        return error_message, "", False
