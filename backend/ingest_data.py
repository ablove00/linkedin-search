"""
ingest_data.py

This script reads LinkedIn CSV data, cleans each column using 'column_cleaners',
creates/recreates an Elasticsearch index with proper mappings, and indexes all
cleaned rows into Elasticsearch.

Special handling:
- Columns 'education', 'experience', and 'skills' are stored as keyword lists,
  split by '|'.
- Other columns are stored as text for full-text search.
"""

import pandas as pd
from es_client import es, INDEX_NAME
from column_cleaners import get_cleaner

# CSV data file path
DATA_FILE = "data/300-user-linkedin.txt"

# Columns to process
columns = [
    "full_name", "job_title", "industry", "summary",
    "location_country", "education", "experience",
    "skills", "job_summary"
]

# Columns to store as keyword (splittable lists)
KEYWORD_COLUMNS = ["education", "experience", "skills"]

# Define Elasticsearch index mappings
INDEX_MAPPINGS = {
    "properties": {
        "full_name": {"type": "text"},
        "job_title": {"type": "text"},
        "industry": {"type": "text"},
        "summary": {"type": "text"},
        "location_country": {"type": "text"},
        "education": {"type": "keyword"},
        "experience": {"type": "keyword"},
        "skills": {"type": "keyword"},
        "job_summary": {"type": "text"},
    }
}

def recreate_index():
    """
    Recreate the Elasticsearch index:
    - Delete the index if it exists.
    - Create a new index with proper mappings.
    """
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        print(f"Deleted existing index '{INDEX_NAME}'")

    es.indices.create(index=INDEX_NAME, mappings=INDEX_MAPPINGS)
    print(f"Created index '{INDEX_NAME}' with mappings.")


def ingest():
    """
    Ingest LinkedIn CSV data into Elasticsearch:
    - Read the CSV file using pandas.
    - Apply cleaning functions for each column.
    - Keyword columns are split by '|' and stored as lists.
    - Index each cleaned row into Elasticsearch.
    """
    recreate_index()

    # Read CSV file with pandas
    df = pd.read_csv(
        DATA_FILE,
        delimiter=",",
        quotechar='"',
        engine="python",
        on_bad_lines='skip'  # skip malformed lines
    )

    countAll = 337
    before_count = len(df)
    df = df.drop_duplicates(subset=columns)
    after_count = len(df)
    removed = countAll - after_count
    print(
        f"Rows data: 337 | "
        f"Rows before deduplication: {before_count} | "
        f"Rows after deduplication: {after_count} | "
        f"Removed: {removed}"
    )

    # Prepare cleaning functions for each column
    cleaners = {col: get_cleaner(col) for col in columns}

    for i, row in df.iterrows():
        try:
            doc = {}
            for col in columns:
                cleaned_text = cleaners[col](str(row.get(col, "")))

                # For keyword columns, split by '|' and strip items
                if col in KEYWORD_COLUMNS:
                    if cleaned_text:
                        doc[col] = [item.strip() for item in cleaned_text.split("|") if item.strip()]
                    else:
                        doc[col] = []
                else:
                    doc[col] = cleaned_text

            # Index the cleaned document
            es.index(index=INDEX_NAME, document=doc)

        except Exception as e:
            print(f"⚠️ Error in row {i}: {e}")

    print("✅ Data indexed successfully.")


if __name__ == "__main__":
    ingest()
