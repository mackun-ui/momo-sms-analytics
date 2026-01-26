# MoMo SMS Analytics App

## Team Name
**Codeizzy**

## Project Description
An ETL-based fullstack application for cleaning, categorising, and visualising MoMo SMS transaction data.

## Project Organisation
```
.
├── README.md                         # Setup, run, overview
├── .env.example                      # DATABASE_URL or path to SQLite
├── requirements.txt                  # lxml/ElementTree, dateutil, (FastAPI optional)
├── index.html                        # Dashboard entry (static)
├── web/
│   ├── styles.css                    # Dashboard styling
│   ├── chart_handler.js              # Fetch + render charts/tables
│   └── assets/                       # Images/icons (optional)
├── data/
│   ├── raw/                          # Provided XML input (git-ignored)
│   │   └── momo.xml
│   ├── processed/                    # Cleaned/derived outputs for frontend
│   │   └── dashboard.json            # Aggregates the dashboard reads
│   ├── db.sqlite3                    # SQLite DB file
│   └── logs/
│       ├── etl.log                   # Structured ETL logs
│       └── dead_letter/              # Unparsed/ignored XML snippets
├── etl/
│   ├── __init__.py
│   ├── config.py                     # File paths, thresholds, categories
│   ├── parse_xml.py                  # XML parsing (ElementTree/lxml)
│   ├── clean_normalize.py            # Amounts, dates, phone normalization
│   ├── categorize.py                 # Simple rules for transaction types
│   ├── load_db.py                    # Create tables + upsert to SQLite
│   └── run.py                        # CLI: parse -> clean -> categorize -> load -> export JSON
├── api/                              # Optional (bonus)
│   ├── __init__.py
│   ├── app.py                        # Minimal FastAPI with /transactions, /analytics
│   ├── db.py                         # SQLite connection helpers
│   └── schemas.py                    # Pydantic response models
├── scripts/
│   ├── run_etl.sh                    # python etl/run.py --xml data/raw/momo.xml
│   ├── export_json.sh                # Rebuild data/processed/dashboard.json
│   └── serve_frontend.sh             # python -m http.server 8000 (or Flask static)
└── tests/
    ├── test_parse_xml.py             # Small unit tests
    ├── test_clean_normalize.py
    └── test_categorize.py
```

## High Level System Architecture
Here is the link to the high level system architecture diagram of our MoMo SMS Analytics app.
https://drive.google.com/file/d/15Wdv7dohUM3AlQf6I7Dvo1iaNmrMPi_R/view?usp=sharing

## Scrum Board Setup
We are using GitHub Projects to track our progress. 
https://github.com/users/mackun-ui/projects/1/views/1

## Database Design Documentation
Find a detailed explanation and justification for our database design in the PDF document in the docs folder.
```
├── ...
├── docs/
│   ├── momo sms analytics erd.drawio.png
│   ├── Database Design Documentation.pdf
```

## SQL to JSON Mapping
| SQL TABLE            | JSON REPRESENTATION                         | 
|----------------------|---------------------------------------------|
| USER                 | USER[], sender, receiver                    | 
| TRANSACTION          | TRANSACTION[], complete_transaction_example | 
| CATEGORY             | CATEGORY[], categories[]                    |
| TRANSACTION_CATEOGRY | This can be seen within categories[]        |
| LOGS                 | LOG[], logs[]                               |

## Team Members
- David Chukwuebuka Achibiri 
- Manuelle Aseye Ackun
- Rhoda Nicole Umutesi