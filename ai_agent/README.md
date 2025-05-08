# AI Blog Writer

An intelligent blog post generator that creates high-quality, SEO-friendly content using LangChain and Gemini, enriched with real-time trend data and AI-powered research capabilities.

## Features

- Advanced AI content generation using Gemini LLM through LangChain
- Professional-grade prompt engineering with dynamic template generation
- Automatic research integration using dedicated AI agents
- Real-time Google Trends data analysis for timely content
- Intelligent word count management based on content type
- Support for multiple blog structures (How-To, Listicle, Comparison, etc.)
- SEO-friendly content with built-in meta description generation

## How It Works

The AI Blog Writer uses a sophisticated pipeline architecture:

1. **Input Processing**: Takes structured metadata about the desired blog post
2. **Research & Trends**: Automatically gathers relevant research and trend data
3. **Prompt Engineering**: Generates tailored prompts for each blog section
4. **AI Content Generation**: Uses Gemini LLM to create high-quality content
5. **Output Formatting**: Delivers content in both Markdown and HTML formats

## Example Usage

Here's how to generate a blog post about education loans for studying in the USA:

```python
from src.main import run_blog_generation

metadata_json = {
    "structure": "guide",  # Options: blog, how-to, listicle, comparison, guide, faq
    "persona": "professional",
    "topic": "Education Loan for Study in USA",
    "tone": "professional",
    "keyword": "Education Loan for Study in USA",
    "goal": "Provide comprehensive information about education loan options for students planning to study in the USA"
}

# Generate the blog post
blog_markdown, blog_text, blog_html, success = run_blog_generation(metadata_json)

# If successful, use the content as needed
if success:
    print(blog_markdown)  # Markdown version for editing
    # Or use blog_html for web publishing
```

## Prerequisites

- Python 3.9+
- Google Cloud Project with Gemini API enabled
- SerpAPI key for Google Trends data
- (Optional) Database for content storage

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Rishabh250/ai-blog-writer.git
cd ai-blog-writer
```

2. Create a virtual environment and activate it:

```bash
uv init
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies using uv (faster, more reliable Python package installer):

```bash
# Install dependencies with uv
uv install -r requirements.txt
```

Alternatively, you can use pip:

```bash
uv install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file with the following variables:

```
GOOGLE_API_KEY=your_google_api_key
SERPAPI_KEY=your_serpapi_key
LLM_MODEL=gemini-1.5-flash
DATABASE_URI=your_database_uri
GOOGLE_DRIVE_FOLDER_ID=your_folder_id (optional)
DEBUG=False
LOG_LEVEL=INFO
```

## Usage

### Method 1: Import in Your Code

```python
from src.main import run_blog_generation

metadata_json = {
    "structure": "blog",
    "persona": "professional",
    "topic": "Your Topic",
    "tone": "professional",
    "keyword": "Your Keyword",
    "goal": "Your Goal"
}

blog_markdown, blog_text, blog_html, success = run_blog_generation(metadata_json)
```

### Method 2: Create a Simple Interface

Create a file called `generate.py` in the project root with this content:

```python
from src.main import run_blog_generation
import json
import sys

def main():
    if len(sys.argv) < 2:
        print("Please provide a JSON file with blog metadata")
        return
    
    with open(sys.argv[1], 'r') as f:
        metadata = json.load(f)
    
    blog_markdown, blog_text, blog_html, success = run_blog_generation(metadata)
    
    if success:
        output_file = metadata.get('output_file', 'output_blog.md')
        with open(output_file, 'w') as f:
            f.write(blog_markdown)
        print(f"Blog successfully written to {output_file}")
    else:
        print(f"Error: {blog_markdown}")

if __name__ == "__main__":
    main()
```

Then run:

```bash
python generate.py your_metadata.json
```

## Project Structure

The AI Blog Writer follows a modular architecture with clearly separated components:

```text
ai-blog-writer/
│
├── config/                     # Configuration files
│   └── settings.py             # Environment settings (API keys, DB URI, etc.)
│
├── src/                        # Main application logic
│   ├── __init__.py
│   ├── main.py                 # Core blog generation functions and entry point
│   │
│   ├── pipeline/               # Pipeline components
│   │   ├── __init__.py
│   │   ├── prompt_builder.py   # Creates dynamic prompts with BlogLengthManager
│   │   ├── ai_generator.py     # Manages LLM integration via LangChain
│   │   └── validator.py        # Validates input metadata
│   │
│   ├── integrations/           # External service integrations
│   │   ├── __init__.py
│   │   ├── tools.py            # Google Trends and AI Research tools
│   │   ├── database.py         # Optional database connectivity
│   │   └── google_docs.py      # Optional Google Drive export
│   │
│   └── utils/                  # Helper utilities
│       ├── __init__.py
│       ├── constants.py        # Global constants and configurations
│       └── helpers.py          # Utility functions (markdown conversion, etc.)
│___ app.py                     # Main application file
│___ config.py                  # Configuration file
│___ requirements.txt           # Python dependencies
│___ pyproject.toml             # Modern Python project configuration
│___ .env.example               # Example environment variables (template)
│___ .env                       # Actual environment variables (gitignored)
│___ .gitignore                 # Git ignore file
│___ README.md                  # Project README
```

### Key Files

- **main.py**: Contains the core `run_blog_generation()` function for generating blog content
- **prompt_builder.py**: Defines the `PromptBuilder` class that creates dynamic prompts for each blog section
- **tools.py**: Integrates external tools like Google Trends analysis and AI-powered research

### Blog Structure Types

| Structure Type | Ideal Word Count | Notes                                       |
| -------------- | ---------------- | ------------------------------------------- |
| **How-To**     | 1200–1800 words  | Step-by-step detail is key                  |
| **Listicle**   | 1000–1500 words  | 7–10 list items, each \~100–150 words       |
| **Comparison** | 1300–1800 words  | Multiple feature breakdowns, pros/cons      |
| **Guide**      | 1800–2500 words  | In-depth; includes sections, examples, FAQs |
| **FAQ**        | 1000–1400 words  | 8–12 questions, each with a concise answer  |

## Key Technical Details

### PromptBuilder

The `PromptBuilder` class is responsible for generating tailored prompts for each blog section. It:

- Adapts to different blog structure types
- Incorporates Google Trends data and research
- Provides word count guidelines based on content type
- Creates separate prompts for each section of the blog post

### External Tools Integration

- **FetchGoogleTrendsDataTool**: Retrieves and analyzes real-time trends data
- **ResearchTool**: Uses LLM to conduct targeted research for the blog topic

### LangChain Integration

The project uses LangChain for:

- Converting PromptTemplate objects to formatted strings
- Managing LLM interactions efficiently
- Processing outputs and handling errors


## Common Issues and Solutions

- **PromptTemplate Formatting**: Ensure PromptTemplate objects are converted to strings using the `format()` method before passing to LangChain agents
- **API Rate Limits**: Google Trends API (via SerpAPI) and Gemini API have rate limits that may affect production usage
- **Error Handling**: The system includes robust error handling but may need adjustment for specific edge cases

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE file](LICENSE) for details.