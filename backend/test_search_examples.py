"""
Test examples for LinkedIn Profiles FastAPI Search.

Includes:
- Single-column search (GET)
- Multi-column search (GET)
- Multi-text search with highlight (GET)
- Advanced AND-based search (POST)
"""

import requests
import json

SEARCH_URL = "http://127.0.0.1:8021/search/"
ADVANCED_URL = "http://127.0.0.1:8021/search/advanced"


# ---------------------------
# Example 1: Single-column search
# ---------------------------
def single_column_search():
    """
    Search only one column using OR-based search.
    """
    params = {
        "columns": ["full_name"],
        "q": "randall evans",
        "size": 5
    }

    response = requests.get(SEARCH_URL, params=params)
    print("\n--- Single Column Search ---")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))


# ---------------------------
# Example 2: Multi-column search
# ---------------------------
def multi_column_search():
    """
    Search across multiple columns using a single query string.
    OR-based logic.
    """
    params = {
        "columns": ["full_name", "skills"],
        "q": "Python",
        "size": 5
    }

    response = requests.get(SEARCH_URL, params=params)
    print("\n--- Multi-Column Search ---")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))


# ---------------------------
# Example 3: Multi-text columns with highlight
# ---------------------------
def multi_text_columns_search():
    """
    Search across multiple TEXT columns to see highlight results.
    """
    params = {
        "columns": ["summary", "job_summary"],
        "q": "manager",
        "size": 5
    }

    response = requests.get(SEARCH_URL, params=params)
    print("\n--- Multi Text Columns Search (Highlight) ---")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))


# ---------------------------
# Example 4: Advanced AND-based search (POST)
# ---------------------------
def advanced_search():
    """
    Advanced search using AND logic.

    Each field has its own query value.
    ALL provided fields must match.
    """
    payload = {
        "summary": "ali",
        "job_summary": "ahmad",
        "skills": "python"
    }

    params = {
        "size": 5
    }

    response = requests.post(ADVANCED_URL, json=payload, params=params)
    print("\n--- Advanced AND-Based Search ---")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))


# ---------------------------
# Run all examples
# ---------------------------
if __name__ == "__main__":
    single_column_search()
    print("=" * 50)
    multi_column_search()
    print("=" * 50)
    multi_text_columns_search()
    print("=" * 50)
    advanced_search()
