from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.main import run_blog_generation

app = FastAPI(
    title="AI Blog Writer API",
    description="An API for generating AI-powered blog content",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BlogMetadata(BaseModel):
    structure: str = "blog"  # blog, how-to, listicle, comparison, guide, faq
    persona: str = "professional"  # professional, academic, casual
    topic: str
    tone: str = "informative"  # informative, engaging, persuasive
    keyword: Optional[str] = None
    goal: str


class BlogResponse(BaseModel):
    content: str
    html: str
    success: bool


@app.get("/")
async def root():
    return {"message": "Welcome to the AI Blog Writer API"}


@app.post("/generate-blog", response_model=BlogResponse)
async def generate_blog(metadata: BlogMetadata):
    try:
        if not metadata.keyword:
            metadata.keyword = metadata.topic

        metadata_dict = metadata.model_dump()

        content, html, success = run_blog_generation(metadata_dict)

        if not success:
            raise HTTPException(status_code=500, detail="Blog generation failed")

        return BlogResponse(content=content, html=html, success=success)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
