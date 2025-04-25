import chromadb
from chromadb.utils import embedding_functions

class ShortTermMemory:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("short_term")

    def add_document(self, doc_id: str, content: str):
        self.collection.add(
            documents=[content],
            ids=[doc_id]
        )

    def query_memory(self, query: str, top_k: int = 3):
        return self.collection.query(query_texts=[query], n_results=top_k)
