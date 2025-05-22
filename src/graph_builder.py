def build_mentions_graph(drugs, pubmed, clinical_trials):
    """
    Build a graph structure linking drugs to their mentions in publications.
    - Ensures modularity and separation of concerns.
    - Facilitates downstream analytics and reporting.
    """
    graph = []
    for _, drug_row in drugs.iterrows():
        drug_name = drug_row['drug']
        atccode = drug_row['atccode']
        mentions = []
        # PubMed
        for _, row in pubmed.iterrows():
            if drug_name in row['title']:
                mentions.append({
                    "source": "pubmed",
                    "journal": row['journal'],
                    "date": row['date'].strftime('%Y-%m-%d'),
                    "title": row['title']
                })
        # Clinical Trials
        for _, row in clinical_trials.iterrows():
            if drug_name in row['title']:
                mentions.append({
                    "source": "clinical_trials",
                    "journal": row['journal'],
                    "date": row['date'].strftime('%Y-%m-%d'),
                    "title": row['title']
                })
        graph.append({
            "drug": drug_row['drug'],
            "atccode": atccode,
            "mentions": mentions
        })
    return graph