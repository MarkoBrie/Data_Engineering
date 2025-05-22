import pandas as pd
import json
from config import DRUGS_PATH, PUBMED_CSV_PATH, PUBMED_JSON_PATH, CLINICAL_TRIALS_PATH

def load_drugs():
    return pd.read_csv(DRUGS_PATH, encoding='utf-8')

def load_pubmed():
    df_csv = pd.read_csv(PUBMED_CSV_PATH, encoding='utf-8')
    with open(PUBMED_JSON_PATH, encoding='utf-8') as f:
        data_json = pd.json_normalize(json.load(f))
    return pd.concat([df_csv, data_json], ignore_index=True)

def load_clinical_trials():
    return pd.read_csv(CLINICAL_TRIALS_PATH, encoding='utf-8')