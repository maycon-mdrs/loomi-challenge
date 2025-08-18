# from sqlalchemy.orm import Session
# from langchain_core.documents import Document
# from app.database.vector_store import VectorStoreSingleton
# from app.models.paint_vector_store import PaintVectorStoreModel

# class PaintVectorStoreRepository:
#     def __init__(self, db_session: Session):
#         self.db_session = db_session
#         self.vector_store = VectorStoreSingleton.get_instance("paints_collection")

#     def add_vectors(self, vector_ids: list[str], paint_id: int):
#         self.db_session.add_all([
#             PaintVectorStoreModel(vector_store_id=vector_id, paint_id=paint_id)
#             for vector_id in vector_ids
#         ])
#         self.db_session.commit()

#     def get_vector_ids_by_paint(self, paint_id: int) -> list[str]:
#         result = self.db_session.query(PaintVectorStoreModel.vector_store_id).filter(
#             PaintVectorStoreModel.paint_id == paint_id
#         ).all()
#         return [str(r[0]) for r in result]

#     def delete_vectors_by_paint(self, paint_id: int):
#         self.db_session.query(PaintVectorStoreModel).filter(
#             PaintVectorStoreModel.paint_id == paint_id
#         ).delete()
#         self.db_session.commit()

#     def add_documents(self, documents: list[Document]) -> list[str]:
#         return self.vector_store.add_documents(documents)
        
#     def persist_vector_store(self, vector_ids: list[str], paint_id: int):
#         self.db.add_all([
#             DocumentVectorStoreModel(
#                 vector_store_id=vector_id,
#                 document_id=document_id,
#             )
#             for vector_id in vector_ids
#         ])