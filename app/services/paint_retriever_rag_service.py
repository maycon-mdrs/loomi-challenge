from app.database.vector_store import VectorStoreSingleton

class PaintRetrieverRagService:
    def __init__(self):
        self.paints_retriever = VectorStoreSingleton.get_instance("paints_collection").as_retriever()

    def retrieve_paints(self, question: str):
        return self.paints_retriever.invoke(question)
