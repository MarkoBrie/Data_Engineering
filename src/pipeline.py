from data_loader import load_drugs, load_pubmed, load_clinical_trials
from data_cleaning import clean_drugs, clean_publications
from graph_builder import build_mentions_graph
from analysis import get_top_journal, get_co_mentioned_drugs
from config import GRAPH_OUTPUT_PATH

import json

def main():
    drugs = clean_drugs(load_drugs())
    pubmed = clean_publications(load_pubmed())
    clinical_trials = clean_publications(load_clinical_trials())
    graph = build_mentions_graph(drugs, pubmed, clinical_trials)
    with open(GRAPH_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    print("Top journal:", get_top_journal(graph))
    print("Co-mentioned drugs for 'aspirin':", get_co_mentioned_drugs(graph, "aspirin"))

if __name__ == "__main__":
    main()