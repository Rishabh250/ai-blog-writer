from typing import Any, Dict

from langchain.prompts import PromptTemplate

from src.utils.constants import Constants


class BlogLengthManager:
    def __init__(self, structure_type):
        self.structure_type = structure_type.lower()

    def get_ideal_word_count(self):
        mapping = {
            "how-to": (1200, 1800),
            "listicle": (1000, 1500),
            "comparison": (1300, 1800),
            "guide": (1800, 2500),
            "faq": (1000, 1400),
            "blog": (1000, 1600),
        }

        return mapping.get(self.structure_type, (1000, 1600))

    def get_word_limit_instruction(self):
        min_words, max_words = self.get_ideal_word_count()
        return f"Write between {min_words} and {max_words} words."


class PromptBuilder:
    def __init__(self, metadata_json: Dict[str, Any], **kwargs):
        self.metadata_json = metadata_json
        self.user_input = kwargs.get("user_input", None)
        self.length_manager = BlogLengthManager(metadata_json.get("structure", "blog"))
        self.trends_data = kwargs.get("trends_data", None)
        self.research_data = kwargs.get("research_data", None)
        self.blog_outline_data = kwargs.get("blog_outline_data", None)
        self.steps = self.get_blog_structure_steps(
            metadata_json.get("structure", "blog")
        )

        self.metadata_json["min_words"], self.metadata_json["max_words"] = (
            self.length_manager.get_ideal_word_count()
        )

    def get_blog_structure_steps(self, structure: str):
        structure = structure.lower()

        steps = Constants.STRUCTURE_STEPS.get(structure, [])

        return steps

    def build_prompt(self):
        prompts = {}

        for section in self.steps:
            trends_text = (
                f"\nTrend insights to consider (summarized):\n{self.trends_data}\n"
                if self.trends_data
                and section.lower()
                in ["introduction", "main content", "guide body", "step-by-step guide"]
                else ""
            )

            research_text = (
                f"\nResearch insights to consider (summarized):\n{self.research_data}\n"
                if self.research_data
                and section.lower()
                in ["introduction", "main content", "guide body", "step-by-step guide"]
                else ""
            )

            blog_outline_text = (
                f"\nBlog outline to consider:\n{self.blog_outline_data}\n"
                if self.blog_outline_data
                and section.lower()
                in ["introduction", "main content", "guide body", "step-by-step guide"]
                else ""
            )

            if section.lower() == "meta description":
                guidelines = "- Write a natural-sounding, SEO-optimized meta description (150–160 characters) that clearly conveys the article's value.\n"
            elif section.lower() == "faqs":
                guidelines = "- List 3–5 unique, practical FAQs with clear, non-repetitive answers that address common reader concerns.\n"
            else:
                guidelines = (
                    "- Begin with a relatable or thought-provoking opening line if relevant.\n"
                    "- Use natural phrasing and varied sentence lengths to engage readers.\n"
                    "- Integrate keywords contextually, without sounding robotic.\n"
                    "- Include real-world examples, statistics, or quotes where appropriate.\n"
                    "- Use subheadings for clarity, and ensure smooth transitions between ideas.\n"
                )

            template = PromptTemplate(
                input_variables=[
                    "structure",
                    "persona",
                    "topic",
                    "tone",
                    "keyword",
                    "goal",
                ],
                template=(
                    f"You are a highly experienced human blog writer, not an AI.\n"
                    f"Write only the **{section}** section of a {self.metadata_json['structure']} article.\n"
                    "Your writing must sound completely human and avoid common AI patterns.\n\n"
                    "Content Brief:\n"
                    "- Topic: {topic}\n"
                    "- Tone: {tone}\n"
                    "- Primary Keyword: {keyword}\n"
                    "- Purpose: {goal}\n"
                    "- Intended Audience: {persona}\n\n"
                    f"{blog_outline_text}\n"
                    f"{trends_text}\n"
                    f"{research_text}\n"
                    "Writing Guidelines:\n"
                    f"{guidelines}"
                    "Keep the language fluid, insightful, and grounded. Avoid generic phrasing and overly polished structure.\n"
                    "Avoid using placeholder phrases such as 'Okay, here's...' or 'Let me...' at the beginning of sections.\n"
                    "Write in a professional, third-person voice with a touch of authenticity.\n"
                ),
            )

            prompts[section] = template

        return prompts

    def data_trends(self):
        prompt_text = f"""
        Analyze the following Google Trends data related to "{self.metadata_json["topic"]}":

        {self.trends_data}

        Your analysis should include:
        1. A brief summary of the overall trend.
        2. Key patterns such as spikes, declines, or sustained interest.
        3. Notable regions, time periods, or search terms driving the trend.
        4. Possible reasons behind the observed patterns.
        5. Actionable insights for marketing, content planning, or strategy.

        Provide a clear and well-organized report.
        """

        return prompt_text

    def research_prompt(self):
        prompt_text = f"""
        You are a Research Agent supporting blog content creation.

        Goal: "{self.metadata_json["goal"]}"
        Topic: "{self.metadata_json["topic"]}"

        Research Objectives:
        1. Summarize the topic's current landscape and relevance.
        2. Identify key trends, controversies, or recent developments.
        3. Highlight authoritative sources, influential figures, or organizations in this field.
        4. Uncover statistics, case studies, or examples that illustrate important points.
        5. Explore different perspectives or approaches to the topic.
        6. Identify potential challenges or criticisms related to the topic.
        7. Maximum size of the research should be less than 300 words.

        Provide actionable insights for blog writers:
        - Suggest compelling angles or hooks for the blog post
        - Recommend subtopics or sections to cover
        - Propose questions the blog post should address
        - Identify key terms or concepts to explain

        Present findings in a clear, structured format optimized for blog writing.
        """

        return prompt_text

    def llm_trends(self):
        prompt_text = f"""
        You are a Blog Content Trend Analyst. Analyze current content and market trends related to "{self.metadata_json["topic"]}" to help create engaging blog content.

        Please provide:
        1. Content Trends
           - What types of content formats are performing well for this topic?
           - Which angles or perspectives are readers most interested in?
           - What questions are people commonly asking?
           - Which subtopics are trending in blog discussions?

        2. Audience Interest
           - What specific aspects of {self.metadata_json["topic"]} are gaining traction?
           - Which pain points or challenges are readers seeking solutions for?
           - What level of knowledge does the target audience typically have?
           - Which related topics do readers often explore?

        3. Content Opportunities
           - What gaps exist in current blog coverage?
           - Which unique angles could differentiate our content?
           - What expert insights or data could add value?
           - Which keywords or phrases should we focus on?

        4. Engagement Factors
           - What type of headlines are attracting readers?
           - Which content elements (examples, case studies, statistics) resonate most?
           - What content length and structure works best?
           - Which calls-to-action are effective?

        5. Recommendations
           - Suggest 3-5 specific blog angles or approaches
           - Recommend content elements to include
           - Propose ways to make the content stand out
           - Identify potential sources or references

        Note: Add some references links to the content to make it more engaging and informative.

        Focus on actionable insights that will help create engaging, relevant, and valuable blog content.
        Maximum length: 300 words.
        """

        return prompt_text

    def blog_outline(self):
        trends_text = (
            f"\nTrend insights to consider (summarized):\n{self.trends_data}\n"
            if self.trends_data
            else ""
        )

        research_text = (
            f"\nResearch insights to consider (summarized):\n{self.research_data}\n"
            if self.research_data
            else ""
        )

        user_input = (
            f"\nUser input to consider:\n{self.user_input}\n" if self.user_input else ""
        )

        word_limit_instruction = self.length_manager.get_word_limit_instruction()

        prompt_text = f"""
        You are a Blog Outline Generator, an expert at creating comprehensive and engaging blog outlines.

        Your task is to generate a detailed, well-structured outline for a blog post with the following specifications:

        Topic: "{self.metadata_json["topic"]}"
        Goal: "{self.metadata_json["goal"]}"
        Structure Type: "{self.metadata_json.get("structure", "blog")}"
        Target Persona: "{self.metadata_json.get("persona", "professional")}"
        Desired Tone: "{self.metadata_json.get("tone", "informative")}"

        {trends_text}
        {research_text}
        {user_input}

        Please create an outline that:
        1. Follows this structural flow: {self.steps}
        2. Includes clear, descriptive headings and subheadings
        3. Highlights key points to be covered under each section
        4. Ensures logical flow and progression of ideas
        5. Incorporates relevant keywords naturally
        6. Addresses the target audience's needs and pain points
        7. Maintains consistency with the desired tone and style
        8. Includes placeholders for examples, statistics, or case studies where appropriate
        9. Add some references links to the content to make it more engaging and informative.

        For each major section, provide:
        - Main topic/focus
        - 2-3 key points to cover
        - Suggested supporting elements (examples, data, quotes)
        - Transition notes to ensure smooth flow

        Format the outline using clear hierarchical structure (e.g., I, A, 1, a).
        Aim for an outline that would support content of {word_limit_instruction}

        Important:
        - Present only the outline structure. Do not include introductory text like "Here's a detailed blog post outline designed to educate professionals about [topic]" in your response.
        - Do not include any other text in your response.
        """

        return prompt_text
