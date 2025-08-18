from app.database.vector_store import VectorStoreSingleton
from app.models.paint_model import PaintModel
from sqlalchemy.orm import Session


# https://chatgpt.com/share/68a268e2-c86c-800c-ac44-d2d77e098d3a
class PaintEmbeddingService:
    def __init__(self):
        self.vector_store = VectorStoreSingleton.get_instance("paints_collection")

    def _build_text(self, paint: PaintModel) -> str:
        """Defines how the paint data will be converted into text for embeddings"""
        environment = paint.environment.value if hasattr(paint.environment, "value") else str(paint.environment)
        return f"{paint.paint_name} - {paint.color or ''} - {paint.surface_type or ''} - {environment} - {paint.finish_type or ''} - {paint.features or ''} - {paint.line or ''}"

    def add_paint(self, db_session: Session, paint: PaintModel):
        document_text = self._build_text(paint)
        
        metadata = {
            "paint_id": paint.id,
            "color": paint.color,
            "surface_type": paint.surface_type,
            "environment": str(paint.environment),
            "finish_type": paint.finish_type,
            "line": paint.line,
        }

        self.vector_store.add_texts(
            texts=[document_text],      # 🔹 Goes to the "document" column
            metadatas=[metadata],       # 🔹 Goes to the "cmetadata" column
            ids=[str(paint.id)]         # 🔹 Goes to "custom_id"
        )

    def update_paint(self, db_session: Session, paint: PaintModel):
        # remove old embedding and add it again
        self.delete_paint(paint.id)
        self.add_paint(db_session, paint)

    def delete_paint(self, paint_id: int):
        self.vector_store.delete(ids=[str(paint_id)])
