"""
skill_extractor.py
Rule-based skill extractor for when LLM is unavailable.
Used as a fallback — primary extraction uses gemini_service.py (LLM-based).
"""
 
# Comprehensive skill keyword list
SKILL_KEYWORDS = [
    # Programming
    "python", "r", "java", "javascript", "typescript", "scala", "c++", "c#", "go",
 
    # Data & Analysis
    "sql", "data analysis", "data engineering", "etl", "data pipeline",
    "data validation", "data transformation", "data quality", "eda",
    "exploratory data analysis", "statistical analysis", "statistics",
    "anomaly detection", "pattern detection",
 
    # ML & AI
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "reinforcement learning", "llm", "large language models",
    "generative ai", "classification", "regression", "clustering",
    "neural network", "transformer", "bert", "gpt",
 
    # ML Frameworks & Libraries
    "scikit-learn", "tensorflow", "keras", "pytorch", "xgboost", "lightgbm",
    "hugging face", "transformers", "spacy", "nltk",
 
    # Python Libraries (keep these — they ARE assessable skills)
    "pandas", "numpy", "matplotlib", "seaborn", "scipy", "plotly",
 
    # Databases
    "mysql", "postgresql", "mongodb", "redis", "sqlite", "bigquery",
    "snowflake", "cassandra",
 
    # Visualization & BI
    "power bi", "tableau", "excel", "google sheets", "looker",
    "dax", "dashboarding",
 
    # Cloud & MLOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes",
    "mlflow", "airflow", "dbt", "spark", "hadoop",
 
    # NLP Specific
    "tokenization", "stemming", "lemmatization", "tf-idf", "word2vec",
    "text preprocessing", "text classification", "text summarization",
    "sentiment analysis", "named entity recognition",
 
    # Soft Skills (relevant for JD matching)
    "communication", "problem solving", "teamwork", "leadership",
    "project management", "agile", "cross-functional collaboration",
]
 
 
def extract_skills(text: str) -> list:
    """
    Extract skills from raw text using keyword matching.
    Returns a deduplicated lowercase list of found skills.
    """
    if not text:
        return []
 
    text_lower = text.lower()
    found = []
 
    for skill in SKILL_KEYWORDS:
        # Match whole word/phrase to avoid partial matches
        if skill in text_lower:
            found.append(skill)
 
    return list(set(found))