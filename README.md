# Data Engineering Project Structure & Best Practices

## Poetry Setup

1. [Install Poetry](https://python-poetry.org/docs/#installation)
2. Install dependencies:
   ```sh
   poetry install
   ```
3. Activate the virtual environment:
   ```sh
   poetry shell
   ```
4. Run the pipeline:
   ```sh
   python -m src.pipeline
   ```

## 1. Structure de projet recommandée

```text
project_root/
│
├── data/                     # Données brutes (input)
│   ├── drugs.csv
│   ├── pubmed.csv
│   ├── pubmed.json
│   └── clinical_trials.csv
│
├── src/                      # Code source principal
│   ├── __init__.py
│   ├── config.py             # Paramètres globaux, chemins, etc.
│   ├── data_loader.py        # Fonctions de chargement des données
│   ├── data_cleaning.py      # Fonctions de nettoyage
│   ├── pipeline.py           # Orchestration de la pipeline
│   ├── graph_builder.py      # Construction du graphe de sortie
│   └── analysis.py           # Fonctions bonus d’analyse ad-hoc
│
├── tests/                    # Tests unitaires
│   └── test_data_cleaning.py
│
├── output/                   # Résultats générés (output)
│   └── drug_mentions_graph.json
│
├── requirements.txt          # Dépendances Python
└── README.md                 # Documentation et instructions
```

### Pourquoi cette structure ?

- **Séparation claire des responsabilités** : chaque module a un rôle précis (chargement, nettoyage, pipeline, etc.).
- **Réutilisabilité** : les fonctions de chargement/nettoyage peuvent être utilisées dans d’autres pipelines.
- **Facilité d’intégration** : la pipeline principale (`pipeline.py`) peut être appelée facilement par un orchestrateur (Airflow, Luigi, etc.).
- **Tests** : les modules sont testables indépendamment.
- **Scalabilité** : structure adaptée à l’ajout de nouvelles étapes ou de nouveaux jeux de données.

---

## 2. Étapes de data cleansing et bonnes pratiques

### Tests

```poetry run pytest tests/test_json_validity.py```

### a) Chargement des données

- Utiliser `pandas` pour les CSV, `json` ou `pandas.read_json` pour le JSON.
- Uniformiser les noms de colonnes si besoin.
- Gérer les encodages (`utf-8` par défaut).

### b) Nettoyage

- Suppression des doublons : éviter les mentions multiples identiques.
- Gestion des valeurs manquantes : suppression ou imputation selon le contexte.
- Normalisation des chaînes : tout en minuscule, suppression des espaces superflus, accents, etc.
- Typage : s’assurer que les dates sont bien au format datetime, les IDs en string/int.
- Vérification de la cohérence : par exemple, un journal doit toujours avoir un nom non vide.

### c) Bonnes pratiques Python

- Utilisation de fonctions pures, testables.
- Documentation (docstrings) systématique.
- Logging pour le suivi des étapes.
- Pas de variables globales inutiles.
- Respect du PEP8.
- Gestion des exceptions (try/except) pour les I/O.

### 3. Orchestration de la pipeline

- Pipeline modulaire : chaque étape (chargement, nettoyage, transformation, export) est une fonction ou une classe.
- Entrée unique : un point d’entrée (main() ou équivalent) pour faciliter l’appel par un orchestrateur.
- Paramétrisation : chemins, options, etc. dans un fichier de config.

### 4. Construction du graphe de sortie

**Modélisation proposée (exemple de structure JSON) :**

```json
[
  {
    "drug": "aspirin",
    "atccode": "N02BA01",
    "mentions": [
      {
        "source": "pubmed",
        "journal": "the lancet",
        "date": "2020-01-01",
        "title": "aspirin in heart disease"
      },
      {
        "source": "clinical_trials",
        "journal": "bmj",
        "date": "2021-03-15",
        "title": "aspirin and stroke prevention"
      }
    ]
  }
]
```

**Pourquoi ce choix ?**

- Facile à parcourir pour répondre aux questions analytiques.
- Permet d’ajouter d’autres sources ou attributs facilement.
- Structure adaptée à la sérialisation/désérialisation JSON.

## 5. Fonctions d’analyse ad-hoc (bonus)

- **Journal mentionnant le plus de médicaments différents** : parcourir le graphe, compter les médicaments par journal.
- **Médicaments co-mentionnés dans les mêmes journaux (PubMed uniquement)** : filtrer les mentions PubMed, trouver les journaux communs, exclure ceux présents dans Clinical Trials.

## 6. Exemple de pipeline (simplifié)

```python
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
```

## 7. Pour la volumétrie (question bonus)

- Utiliser des outils adaptés : Spark, Dask, ou Pandas chunking pour traiter les fichiers volumineux.
- Stockage distribué : S3, HDFS, Azure Blob Storage.
- Partitionnement : découper les données par date, source, etc.
- Streaming : ingestion continue si besoin.
- Optimisation I/O : formats Parquet/ORC plutôt que CSV/JSON.
- Orchestration robuste : Airflow, Luigi, etc.

## 8. Conclusion

- Cette structure favorise la lisibilité, la réutilisabilité, la testabilité et l’intégration dans un orchestrateur.
- Chaque étape est modulaire, facilement extensible, et respecte les standards professionnels du data engineering Python