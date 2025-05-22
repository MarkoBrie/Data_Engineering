import os

# Centralized configuration for file paths.
# Using os.path ensures portability and maintainability.
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')

DRUGS_PATH = os.path.join(DATA_DIR, 'drugs.csv')
PUBMED_CSV_PATH = os.path.join(DATA_DIR, 'pubmed.csv')
PUBMED_JSON_PATH = os.path.join(DATA_DIR, 'pubmed.json')
CLINICAL_TRIALS_PATH = os.path.join(DATA_DIR, 'clinical_trials.csv')
GRAPH_OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'drug_mentions_graph.json')