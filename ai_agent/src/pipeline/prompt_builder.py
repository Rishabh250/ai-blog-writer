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

    def build_prompt(self) -> Dict[str, PromptTemplate]:
        """
        Constructs a dictionary of Langchain PromptTemplates, one for each
        section defined in the blog structure steps, tailored for professional
        content generation.

        Returns:
            Dict[str, PromptTemplate]: A dictionary where keys are section names
                                       and values are the corresponding PromptTemplates.
        """
        prompts = {}
        # Define sections where contextual data (trends, research, outline) is most relevant
        context_relevant_sections = {
            "introduction",
            "main content",
            "guide body",
            "step-by-step guide",
            "meta description",
            "faqs",
        }

        # Safely retrieve the structure type, defaulting to 'blog'
        structure_type = self.metadata_json.get("structure", "blog")

        for section in self.steps:
            section_lower = section.lower()
            include_context = section_lower in context_relevant_sections

            # Prepare contextual information strings, only if data exists and section is relevant
            trends_text = (
                f"\n**Trend Insights (Summary):**\n{self.trends_data}\n"
                if self.trends_data and include_context
                else ""
            )
            research_text = (
                f"\n**Research Insights (Summary):**\n{self.research_data}\n"
                if self.research_data and include_context
                else ""
            )
            blog_outline_text = (
                f"\n**Blog Outline Reference:**\n{self.blog_outline_data}\n"
                if self.blog_outline_data and include_context
                else ""
            )

            # Define section-specific writing guidelines
            if section_lower == "meta description":
                guidelines = (
                    "- Craft a compelling, SEO-optimized meta description (150–160 characters).\n"
                    "- Ensure it accurately reflects the article's core value and encourages clicks.\n"
                    "- Integrate the primary keyword naturally.\n"
                )
            elif section_lower == "faqs":
                guidelines = (
                    "- Develop 3–5 unique and practical FAQs relevant to the main topic.\n"
                    "- Provide clear, concise, and non-repetitive answers.\n"
                    "- Address potential reader questions or concerns effectively.\n"
                )
            else:
                # General guidelines for body sections
                guidelines = (
                    "- Initiate with an engaging hook (e.g., relatable scenario, compelling statistic, thought-provoking question) appropriate for the section.\n"
                    "- Employ natural, fluent language and vary sentence structure to maintain reader interest.\n"
                    "- Seamlessly integrate the primary keyword and related terms where contextually appropriate, avoiding keyword stuffing.\n"
                    "- Incorporate credible evidence (e.g., statistics, real-world examples, expert quotes) to substantiate claims.\n"
                    "- Utilize subheadings (H2, H3, etc.) to organize content logically and enhance readability.\n"
                    "- Ensure smooth, logical transitions between paragraphs and ideas.\n"
                )

            # Construct the prompt template for the current section
            # Note: Using .get() for metadata access within the f-string for robustness
            template_str = (
                f"**Role:** Assume the persona of an expert Human Blog Writer specializing in '{self.metadata_json.get('topic', 'the specified topic')}'.\n"
                f"**Task:** Generate **only** the content for the '{section}' section of a '{structure_type}' article.\n"
                f"**Critical Instruction:** Your writing style *must* be indistinguishable from high-quality human writing. Avoid AI-like patterns, generic statements, excessive formality, or robotic phrasing. Prioritize authenticity, clarity, depth, and reader engagement.\n\n"
                f"**Content Brief:**\n"
                f"- Article Topic: {{topic}}\n"
                f"- Target Audience: {{persona}}\n"
                f"- Desired Tone: {{tone}}\n"
                f"- Primary Keyword Focus: {{keyword}}\n"
                f"- Core Objective: {{goal}}\n\n"
                f"**Contextual Information (Leverage if provided and relevant to this specific '{section}' section):**"
                f"{blog_outline_text}"
                f"{trends_text}"
                f"{research_text}\n"
                f"**Specific Writing Guidelines for the '{section}' Section:**\n"
                f"{guidelines}\n"
                f"**Overall Stylistic Requirements:**\n"
                f"- Maintain a professional, authoritative, yet accessible third-person voice (unless persona dictates otherwise).\n"
                f"- Focus on delivering insightful, valuable content with fluid prose.\n"
                f"- **Strictly avoid** introductory filler phrases (e.g., 'Certainly, here is...', 'Okay, let's craft...', 'In this section...'). Begin writing the section content directly.\n"
            )

            # Create the PromptTemplate instance
            template = PromptTemplate(
                input_variables=[
                    # Variables expected to be filled in from metadata or other sources
                    "persona",
                    "topic",
                    "tone",
                    "keyword",
                    "goal",
                    # 'structure' is available via self.metadata_json but kept here for potential direct use
                    "structure",
                ],
                template=template_str,
            )

            prompts[section] = template

        return prompts

    def data_trends(self):
        prompt_text = f"""
        You are a professional Data Analyst tasked with interpreting Google Trends data.

        **Objective:** Conduct a comprehensive analysis of the provided Google Trends data for the topic "{self.metadata_json["topic"]}" to derive actionable insights for content strategy and marketing efforts.

        **Input Data:**
        Google Trends data related to "{self.metadata_json["topic"]}":
        ```
        {self.trends_data}
        ```

        **Analysis Requirements:**
        Your report must address the following key areas in a structured manner:

        1.  **Executive Summary:** A brief overview summarizing the core findings and overall trend direction.
        2.  **Detailed Trend Analysis:** Identify and elaborate on significant patterns, including:
            *   Periods of peak interest (spikes) and potential catalysts.
            *   Periods of declining interest and potential reasons.
            *   Evidence of seasonality or sustained interest levels.
        3.  **Geographic and Temporal Insights:** Highlight notable variations in interest across different regions and time periods. Pinpoint specific search terms or related queries that are driving the trends, if available in the data.
        4.  **Causal Factors (Hypothesized):** Propose plausible explanations for the observed trends and patterns, considering potential market events, news cycles, or other external influences.
        5.  **Strategic Implications & Recommendations:** Translate the analysis into actionable recommendations for:
            *   Marketing campaign timing and focus.
            *   Content creation themes and topic prioritization.
            *   Broader business or content strategy adjustments.

        **Output Format:**
        Deliver a clear, concise, and professionally structured report. Ensure all conclusions are data-driven and insights are directly applicable to strategic planning.
        """

        return prompt_text

    def research_prompt(self):
        prompt_text = f"""
        **Role:** You are a Senior Research Analyst tasked with providing foundational research for high-quality blog content creation.

        **Objective:** Conduct thorough background research on the specified topic to inform the writing process and ensure accuracy, depth, and relevance.

        **Context:**
        - **Blog Goal:** "{self.metadata_json["goal"]}"
        - **Primary Topic:** "{self.metadata_json["topic"]}"

        **Research Mandate:**
        1.  **Current Landscape & Relevance:** Provide a concise overview of the current landscape and establish the topic's relevance.
        2.  **Trends & Developments:** Identify significant current trends, ongoing controversies, and notable recent developments.
        3.  **Authorities & Influencers:** Pinpoint key authoritative sources, influential thought leaders, and prominent organizations within this domain.
        4.  **Supporting Evidence:** Compile pertinent statistics, relevant case studies, and illustrative examples to substantiate key points.
        5.  **Perspectives & Approaches:** Analyze diverse perspectives and methodologies related to the topic.
        6.  **Challenges & Criticisms:** Outline potential challenges, limitations, or criticisms associated with the topic.

        **Actionable Recommendations for Blog Content:**
        Based on your research, provide specific, actionable insights for the blog writer:
        - **Compelling Angles:** Propose unique and compelling narrative angles or hooks to capture reader interest.
        - **Content Structure:** Recommend essential subtopics and a logical structure for the blog post.
        - **Key Questions:** Formulate critical questions the blog post should aim to answer for the target audience.
        - **Terminology:** Identify crucial terms or concepts requiring clear explanation.

        **Output Requirements:**
        - Present findings in a clear, structured, and easily digestible format, optimized for direct use by blog writers.
        - Ensure all information is accurate and verifiable where possible.
        - Deliver a comprehensive yet concise summary, strictly adhering to a **maximum length of 300 words**. Focus on impactful information.
        """

        return prompt_text

    def llm_trends(self):
        prompt_text = f"""
        **Role:** Senior Market Research Analyst specializing in Digital Content Trends.

        **Objective:** Conduct a comprehensive analysis of current content and market trends related to the topic "{self.metadata_json["topic"]}". The goal is to identify strategic insights and actionable recommendations for developing high-impact, engaging, and differentiated blog content.

        **Analysis Requirements:**

        Please provide a structured report covering the following areas:

        1.  **Current Content Landscape & Performance:**
            *   Identify dominant content formats (e.g., tutorials, case studies, opinion pieces, data reports) successfully employed for "{self.metadata_json["topic"]}".
            *   Analyze prevailing angles, narratives, and perspectives resonating most strongly with the target audience.
            *   Determine the most frequently asked questions and search queries related to this topic.
            *   Pinpoint trending subtopics and niche areas within the broader "{self.metadata_json["topic"]}" discussion.

        2.  **Target Audience Insights:**
            *   Detail specific facets or sub-themes of "{self.metadata_json["topic"]}" currently experiencing heightened audience interest or engagement.
            *   Identify key reader pain points, challenges, or aspirations that content within this topic area should address.
            *   Assess the typical knowledge level and sophistication of the target audience for this topic.
            *   Map out related topics, interests, or adjacent fields commonly explored by the audience.

        3.  **Strategic Content Opportunities:**
            *   Identify underserved areas or content gaps within the existing blog coverage of "{self.metadata_json["topic"]}".
            *   Propose unique, differentiated angles or value propositions to distinguish future content.
            *   Suggest types of expert insights, proprietary data, or original research that could significantly enhance content value.
            *   Recommend primary and secondary keywords/phrases exhibiting high potential for organic visibility and relevance.

        4.  **Engagement & Optimization Factors:**
            *   Analyze characteristics of high-performing headlines and titles within this topic space.
            *   Evaluate the impact of specific content elements (e.g., data visualizations, expert quotes, interactive elements, case studies, practical examples) on reader engagement.
            *   Provide recommendations on optimal content length, structure, and formatting based on current best practices for "{self.metadata_json["topic"]}".
            *   Identify effective call-to-action (CTA) strategies relevant to the topic and audience.

        5.  **Actionable Recommendations:**
            *   Propose 3-5 specific, well-rationalized blog post concepts or strategic approaches.
            *   Recommend essential content elements, data points, or expert perspectives to incorporate for maximum impact.
            *   Suggest concrete strategies to ensure the content stands out from competitors.
            *   Identify credible sources, potential expert contributors, or relevant data repositories for reference and validation. Include examples of high-quality reference links where applicable.

        **Output Guidelines:**
        *   Focus strictly on actionable, data-informed insights directly applicable to blog content strategy and creation.
        *   Maintain a professional, analytical tone.
        *   Ensure the total response length does not exceed 300 words.
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
        **Role:** Expert Content Strategist specializing in Blog Architecture.

        **Objective:** Generate a comprehensive, strategically sound, and highly detailed outline for a blog post based on the provided specifications. The outline must serve as a robust blueprint for content creation, adhering strictly to the required format and constraints.

        **Input Specifications:**
        *   **Topic:** "{self.metadata_json["topic"]}"
        *   **Primary Goal:** "{self.metadata_json["goal"]}"
        *   **Content Structure Type:** "{self.metadata_json.get("structure", "blog")}"
        *   **Target Audience Persona:** "{self.metadata_json.get("persona", "professional")}"
        *   **Desired Tone:** "{self.metadata_json.get("tone", "informative")}"
        *   **Mandatory Structural Flow:** {self.steps}
        *   **Target Word Count Guidance:** {word_limit_instruction}
        *   **Primary Keyword (if provided):** "{self.metadata_json.get("keyword", "N/A")}"

        **Contextual Data (Incorporate these insights):**
        {trends_text}
        {research_text}
        {user_input}

        **Outline Requirements:**
        1.  **Structural Adherence:** Strictly follow the specified structural flow: {self.steps}.
        2.  **Headings & Subheadings:** Craft clear, compelling, and descriptive headings/subheadings. Optimize for readability and potential SEO value where appropriate.
        3.  **Section Depth:** For each major section defined in the structural flow, detail:
            *   The core focus or main topic.
            *   2-4 substantive key points, arguments, or steps to be elaborated upon.
            *   Suggestions for supporting elements (e.g., specific data points, types of examples, potential case studies, relevant statistics, expert quotes).
        4.  **Logical Progression:** Ensure a seamless and logical flow of information between sections and points, facilitating reader comprehension.
        5.  **Keyword Integration:** Naturally integrate the primary keyword and related terms throughout the outline's suggested content points.
        6.  **Audience & Goal Alignment:** Directly address the needs, pain points, and knowledge level of the "{self.metadata_json.get("persona", "professional")}" persona. Ensure the outline structure and content points clearly support achieving the stated "{self.metadata_json["goal"]}".
        7.  **Tone Consistency:** Reflect the specified "{self.metadata_json.get("tone", "informative")}" in the nature and framing of the outlined points.
        8.  **Actionability & Value:** Design an outline that guides the creation of practical, valuable, and engaging final content for the target audience.
        9.  **Source Integration:** Indicate logical points within the outline where incorporating credible references, data, or external links would enhance authority and reader value.

        **Output Format & Constraints:**
        *   **Format:** Utilize a clear hierarchical structure (e.g., I., A., 1., a.).
        *   **Content:** Output *only* the structured outline.
        *   **Exclusions:** CRITICAL - Do NOT include any introductory sentences (e.g., "Here is the outline...", "Okay, here's the structure..."), concluding remarks, summaries, or any text whatsoever outside the hierarchical outline structure itself. The response MUST begin directly with the first heading/point of the outline (e.g., "I. Introduction").
        """

        return prompt_text
