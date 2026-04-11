# RAG Chatbot (Azure SQL Login + OpenAI Embeddings)

This project provides a local, production-style baseline for a Retrieval-Augmented Generation chatbot with:

- Login backed by Azure SQL Server (`users` table)
- Chat UI (login page + chat page)
- Persistent chat history in Azure SQL (`chats`, `messages`)
- RAG retrieval from indexed local documents (`document_chunks` with OpenAI embeddings)
- OpenAI response generation

## Repository structure

```
gen-ai-project-main/
├── README.md
├── RUN_APP.md
├── WORKFLOW.md
├── requirements.txt
├── note.txt
├── project.md
├── streamlit_dashboard.py
├── streamlit_rag_eval_dashboard.py
├── app/
│   ├── chroma_store.py
│   ├── config.py
│   ├── db.py
│   ├── main.py
│   ├── models.py
│   ├── rag.py
│   └── security.py
├── chroma_data/
│   ├── chroma.sqlite3
│   ├── 058323db-1471-48bb-a523-616892016a15/
│   ├── 86a5a161-5db3-4437-b73d-21fcca84af45/
│   ├── c3494ee5-4544-4bed-bd68-5cd96dca92f0/
│   ├── c49df7ea-cb66-4f67-a993-ff3d13c865bc/
│   └── ce963533-1326-4aae-8f80-f935dc3042a7/
├── data/
├── eval/
│   ├── ground_truth_rag.json
│   └── rag_eval_report.json
├── scripts/
│   ├── evaluate_rag.py
│   ├── ingest_data.py
│   ├── seed_metrics.py
│   └── seed_user.py
├── static/
│   ├── chat-react.js
│   ├── chat.js
│   ├── login-react.js
│   ├── login.js
│   └── styles.css
└── templates/
    ├── chat.html
    └── login.html
```

## 1) Prerequisites

- Python 3.11+
- ODBC Driver 18 for SQL Server
- Reachable Azure SQL Server database

## 2) Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with:

- `AZURE_SQL_CONNECTION_STRING`
- `OPENAI_API_KEY`
- Optional model overrides

## 3) Initialize data

Seed a login user:

```bash
python -m scripts.seed_user --username admin --password "StrongPassword!123" --full-name "Admin User"
```

Ingest files from `data/` (supports `.txt`, `.md`, `.csv`, `.json`):

```bash
python -m scripts.ingest_data --data-dir data
```

## 4) Run app

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open:

- `http://localhost:8000/login`

## 5) Seed and view log metrics dashboard (Streamlit)

Seed exactly 20 metrics into the database:

```bash
python -m scripts.seed_metrics
```

Run Streamlit dashboard:

```bash
streamlit run streamlit_dashboard.py --server.port 8501 --server.address 0.0.0.0
```

Open:

- `http://localhost:8501`

## 6) Production hardening checklist

- Replace `APP_SECRET_KEY` with a secure random value
- Use HTTPS and secure cookie settings in deployment
- Restrict network access to Azure SQL by IP/VNet
- Add DB migrations (Alembic) and CI/CD pipeline
- Add request rate limiting and structured logging
- Add monitoring/alerts and secret management (Key Vault)
