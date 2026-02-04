import ast
import re

# ------------------------
# get_cleaner
# ------------------------
def get_cleaner(column_name: str):
    """
    Returns the cleaning function for a given column name.

    Args:
        column_name (str): Name of the column (e.g., 'full_name', 'job_title', etc.)

    Returns:
        function: The corresponding cleaning function.

    Raises:
        ValueError: If the column name is not recognized.
    """
    cleaners = {
        "full_name": clean_full_name,
        "job_title": clean_job_title,
        "industry": clean_industry,
        "summary": clean_summary,
        "location_country": clean_location_country,
        "education": clean_education,
        "experience": clean_experience,
        "skills": clean_skills,
        "job_summary": clean_job_summary,
    }

    if column_name not in cleaners:
        raise ValueError(f"No cleaner found for column '{column_name}'")

    return cleaners[column_name]

# ------------------------
# full_name
# ------------------------
def clean_full_name(text: str) -> str:
    """
    Cleans the full name text.

    Rules:
    - Returns an empty string if the text is None or only whitespace.
    - Removes text that looks like file paths (Windows/Linux) or file names.
    - Keeps only letters (a-z, A-Z) and spaces.
    - Collapses multiple spaces into a single space.
    """
    if not text:
        return ""
    text = text.strip()
    if ("\\" in text or "/" in text or 
        re.search(r"[a-zA-Z]:", text) or 
        re.search(r"\.(csv|txt|xlsx|json|zip)$", text, re.IGNORECASE)):
        return ""
    cleaned = re.sub(r"[^a-zA-Z\s]", "", text)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned if cleaned else ""

# ------------------------
# job_title
# ------------------------
def clean_job_title(text: str) -> str:
    """
    Cleans the job title text.

    Rules:
    - Returns an empty string if the text is None or only whitespace.
    - Removes text that is a list or JSON format.
    - Otherwise, returns the text as-is.
    """
    if not text:
        return ""
    text = text.strip()
    if text.startswith("[") or text.startswith("{") or text == "[]":
        return ""
    return text

# ------------------------
# industry
# ------------------------
def clean_industry(text: str) -> str:
    """
    Cleans the industry text.

    Rules:
    - Returns an empty string if the text is None or only whitespace.
    - Removes text that is a list or JSON format.
    - Removes text containing digits.
    - Removes text containing characters outside of letters, spaces, commas, hyphens, and ampersands.
    - Collapses multiple spaces into a single space.
    """
    if not text:
        return ""
    text = text.strip()
    if (text.startswith("[") or 
        text.startswith("{") or 
        text == "[]" or 
        re.search(r"\d", text)):
        return ""
    if re.search(r"[^a-zA-Z\s,&-]", text):
        return ""
    cleaned = re.sub(r"\s+", " ", text)
    return cleaned.strip()

# ------------------------
# summary
# ------------------------
def clean_summary(text: str) -> str:
    """
    Cleans generic summary text.

    Rules:
    - Returns an empty string if the text is None or only whitespace.
    - Removes text that is a list or JSON format.
    - Removes text that is a numeric range (e.g., 1-10), number with plus (e.g., 10001+), or float (e.g., 9.0).
    - Otherwise, returns the text as-is.
    """
    if not text:
        return ""
    text = text.strip()
    if text.startswith("[") or text.startswith("{") or text == "[]":
        return ""
    if (re.fullmatch(r"\d+-\d+", text) or 
        re.fullmatch(r"\d+\+", text) or 
        re.fullmatch(r"\d+\.\d+", text)):
        return ""
    return text

# ------------------------
# location_country
# ------------------------
def clean_location_country(text: str) -> str:
    """
    Cleans the location_country text.

    Rules:
    - Returns an empty string if the text is None or only whitespace.
    - Removes text that is a list or JSON format.
    - Removes text that is a date in format YYYY-MM-DD.
    - Removes numeric ranges with commas (e.g., 55,000-70,000), less than (<20,000) or greater than (>250,000) formats.
    - Removes simple floats (e.g., 41.0).
    - Removes text that is a single character.
    - Otherwise, returns the text as-is.
    """
    if not text:
        return ""
    text = text.strip()
    if text.startswith("[") or text.startswith("{") or text == "[]":
        return ""
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return ""
    if re.fullmatch(r"[\d,]+-[\d,]+", text):
        return ""
    if re.fullmatch(r"<[\d,]+", text) or re.fullmatch(r">[\d,]+", text):
        return ""
    if re.fullmatch(r"\d+\.\d+", text):
        return ""
    if len(text) == 1:
        return ""
    return text

# ------------------------
# education
# ------------------------
def clean_education(text: str) -> str:
    """
    Cleans the education field.

    Rules:
    - Returns an empty string if the text is None, only whitespace, or not a list.
    - Parses the text as a Python list using ast.literal_eval.
    - Extracts the 'school.name' from each item if it exists.
    - Returns school names joined by ' | '.
    """
    if not text:
        return ""
    text = text.strip()
    if not (text.startswith("[") and text.endswith("]")):
        return ""
    try:
        data = ast.literal_eval(text)
    except Exception:
        return ""
    if not isinstance(data, list):
        return ""
    school_names = []
    for item in data:
        if isinstance(item, dict):
            school = item.get("school")
            if isinstance(school, dict):
                name = school.get("name")
                if isinstance(name, str) and name.strip():
                    school_names.append(name.strip())
    return " | ".join(school_names)

# ------------------------
# experience
# ------------------------
def clean_experience(text: str) -> str:
    """
    Cleans the experience field.

    Rules:
    - Returns an empty string if the text is None, only whitespace, or not a list.
    - Parses the text as a Python list using ast.literal_eval.
    - Extracts 'company.name' and 'title.name' from each item if they exist.
    - Joins company and title with ':', and separates items with ' | '.
    - If only one of company or title exists, includes only that.
    """
    if not text:
        return ""
    text = text.strip()
    if not (text.startswith("[") and text.endswith("]")):
        return ""
    try:
        data = ast.literal_eval(text)
    except Exception:
        return ""
    if not isinstance(data, list):
        return ""
    results = []
    for item in data:
        if not isinstance(item, dict):
            continue
        company_name = ""
        title_name = ""
        company = item.get("company")
        if isinstance(company, dict):
            name = company.get("name")
            if isinstance(name, str):
                company_name = name.strip()
        title = item.get("title")
        if isinstance(title, dict):
            name = title.get("name")
            if isinstance(name, str):
                title_name = name.strip()
        if company_name and title_name:
            results.append(f"{company_name} : {title_name}")
        elif company_name:
            results.append(company_name)
        elif title_name:
            results.append(title_name)
    return " | ".join(results)

# ------------------------
# skills
# ------------------------
def clean_skills(text: str) -> str:
    """
    Cleans the skills field.

    Rules:
    - Returns an empty string if the text is None, only whitespace, or not a list.
    - Parses the text as a Python list using ast.literal_eval.
    - Keeps only string items.
    - Removes items that look like international phone numbers (e.g., +1234567890).
    - Returns the remaining skills joined by ' | '.
    """
    if not text:
        return ""
    text = text.strip()
    if not (text.startswith("[") and text.endswith("]")):
        return ""
    try:
        data = ast.literal_eval(text)
    except Exception:
        return ""
    if not isinstance(data, list):
        return ""
    skills = []
    for item in data:
        if isinstance(item, str):
            item_clean = item.strip()
            if not item_clean:
                continue
            if re.fullmatch(r"\+\d{7,15}", item_clean):
                continue
            skills.append(item_clean)
    return " | ".join(skills)

# ------------------------
# job_summary
# ------------------------
def clean_job_summary(text: str) -> str:
    """
    Cleans the job summary text.

    Rules:
    - Returns an empty string if the text is None or only whitespace.
    - Removes text that is a single character.
    - Removes text that contains only digits.
    - Removes text in date format: YYYY-MM or YYYY-MM-DD.
    - Otherwise, returns the cleaned text.
    """
    if not text:
        return ""
    text = text.strip()
    if (len(text) == 1 or 
        text.isdigit() or 
        re.fullmatch(r"\d{4}-\d{2}(-\d{2})?", text)):
        return ""
    return text
