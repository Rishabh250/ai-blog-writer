from langchain.prompts import PromptTemplate

class PromptBuilder:
    def __init__(self, metadata_json):
        self.metadata_json = metadata_json

    def build_prompt(self):
        prompt = PromptTemplate(
            input_variables=["structure", "persona", "topic", "tone", "keyword", "goal"],
            template=(
                "You are an expert blog writer with over 30 years of experience crafting compelling, SEO-friendly content "
                "for global product companies. Your goal is to write a well-researched, engaging, and human-sounding blog post.\n\n"
                "Assume you’ve done thorough keyword research from the latest web search results.\n"
                "Incorporate natural language, real-world examples, and a conversational tone.\n\n"
                "Write a {structure} style blog post for {persona} about '{topic}' in a {tone} tone.\n"
                "Focus keyword: {keyword}. The goal of the blog is to: {goal}.\n\n"
                "Ensure the introduction is emotionally compelling, the body is clear and structured, "
                "and the conclusion includes a clear call-to-action.\n\n"
                "Avoid sounding robotic or generic. This content should feel as if it was written by a human with deep understanding."
            )
        )
        return prompt
