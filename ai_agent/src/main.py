from typing import Any, Dict, Optional, Tuple

from config.settings import settings
from src.integrations.tools import (
    BlogOutlineTool,
    FetchGoogleTrendsDataTool,
    LLMTrendsTool,
    ResearchTool,
)
from src.pipeline.ai_generator import get_gemini_llm, get_memory
from src.pipeline.prompt_builder import PromptBuilder
from src.utils.constants import Constants


def memory_handler(
    session_id: str,
    blog_outline: Optional[str] = None,
    trends_data: Optional[Any] = None,
    research_data: Optional[Any] = None,
) -> None:
    """Save data to memory for a session.

    Args:
        session_id: The session ID
        blog_outline: Optional blog outline to save
        trends_data: Optional trends data to save
        research_data: Optional research data to save
    """
    if not (settings.USE_MEMORY and session_id):
        return

    memory = get_memory(session_id=session_id)

    if trends_data:
        memory.set_session_data("trends_data", trends_data)
    if research_data:
        memory.set_session_data("research_data", research_data)
    if blog_outline:
        memory.set_session_data("blog_outline", blog_outline)


def retrieve_data_from_memory(session_id: str) -> Dict[str, Any]:
    """Retrieve data from memory for a session.

    Args:
        session_id: The session ID

    Returns:
        Dict containing trends_data, research_data and blog_outline if available
    """
    if not (settings.USE_MEMORY and session_id):
        return {"trends_data": None, "research_data": None, "blog_outline": None}

    memory = get_memory(session_id=session_id)

    return {
        "trends_data": memory.get_session_data("trends_data"),
        "research_data": memory.get_session_data("research_data"),
        "blog_outline": memory.get_session_data("blog_outline"),
    }


def initialize_ai_tools(
    metadata: Dict[str, Any], find_trends_type: str
) -> Tuple[Any, Any]:
    """Initialize and run AI tools to gather trends and research data.

    Args:
        metadata: The metadata for the blog
        find_trends_type: The type of trends to find

    Returns:
        Tuple of trends_data and research_data
    """
    constants = Constants()
    trends_data = None

    if find_trends_type == constants.FIND_TRENDS_TYPE["GOOGLE_TRENDS"]:
        trends_data = FetchGoogleTrendsDataTool(metadata).get_raw_trends()
    elif find_trends_type == constants.FIND_TRENDS_TYPE["LLM"]:
        trends_data = LLMTrendsTool(metadata).get_llm_trends()

    research_data = ResearchTool(metadata).get_research()

    return trends_data, research_data


def run_blog_generation(
    metadata: Dict[str, Any],
    find_trends_type: str,
    session_id: Optional[str] = None,
    clear_memory: bool = False,
    user_input: Optional[str] = None,
    step: Optional[str] = None,
) -> Tuple[str, str, bool]:
    """Generate a blog based on metadata and optional session data.

    Args:
        metadata: The metadata for the blog
        find_trends_type: The type of trends to find
        session_id: Optional session ID for memory retrieval/storage
        clear_memory: Whether to clear memory for this session
        user_input: Optional user input to incorporate
        step: The step of the blog generation process

    Returns:
        Tuple of (content, content_type, success_flag)
    """
    trends_data = None
    research_data = None
    blog_outline = None

    try:
        if session_id and settings.USE_MEMORY:
            if clear_memory:
                memory = get_memory(session_id=session_id)
                memory.clear()

            stored_data = retrieve_data_from_memory(session_id)
            trends_data = stored_data.get("trends_data")
            research_data = stored_data.get("research_data")
            blog_outline = stored_data.get("blog_outline")

            if not trends_data or not research_data:
                trends_data, research_data = initialize_ai_tools(
                    metadata, find_trends_type
                )

                memory_handler(
                    session_id,
                    trends_data=trends_data,
                    research_data=research_data,
                )

            if step == "blog_outline":
                blog_outline = BlogOutlineTool(
                    metadata, trends_data, research_data, user_input
                ).get_blog_outline()

                memory_handler(session_id, blog_outline=blog_outline)

                print(f"############ Blog outline: \n{blog_outline}\n############")

                return blog_outline, "blog_outline", True

            if step == "generate_blog":
                prompts = PromptBuilder(
                    metadata, blog_outline_data=blog_outline
                ).build_prompt()
                llm = get_gemini_llm()

                blog_sections = [
                    f"{llm.invoke(prompt_template.format(**metadata)).content}\n"
                    for prompt_template in prompts.values()
                ]

                full_blog = "\n".join(blog_sections)

                print(f"############ Full blog: \n{full_blog}\n############")

                return full_blog, "markdown", True

        return "", "", False

    except (KeyError, ValueError, ConnectionError, TimeoutError) as e:
        error_message = f"Error during blog generation: {str(e)}"
        print(error_message)
        return error_message, "", False
