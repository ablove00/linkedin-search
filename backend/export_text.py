"""
export_text.py

This script reads a raw LinkedIn data CSV file, cleans each column using
predefined cleaning functions from the 'column_cleaners' module, and writes
the cleaned output of each column into separate text files.

Each column is cleaned according to its specific rules:
- full_name, job_title, industry, summary, location_country, education,
  experience, skills, job_summary

Steps:
1. Count total number of lines in the raw data file.
2. Read the CSV into a pandas DataFrame, skipping malformed lines.
3. Iterate over each column, get its cleaning function from 'get_cleaner'.
4. Apply the cleaning function to each row and write the cleaned output
   to a separate text file, adding a separator between entries.
"""

import pandas as pd
import os
from column_cleaners import get_cleaner

DATA_FILE = "data/300-user-linkedin.txt"
OUTPUT_DIR = "data/columns_text"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Step 1: Count total lines in the raw data file
with open(DATA_FILE, encoding="utf-8") as f:
    total_lines = sum(1 for _ in f)
print(f"Total lines in raw file: {total_lines}")

# Step 2: Read the CSV file into a pandas DataFrame
df = pd.read_csv(
    DATA_FILE,
    delimiter=",",
    quotechar='"',
    engine="python",
    on_bad_lines='skip'   # skip malformed lines
)
print(f"Total rows after reading with pandas: {len(df)}")

# Columns to clean
columns = [
    "full_name", "job_title", "industry", "summary", 
    "location_country", "education", "experience", 
    "skills", "job_summary"
]

# Step 3: Clean each column and write to separate text files
for col in columns:
    cleaner = get_cleaner(col)  # Get the appropriate cleaning function
    output_file = os.path.join(OUTPUT_DIR, f"{col}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        for val in df[col].fillna("").astype(str):
            cleaned = cleaner(val)  # Apply cleaning
            f.write(cleaned + "\n")
            f.write("=" * 50 + "\n")  # Separator between entries

print("Columns have been successfully extracted and cleaned.")
