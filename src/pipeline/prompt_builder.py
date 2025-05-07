from typing import Any, Dict

from langchain.prompts import PromptTemplate


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
        self.length_manager = BlogLengthManager(metadata_json.get("structure", "blog"))
        self.trends_data = kwargs.get("trends_data", None)
        self.research_data = kwargs.get("research_data", None)

        self.metadata_json["min_words"], self.metadata_json["max_words"] = (
            self.length_manager.get_ideal_word_count()
        )

    def get_blog_structure_steps(self, structure: str):
        structure = structure.lower()

        steps = {
            "blog": [
                "Introduction",
                "Main Content",
                "Conclusion",
                "FAQs",
                "Meta Description",
                "References",
            ],
            "how-to": [
                "Introduction",
                "Step-by-Step Guide",
                "Tips & Best Practices",
                "Conclusion",
                "FAQs",
                "Meta Description",
                "References",
            ],
            "listicle": [
                "Introduction",
                "List Items with Details",
                "Conclusion",
                "FAQs",
                "Meta Description",
                "References",
            ],
            "comparison": [
                "Introduction",
                "Criteria for Comparison",
                "Detailed Comparison",
                "Pros & Cons",
                "Conclusion",
                "FAQs",
                "Meta Description",
                "References",
            ],
            "guide": [
                "Introduction",
                "Detailed Guide Sections",
                "Expert Tips",
                "Conclusion",
                "FAQs",
                "Meta Description",
                "References",
            ],
            "faq": [
                "Introduction",
                "Comprehensive FAQ Section",
                "Conclusion",
                "Meta Description",
                "References",
            ],
        }

        return steps.get(
            structure,
            ["Introduction", "Main Content", "Conclusion", "FAQs", "Meta Description"],
        )

    def build_prompt(self):
        steps = self.get_blog_structure_steps(self.metadata_json["structure"])
        prompts = {}

        for section in steps:
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
                    "- Intended Audience: {persona}\n"
                    f"{trends_text}\n"
                    f"{research_text}\n"
                    "Writing Guidelines:\n"
                    f"{guidelines}"
                    "Keep the language fluid, insightful, and grounded. Avoid generic phrasing and overly polished structure.\n"
                    "Avoid using placeholder phrases such as 'Okay, here's...' or 'Let me...' at the beginning of sections.\n"
                    "Write in a professional, third-person voice with a touch of authenticity.\n"
                    "Use the research tool to get research insights for the blog post and only do research when needed, tool name is 'research_tool'.\n"
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
