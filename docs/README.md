# AI Blog Writer Documentation

This project uses AI to generate blog content. It integrates with various services including Google Docs and a database for content management.

## Project Structure

```
ai-blog-writer/
├── config/                     # Configuration files
├── data/                       # Input/output JSONs for testing
├── docs/                       # Documentation
├── src/                        # Main application logic
│   ├── pipeline/               # Langchain pipeline components
│   ├── integrations/           # External service integrations
│   └── utils/                  # Helper functions
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
└── README.md                   # Project documentation
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
- Copy `.env.example` to `.env`
- Fill in your API keys and configuration values

3. Run the application:
```bash
python src/main.py
```
