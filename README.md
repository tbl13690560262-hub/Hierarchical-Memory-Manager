# Hierarchical Memory Manager

A lightweight Python-based memory management and retrieval system exploring different strategies for retrieving information from hierarchical long-term memory.

## Overview

This independent project implements a hierarchical memory storage system and evaluates five retrieval approaches using manually labeled queries.

The project focuses on practical system development, retrieval evaluation, and understanding the trade-offs between precision and recall.

## Features

* Hierarchical memory organization using Python dictionaries
* Add, search, view, update, and delete memory entries
* JSON-based persistent storage
* Interactive command-line interface
* Five keyword-based retrieval strategies
* Automated evaluation using Precision, Recall, and F1-score
* CSV export of experimental results

## Project Structure

```text
Hierarchical-Memory-Manager/
├── memory_manager.py
├── experiment.py
├── independent_test.py
├── EXPERIMENT_REPORT.md
├── README.md
├── .gitignore
├── evaluation_results.csv
└── independent_results.csv
```

The personal `memories.json` file is excluded from version control.

## Retrieval Methods

| Method            | Description                                    |
| ----------------- | ---------------------------------------------- |
| Baseline          | Full-query substring matching                  |
| Ranked            | Multi-keyword substring matching with ranking  |
| Token             | Whole-word matching with ranking               |
| Strict Token      | Requires all query tokens to match             |
| Concept Expansion | Uses manually defined related-concept mappings |

These are lexical and rule-based retrieval methods. The system does not currently use language-model embeddings.

## Getting Started

**Requirements:** Python 3.9 or later.

No third-party packages are required.

Clone the repository and enter the project directory:

```bash
git clone https://github.com/tbl13690560262-hub/Hierarchical-Memory-Manager.git
cd Hierarchical-Memory-Manager
```

Run the memory manager:

```bash
python memory_manager.py
```

The interactive menu supports adding, searching, viewing, updating, and deleting saved memories.

## Running the Experiments

Development-set experiment:

```bash
python experiment.py
```

Additional query-set evaluation:

```bash
python independent_test.py
```

Both experiments use a fixed dataset of 20 synthetic memories. The development set contains 11 queries, and the additional evaluation set contains 5 queries.

Retrieval is evaluated at a maximum of three returned results per query (K = 3).

## Experimental Results

Macro-average F1-score:

| Method            | Development Queries | Additional Queries |
| ----------------- | ------------------: | -----------------: |
| Baseline          |               0.515 |              0.200 |
| Ranked            |               0.677 |          **0.760** |
| Token             |               0.729 |          **0.760** |
| Strict Token      |           **0.747** |              0.600 |
| Concept Expansion |               0.735 |              0.200 |

Strict Token performed best on the development queries, while Ranked and Token achieved the highest F1-score on the additional queries.

These results highlight the trade-off between strict lexical matching and flexible keyword retrieval.

See [EXPERIMENT_REPORT.md](EXPERIMENT_REPORT.md) for more details.

## Limitations

* Small synthetic dataset and limited query coverage
* Manually defined relevance labels
* Both query sets use the same memory corpus
* Concept mappings are manually constructed
* No embedding-based semantic retrieval
* Results are preliminary and are not evidence of general performance on real-world long-term memory tasks

## Future Work

* Larger and more diverse evaluation datasets
* Improved relevance annotation
* Semantic retrieval using text embeddings
* More advanced ranking and memory organization strategies

## Project Status

Functional prototype with preliminary retrieval experiments.

Developed as an independent learning and research exploration project.
