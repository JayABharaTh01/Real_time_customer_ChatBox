
import json
from pathlib import Path
from typing import Dict, List, Optional

from langchain.docstore.document import Document
from langchain.document_loaders import JSONLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

from config.config import FAISS_PATH, OPENAI_API_KEY


class RAGPipeline:
    """RAG pipeline with dummy JSON KB and FAISS vector store."""

    def __init__(self, data_folder: str = None):
        default_data_folder = Path(__file__).resolve().parents[2] / "data"
        self.data_folder = Path(data_folder or default_data_folder)
        self.faiss_path = Path(FAISS_PATH)
        self.embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = None
        self.retriever = None
        self._load_or_build_store()

    def _load_documents(self) -> List[Document]:
        documents: List[Document] = []
        for path in [self.data_folder / "faqs.json", self.data_folder / "policies.json", self.data_folder / "orders.json"]:
            if not path.exists():
                continue
            with open(path, "r", encoding="utf-8") as f:
                items = json.load(f)
            for item in items:
                if path.name == "orders.json":
                    content = f"OrderID: {item.get('order_id','')} status: {item.get('status','')} items: {', '.join(item.get('items', []))}"
                else:
                    question = item.get("question") or item.get("title") or ""
                    answer = item.get("answer") or item.get("body") or ""
                    content = f"{question} {answer}".strip()

                documents.append(Document(page_content=content, metadata=item))
        return documents

    def _load_or_build_store(self):
        if self.faiss_path.exists():
            try:
                self.vectorstore = FAISS.load_local(str(self.faiss_path), self.embedding_model)
            except Exception:
                self.vectorstore = None

        if self.vectorstore is None:
            docs = self._load_documents()
            if not docs:
                docs = [Document(page_content="No docs available", metadata={})]
            self.vectorstore = FAISS.from_documents(docs, self.embedding_model)
            self.faiss_path.mkdir(parents=True, exist_ok=True)
            self.vectorstore.save_local(str(self.faiss_path))

        self.retriever = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    def retrieve_context(self, query: str):
        if not self.retriever:
            raise RuntimeError("Retriever not initialized")
        hits = self.retriever.get_relevant_documents(query)
        return "\n".join([f"{i+1}. {doc.page_content}" for i, doc in enumerate(hits)])

    def retrieve_matches(self, query: str, k: int = 4):
        if not self.retriever:
            raise RuntimeError("Retriever not initialized")
        hits = self.retriever.get_relevant_documents(query, k=k)
        return [
            {
                "rank": i + 1,
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
            for i, doc in enumerate(hits)
        ]

    def answer_with_context(self, query: str) -> str:
        llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.2)
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=False,
        )
        return chain.run(query)

    @staticmethod
    def query_rewrite(query: str) -> str:
        return query.strip().capitalize()