import pandas as pd
import unicodedata

def normalize_text(text):
    if pd.isnull(text):
        return ""
    text = text.lower().strip()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text

def clean_drugs(df):
    df = df.drop_duplicates(subset=['atccode', 'drug'])
    df['drug'] = df['drug'].apply(normalize_text)
    df['atccode'] = df['atccode'].astype(str)
    return df

def clean_publications(df):
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