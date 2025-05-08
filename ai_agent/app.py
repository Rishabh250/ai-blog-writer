from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.main import run_blog_generation
from src.utils.constants import Constants

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


class Blog(BaseModel):
    structure: str = Field(
        default="blog",
        description="Content structure type (blog, how-to, listicle, comparison, guide, faq)",
    )
    persona: str = Field(
        default="professional",
        description="Target audience persona (professional, academic, casual)",
    )
    topic: str = Field(..., description="Main topic of the blog")
    tone: str = Field(
        default="informative",
        description="Content tone (informative, engaging, persuasive)",
    )
    keyword: Optional[str] = Field(
        default=None, description="Primary keyword to target"
    )
    goal: str = Field(..., description="Purpose of the content")


class BlogRequest(BaseModel):
    blog: Blog
    find_trends_type: str = Field(
        default=Constants.FIND_TRENDS_TYPE["GOOGLE_TRENDS"],
        description="Method to find trends data",
    )
    session_id: str = Field(..., description="Unique session identifier")
    clear_memory: bool = Field(
        default=False, description="Whether to clear session memory"
    )
    user_input: Optional[str] = Field(
        default=None, description="Additional user instructions"
    )
    step: Optional[str] = Field(
        default="blog_outline", description="The step of the blog generation process"
    )


class BlogResponse(BaseModel):
    content: str
    type: str
    success: bool
    message: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Welcome to the AI Blog Writer API"}


@app.post("/generate-blog", response_model=BlogResponse)
async def generate_blog(request: BlogRequest):
    try:
        metadata_dict = request.blog.model_dump()

        content, content_type, success = run_blog_generation(
            metadata=metadata_dict,
            find_trends_type=request.find_trends_type,
            session_id=request.session_id,
            clear_memory=request.clear_memory,
            user_input=request.user_input,
            step=request.step,
        )

        if not success:
            return BlogResponse(
                content=content,
                type=content_type,
                success=False,
                message="Blog generation failed",
            )

        return BlogResponse(content=content, type=content_type, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
