"""
FastAPI application for LinkedIn Profiles Search.

Supports:
- Multi-column search (OR-based)
- Advanced per-field search (AND-based)
- Highlighting matches in text columns
"""

from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from search_service import (
    search_columns,
    advanced_search,
    ALL_COLUMNS
)
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="LinkedIn Profiles Search API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # اجازه برای همه آدرس‌های فرانت
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search/")
def search(
    columns: List[str] = Query(..., description="Columns to search in"),
    q: str = Query(..., description="Query string"),
    size: int = Query(10, description="Number of results")
):
    """
    Perform OR-based multi-column search using a single query string.
    """
    results, total = search_columns(columns, q, size)
    return {"total": total, "results": results}


class AdvancedSearchRequest(BaseModel):
    """
    Request model for advanced AND-based search.

    Each field is optional.
    If a field is provided, it will be added as an AND condition
    in the Elasticsearch query.

    Example:
        {
            "summary": "Business Analyst",
            "job_summary": "I work on the CREW",
            "skills": "python"
        }
    """

    full_name: Optional[str] = None
    job_title: Optional[str] = None
    industry: Optional[str] = None
    summary: Optional[str] = None
    location_country: Optional[str] = None

    education: Optional[str] = None
    experience: Optional[str] = None
    skills: Optional[str] = None

    job_summary: Optional[str] = None


@app.post("/search/advanced")
def search_advanced(payload: dict, size: int = 10):
    results, total = advanced_search(payload, size)
    return {"total": total, "results": results}
