from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel
from serpapi import GoogleSearch

from config.settings import settings
from src.pipeline.ai_generator import get_gemini_llm
from src.pipeline.prompt_builder import PromptBuilder


class UserStepAnalysis(BaseModel):
    blog_outline_completed: bool


class FetchGoogleTrendsDataTool:
    def __init__(self, metadata_json: Dict[str, Any]):
        self.settings = settings
        self.metadata_json = metadata_json
        self.query = metadata_json["topic"]

    def _get_trends_data(self, data_type="TIMESERIES", time_period="today 3-m") -> Dict:
        params = {
            "api_key": self.settings.SERPAPI_KEY,
            "engine": "google_trends",
            "q": self.query,
            "data_type": data_type,
            "date": time_period,
        }
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            base_result = {"query": self.query}

            if data_type == "TIMESERIES":
                return {**base_result, **results.get("interest_over_time", {})}
            elif data_type == "RELATED_QUERIES":
                return {**base_result, **results.get("related_queries", {})}

            return {**base_result, **results}
        except (KeyError, ValueError, TypeError) as e:
            print(f"Error processing trends data: {str(e)}")
            return {"query": self.query}

    def format_trends_for_llm(self, trends_data: Dict) -> Dict:
        formatted_data = {
            "query": trends_data.get("query", ""),
            "trend_summary": {},
            "interest_peaks": [],
            "related_topics": [],
        }

        # Process time periods
        for period_key, period_data in trends_data.get("time_periods", {}).items():
            if not period_data.get("available", False):
                continue

            timeline_data = period_data.get("data", {}).get("timeline_data", [])
            if not timeline_data:
                continue

            peak_points = []
            for point in timeline_data:
                date = point.get("date", "")
                for value in point.get("values", []):
                    if (
                        value.get("query", "") == trends_data.get("query", "")
                        and int(value.get("extracted_value", 0)) > 50
                    ):
                        peak_points.append(
                            {"date": date, "value": value.get("extracted_value", 0)}
                        )

            formatted_data["trend_summary"][period_key] = {
                "period": period_data.get("period", ""),
                "has_significant_interest": bool(peak_points),
                "peak_count": len(peak_points),
                "data_points": len(timeline_data),
            }
            formatted_data["interest_peaks"].extend(peak_points)

        related_keywords = trends_data.get("related_keywords", {}).get("keywords", {})
        for keyword, data in related_keywords.items():
            if "timeline_data" in data:
                peak_value = 0
                peak_date = ""
                for point in data.get("timeline_data", []):
                    for value in point.get("values", []):
                        extracted_value = int(value.get("extracted_value", 0))
                        if extracted_value > peak_value:
                            peak_value = extracted_value
                            peak_date = point.get("date", "")

                if peak_value > 0:
                    formatted_data["related_topics"].append(
                        {
                            "keyword": keyword,
                            "peak_interest": peak_value,
                            "peak_date": peak_date,
                        }
                    )

        formatted_data["insights"] = self._generate_insights(formatted_data)
        return formatted_data

    def get_raw_trends(self) -> str:
        try:
            short_term = self._get_trends_data(
                data_type="TIMESERIES", time_period="today 1-m"
            )
            related_queries = self._get_trends_data(data_type="RELATED_QUERIES")

            if not short_term or not related_queries:
                return "No trends data available for the given topic."

            related_keywords = self._generate_related_keywords()
            related_keyword_trends = {}

            # Get trends for related keywords
            original_query = self.query
            for keyword in related_keywords:
                self.query = keyword
                related_keyword_trends[keyword] = self._get_trends_data(
                    time_period="today 3-m"
                )
            self.query = original_query

            data = {
                "query": self.query,
                "time_periods": {
                    "short_term": {
                        "period": "Last 1 month",
                        "data": short_term,
                        "available": bool(short_term),
                    },
                },
                "related_queries": related_queries,
                "related_keywords": {
                    "keywords": related_keyword_trends,
                    "count": len(related_keyword_trends),
                },
                "meta": {
                    "last_updated": datetime.utcnow().isoformat(),
                    "query_variations_analyzed": len(related_keywords) + 1,
                },
            }

            prompt_builder = PromptBuilder(self.metadata_json, trends_data=data)
            return get_gemini_llm().invoke(prompt_builder.data_trends()).content

        except (KeyError, ValueError, TypeError) as e:
            print(f"Error in get_raw_trends: {str(e)}")
            return "Unable to retrieve trends data for the given topic."

    def _generate_related_keywords(self) -> List[str]:
        base_query = self.query.lower()
        return [
            f"{base_query} requirements",
            f"{base_query} cost",
            f"{base_query} scholarships",
            f"Best {base_query} programs",
            f"{base_query} rankings",
        ]

    def _generate_insights(self, formatted_data: Dict) -> List[str]:
        insights = []

        if formatted_data["interest_peaks"]:
            sorted_peaks = sorted(
                formatted_data["interest_peaks"], key=lambda x: x["value"], reverse=True
            )
            insights.append(
                f"Peak interest in '{formatted_data['query']}' occurred on {sorted_peaks[0]['date']}"
            )
            if len(sorted_peaks) > 1:
                insights.append(
                    f"There were {len(sorted_peaks)} significant spikes in interest over the analyzed periods"
                )
        else:
            insights.append(
                f"Interest in '{formatted_data['query']}' has been relatively steady with no major spikes"
            )

        # Process related topics
        if formatted_data["related_topics"]:
            sorted_topics = sorted(
                formatted_data["related_topics"],
                key=lambda x: x["peak_interest"],
                reverse=True,
            )
            top_related = sorted_topics[0]["keyword"]
            insights.append(
                f"'{top_related}' is a highly related topic with significant interest"
            )
            if len(sorted_topics) > 1:
                other_topics = [
                    topic["keyword"]
                    for topic in sorted_topics[1 : min(4, len(sorted_topics))]
                ]
                insights.append(
                    f"Other related topics of interest include: {', '.join(other_topics)}"
                )
        return insights


class ResearchTool:
    def __init__(self, metadata_json: Dict[str, Any]):
        self.metadata_json = metadata_json

    def get_research(self) -> str:
        prompt_builder = PromptBuilder(metadata_json=self.metadata_json)
        return get_gemini_llm().invoke(prompt_builder.research_prompt()).content


class LLMTrendsTool:
    def __init__(self, metadata_json: Dict[str, Any]):
        self.metadata_json = metadata_json

    def get_llm_trends(self) -> str:
        prompt_builder = PromptBuilder(metadata_json=self.metadata_json)
        return get_gemini_llm().invoke(prompt_builder.llm_trends()).content


class BlogOutlineTool:
    def __init__(
        self,
        metadata_json: Dict[str, Any] = None,
        trends_data: Dict = None,
        research_data: Dict = None,
        user_input: str = None,
    ):
        self.metadata_json = metadata_json
        self.trends_data = trends_data
        self.research_data = research_data
        self.user_input = user_input

    def get_blog_outline(self) -> str:
        prompt_builder = PromptBuilder(
            metadata_json=self.metadata_json,
            trends_data=self.trends_data,
            research_data=self.research_data,
            user_input=self.user_input,
        )
        return get_gemini_llm().invoke(prompt_builder.blog_outline()).content
