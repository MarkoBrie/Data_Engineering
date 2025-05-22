import pandas as pd
import json
from config import DRUGS_PATH, PUBMED_CSV_PATH, PUBMED_JSON_PATH, CLINICAL_TRIALS_PATH

# Data loading functions are modular and reusable, 
# which is essential for scalable and maintainable pipelines.

def load_drugs():
    """Load drugs data from CSV."""
    return pd.read_csv(DRUGS_PATH, encoding='utf-8')

def load_pubmed():
    """
    Load PubMed data from both CSV and JSON sources,
    then concatenate for unified downstream processing.
    """
    df_csv = pd.read_csv(PUBMED_CSV_PATH, encoding='utf-8')
    with open(PUBMED_JSON_PATH, encoding='utf-8') as f:
        data_json = pd.json_normalize(json.load(f))
    return pd.concat([df_csv, data_json], ignore_index=True)

def load_clinical_trials():
    """Load clinical trials data from CSV."""
    return pd.read_csv(CLINICAL_TRIALS_PATH, encoding='utf-8')