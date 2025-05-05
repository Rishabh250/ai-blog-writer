from langchain.prompts import PromptTemplate
from typing import Dict, Any

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
        return min_words, max_words


class PromptBuilder:
    def __init__(self, metadata_json: Dict[str, Any], **kwargs):
        self.metadata_json = metadata_json
        self.length_manager = BlogLengthManager(metadata_json.get("structure", "blog"))
        self.trends_data = kwargs.get("trends_data", None)

        min_words, max_words = self.length_manager.get_word_limit_instruction()
        self.metadata_json["min_words"] = min_words
        self.metadata_json["max_words"] = max_words

    def build_prompt(self):
        prompt = PromptTemplate(
            input_variables=["structure", "persona", "topic", "tone", "keyword", "goal", "min_words", "max_words"],
            template=(
                "You're a seasoned blog writer with a personal voice — not a perfect machine.\n\n"
                "Write a {structure} article between {min_words} and {max_words} words for {persona}.\n"
                "Topic: {topic}\n"
                "Tone: {tone}\n"
                "Keyword to naturally include: {keyword}\n"
                "Conversion goal: {goal}\n\n"
                "Here's some trend data about the topic that might be helpful:\n"
                "Start with a surprising fact or a short story that relates to the topic — something from a real-world experience (e.g., 'When I applied for my first loan...').\n"
                "Break the content into natural sections, but avoid sounding robotic.\n"
                "Occasionally use contractions, casual phrasing, or rhetorical questions.\n"
                "It's okay to leave minor imperfection — don't over-polish.\n\n"
                "End with a clear takeaway, but don't label it 'conclusion'. Keep it personal.\n"
            )
        )
        return prompt

    def data_trends(self):
        prompt_text = f"""
        Analyze the following Google Trends data related to "{self.metadata_json['topic']}":

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
