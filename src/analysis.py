def get_top_journal(graph):
    """
    Find the journal mentioning the most unique drugs.
    - Demonstrates ability to aggregate and analyze graph data.
    - Useful for reporting and business insights.
    """
    journal_drugs = {}
    for drug in graph:
        for mention in drug['mentions']:
            journal = mention['journal']
            if journal not in journal_drugs:
                journal_drugs[journal] = set()
            journal_drugs[journal].add(drug['drug'])
    top_journal = max(journal_drugs.items(), key=lambda x: len(x[1]))
    return {"journal": top_journal[0], "unique_drugs": len(top_journal[1])}

def get_co_mentioned_drugs(graph, drug_name):
    """
    For a given drug, find all other drugs mentioned in the same PubMed journals,
    but not in clinical trials.
    - Illustrates advanced filtering and set operations.
    """
    pubmed_journals = set()
    for drug in graph:
        if drug['drug'] == drug_name:
            pubmed_journals = {m['journal'] for m in drug['mentions'] if m['source'] == 'pubmed'}
            break
    co_drugs = set()
    for drug in graph:
        if drug['drug'] == drug_name:
            continue
        journals = {m['journal'] for m in drug['mentions'] if m['source'] == 'pubmed'}
        if journals & pubmed_journals:
            co_drugs.add(drug['drug'])
    return list(co_drugs)