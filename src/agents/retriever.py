from src.retrieval.retriever import retrieve_documents
from src.retrieval.query_embedding import generate_query_embedding

class RetrieverAgent:
    def retrieve(self, question, max_documents=5):
        embedding=generate_query_embedding(question)
        return retrieve_documents(embedding, top_k=max_documents)
    