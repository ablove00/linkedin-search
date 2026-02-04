"""
search_service.py
Advanced Elasticsearch search service for LinkedIn profiles.

Provides:
- Multi-column search (single query across columns)
- Advanced per-field search (AND-based)
- Highlighting matching text fields
"""

from es_client import es, INDEX_NAME

TEXT_COLUMNS = [
    "full_name", "job_title", "industry", "summary",
    "location_country", "job_summary"
]

KEYWORD_COLUMNS = [
    "education", "experience", "skills"
]

ALL_COLUMNS = TEXT_COLUMNS + KEYWORD_COLUMNS


def search_columns(columns: list, query: str, size: int = 10):
    """
    Search multiple columns using a single query string.
    Uses OR logic between columns.

    Example:
        columns=["full_name", "skills"], query="Python"

    This means:
        full_name OR skills contains "Python"
    """
    if not all(col in ALL_COLUMNS for col in columns):
        invalid = [col for col in columns if col not in ALL_COLUMNS]
        raise ValueError(f"Invalid columns: {invalid}")

    should_clauses = []
    for col in columns:
        if col in TEXT_COLUMNS:
            should_clauses.append({"match": {col: query}})
        else:
            should_clauses.append({"term": {col: query}})

    body = {
        "query": {
            "bool": {
                "should": should_clauses,
                "minimum_should_match": 1
            }
        },
        "highlight": {
            "fields": {col: {} for col in columns if col in TEXT_COLUMNS},
            "pre_tags": ["<em>"],
            "post_tags": ["</em>"]
        },
        "size": size
    }

    resp = es.search(index=INDEX_NAME, body=body)
    hits = resp["hits"]["hits"]
    total = resp["hits"]["total"]["value"]

    results = []
    for hit in hits:
        doc = hit["_source"]
        if "highlight" in hit:
            doc["_highlight"] = hit["highlight"]
        results.append(doc)

    return results, total


def advanced_search(field_queries: dict, size: int = 10):
    """
    Perform AND-based search where each field has its own query.

    Example input:
        {
            "summary": "ali",
            "job_summary": "ahmad"
        }

    This translates to:
        summary CONTAINS "ali"
        AND
        job_summary CONTAINS "ahmad"
    """
    if not field_queries:
        raise ValueError("No search fields provided")

    must_clauses = []

    for field, value in field_queries.items():
        if field not in ALL_COLUMNS:
            raise ValueError(f"Invalid field: {field}")

        if field in TEXT_COLUMNS:
            must_clauses.append({
                "match": {
                    field: value
                }
            })
        else:
            must_clauses.append({
                "term": {
                    field: value
                }
            })

    body = {
        "query": {
            "bool": {
                "must": must_clauses
            }
        },
        "highlight": {
            "fields": {
                field: {} for field in field_queries.keys()
                if field in TEXT_COLUMNS
            },
            "pre_tags": ["<em>"],
            "post_tags": ["</em>"]
        },
        "size": size
    }

    resp = es.search(index=INDEX_NAME, body=body)
    hits = resp["hits"]["hits"]
    total = resp["hits"]["total"]["value"]

    results = []
    for hit in hits:
        doc = hit["_source"]
        if "highlight" in hit:
            doc["_highlight"] = hit["highlight"]
        results.append(doc)

    return results, total
