import pandas as pd
import unicodedata

def normalize_text(text):
    """
    Normalize text for consistent processing:
    - Lowercase
    - Strip whitespace
    - Remove accents
    Production best practice: always normalize text fields for reliable matching.
    """
    if pd.isnull(text):
        return ""
    text = text.lower().strip()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text

def clean_drugs(df):
    """
    Clean the drugs DataFrame:
    - Remove duplicates based on 'atccode' and 'drug'
    - Normalize drug names
    - Ensure 'atccode' is string type
    Essential for data quality and downstream join reliability.
    """
    df = df.drop_duplicates(subset=['atccode', 'drug'])
    df['drug'] = df['drug'].apply(normalize_text)
    df['atccode'] = df['atccode'].astype(str)
    return df

def clean_publications(df):
    """
    Clean publication DataFrames (PubMed or Clinical Trials):
    - Rename 'scientific_title' to 'title' for consistency
    - Remove duplicates based on 'id' and 'title'
    - Drop rows with missing essential fields
    - Normalize text fields
    - Convert 'date' to datetime, drop invalid dates
    - Ensure 'id' is string type

    This function is robust to schema differences and ensures
    data consistency for downstream processing.
    """
    # Rename 'scientific_title' from clinical_trials.csv to 'title' if present (for consistency)
    if 'scientific_title' in df.columns:
        df = df.rename(columns={'scientific_title': 'title'})
    df = df.drop_duplicates(subset=['id', 'title'])
    df = df.dropna(subset=['journal', 'title', 'date'])
    df['journal'] = df['journal'].apply(normalize_text)
    df['title'] = df['title'].apply(normalize_text)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df['id'] = df['id'].astype(str)
    return df