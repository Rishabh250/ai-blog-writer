# AI Blog Writer

An intelligent blog post generator that creates high-quality, SEO-friendly content using AI, with seamless integration for content management.

## Features

- Advanced AI content generation using Gemini 2.0
- Professional-grade prompt engineering for better content quality
- Flexible content structure customization
- Input validation and schema-based processing
- Modular pipeline architecture for easy extensibility
- Support for various content types and topics

## Example Usage

Here's an example of generating a blog post about education loans for studying in the USA:

```python
metadata_json = {
    "structure": "blog",
    "persona": "professional",
    "topic": "Education Loan for Study in USA",
    "tone": "professional",
    "keyword": "Education Loan for Study in USA",
    "goal": "Education Loan for Study in USA"
}

# The prompt builder now uses a more sophisticated template:
"""
You are an expert blog writer with over 30 years of experience crafting compelling, SEO-friendly content 
for global product companies. Your goal is to write a well-researched, engaging, and human-sounding blog post.

Assume you've done thorough keyword research from the latest web search results.
Incorporate natural language, real-world examples, and a conversational tone.

Write a {structure} style blog post for {persona} about '{topic}' in a {tone} tone.
Focus keyword: {keyword}. The goal of the blog is to: {goal}.

Ensure the introduction is emotionally compelling, the body is clear and structured, 
and the conclusion includes a clear call-to-action.

Avoid sounding robotic or generic. This content should feel as if it was written by a human with deep understanding.
"""

## Prerequisites

- Python 3.9+
- Google Cloud Project with Gemini API enabled
- Google Drive API credentials
- MongoDB/Supabase instance

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Rishabh250/ai-blog-writer.git
cd ai-blog-writer
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with the following variables:
```
GOOGLE_API_KEY=your_google_api_key
LLM_MODEL=gemini-1.5-flash
DATABASE_URI=your_database_uri
GOOGLE_DRIVE_FOLDER_ID=your_folder_id
DEBUG=False
LOG_LEVEL=INFO
```

## Usage

Run the main script:
```bash
python src/main.py
```

Example usage:
```python
metadata_json = {
    "structure": "blog",
    "persona": "professional",
    "topic": "Your Topic",
    "tone": "professional",
    "keyword": "Your Keyword",
    "goal": "Your Goal"
}

# The script will generate a blog post using the Gemini LLM model
# and print the result to the console
```

## Project Structure

```
ai-blog-writer/
│
├── config/                     # Configuration files
│   ├── settings.py             # Environment-based settings (API keys, DB URI, etc.)
│
├── src/                        # Main application logic
│   ├── __init__.py
│   ├── main.py                 # Main entry point
│   │
│   ├── pipeline/               # Pipeline components
│   │   ├── __init__.py
│   │   ├── prompt_builder.py   # Advanced prompt engineering
│   │   ├── ai_generator.py     # Gemini LLM integration
│   │   └── validator.py        # Input validation
│   │
│   ├── integrations/           # External service integrations
│   │   ├── __init__.py
│   │   ├── database.py         # Database integration
│   │   └── google_docs.py      # Google Drive integration
│   │
│   └── utils/                  # Helper functions
│       ├── __init__.py
│       ├── constants.py        # Constants and configurations
│       └── helpers.py          # Utility functions
│
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (ignored via .gitignore)
├── .gitignore
└── README.md
```

### Blog Structure Types:
| Structure Type | Ideal Word Count | Notes                                       |
| -------------- | ---------------- | ------------------------------------------- |
| **How-To**     | 1200–1800 words  | Step-by-step detail is key                  |
| **Listicle**   | 1000–1500 words  | 7–10 list items, each \~100–150 words       |
| **Comparison** | 1300–1800 words  | Multiple feature breakdowns, pros/cons      |
| **Guide**      | 1800–2500 words  | In-depth; includes sections, examples, FAQs |
| **FAQ**        | 1000–1400 words  | 8–12 questions, each with a concise answer  |


## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.