# Data Engineering Project Structure & Best Practices

## 0 a) How to Install Poetry

1. **Run the official installation command in your terminal:**
   ```sh
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **(Optional) Add Poetry to your PATH**  
   If Poetry is not found after installation, add this to your shell config (`~/.bashrc`, `~/.zshrc`, etc.):
   ```sh
   export PATH="$HOME/.local/bin:$PATH"
   ```
   Then reload your shell:
   ```sh
   source ~/.zshrc
   ```
   or
   ```sh
   source ~/.bashrc
   ```

3. **Verify the installation:**
   ```sh
   poetry --version
   ```

For more details, see the [official Poetry documentation](https://python-poetry.org/docs/#installation).

## 0 b) Create virtual Environment
1. **Install dependencies:**
   ```sh
   poetry install
   ```
2. **Activate the virtual environment:**
   ```sh
   poetry shell
   ```
   or 
   ```sh
   poetry env activate
   ```
3. **Run Tests**

```sh
poetry run pytest tests/test_json_validity.py
```
4. **Run the pipeline:**
   ```sh
   cd src
   python pipeline.py
   ```



## 1. Project structure

```text
project_root/
│
├── data/                     # Raw data (input)
│   ├── drugs.csv
│   ├── pubmed.csv
│   ├── pubmed.json
│   └── clinical_trials.csv
│
├── src/                      # Main source code
│   ├── __init__.py
│   ├── config.py             # Global parameters, paths, etc.
│   ├── data_loader.py        # Data loading functions
│   ├── data_cleaning.py      # Data cleaning functions
│   ├── pipeline.py           # Pipeline orchestration
│   ├── graph_builder.py      # Output graph construction
│   └── analysis.py           # Bonus/ad-hoc analysis functions
│
├── tests/                    # Unit tests
│   └── test_data_cleaning.py
│
├── output/                   # Generated results (output)
│   └── drug_mentions_graph.json
│
├── requirements.txt          # Python dependencies
└── README.md                 # Documentation and instructions
```

### Why this structure?

- **Clear separation of responsibilities:** Each module has a specific role (loading, cleaning, pipeline orchestration, etc.).
- **Reusability:** Data loading/cleaning functions can be reused in other pipelines.
- **Easy integration:** The main pipeline (`pipeline.py`) can be easily called by an orchestrator (Airflow, Luigi, etc.).
- **Testability:** Modules are independently testable.
- **Scalability:** The structure is suitable for adding new steps or new datasets.
---

## 2. Data Cleansing Steps and Best Practices



### a) Data Loading

- Use `pandas` for CSV files, `json` or `pandas.read_json` for JSON files.
- Standardize column names if needed.
- Handle encodings (`utf-8` by default).

### b) Cleaning

- Remove duplicates: avoid multiple identical mentions.
- Handle missing values: remove or impute as appropriate.
- Normalize strings: lowercase, remove extra spaces, accents, etc.
- Typing: ensure dates are in datetime format, IDs as string/int.
- Consistency checks: e.g., a journal should always have a non-empty name.

### c) Python Best Practices

- Use pure, testable functions.
- Systematic documentation (docstrings).
- Logging for step tracking.
- No unnecessary global variables.
- Follow PEP8.
- Exception handling (`try/except`) for I/O.

### 3. Pipeline Orchestration

- Modular pipeline: each step (loading, cleaning, transforming, exporting) is a function or class.
- Single entry point: a main function (e.g., `main()`) for easy integration with an orchestrator.
- Parameterization: paths, options, etc. in a config file.

### 4. Output Graph Construction

**Proposed modeling (example JSON structure):**

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

**Why this choice?**

- Easy to navigate for analytical queries.
- Allows for easy addition of other sources or attributes.
- Structure is suitable for JSON serialization/deserialization.

## 5. Ad-hoc analysis functions (bonus)

- **Journal mentioning the most different drugs**: go the graph and count the number of unique drugs per journal.
- **Drugs co-mentioned in the same journals (PubMed only)**: filter PubMed mentions, find common journals, and exclude those present in Clinical Trials.

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

## 7. For Large-Scale Data (bonus question)

- Use appropriate tools: Spark, Dask, or Pandas chunking to process large files.
- Distributed storage: S3, HDFS, Azure Blob Storage.
- Partitioning: split data by date, source, etc.
- Streaming: continuous ingestion if needed.
- I/O optimization: use Parquet/ORC formats instead of CSV/JSON.
- Robust orchestration: Airflow, Luigi, etc.

## 8. Conclusion

- This structure promotes readability, reusability, testability, and easy integration with an orchestrator.
- Each step is modular, easily extensible, and follows professional data engineering standards in Python.

## Key production/data engineering best practices highlighted:

- **Separation of concerns:** Each module and function has a single responsibility.
- **Reusability:** Functions are generic and can be reused in other pipelines.
- **Data quality:** Cleaning steps ensure consistent, reliable data for downstream jobs.
- **Documentation:** Each function is documented for clarity and team collaboration.
- **Extensibility:** The pipeline is easy to extend with new data sources or analytics.
- **Python standards:** Code is PEP8-compliant and ready for integration in a professional environment.