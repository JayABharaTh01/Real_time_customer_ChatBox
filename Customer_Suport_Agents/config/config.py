import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR=Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "config" / ".env")

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY"," ")
FAISS_PATH=os.getenv("RAG_FAISS_PATH",str(BASE_DIR / "data" / "faiss_index"))
CHAT_MEMORY_WINDOW=int(os.getenv("CHAT_MEMORY_WINDOW","20"))


if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is required in .env")