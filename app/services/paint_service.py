from sqlalchemy.orm import Session

from app.DTOs.paint_dtos import PaintRegister
from app.models.paint_model import EnvironmentPaintEnum, PaintModel
from app.repositories.paint_repository import PaintRepository
from app.exceptions.paint_exceptions import PaintAlreadyExistsException, PaintCreationException, PaintNotFoundException, InvalidPaintDataException
from app.services.paint_embedding_service import PaintEmbeddingService


class PaintService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.paint_repository = PaintRepository(db_session)
        self.embedding_service = PaintEmbeddingService()

    def create_paint(self, paint: PaintRegister) -> PaintModel:
        existing_paint = self.get_paint_by_name_and_color(paint.paint_name, paint.color)
        if existing_paint:
            raise PaintAlreadyExistsException()

        paint = PaintModel(
            paint_name=paint.paint_name,
            color=paint.color,
            surface_type=paint.surface_type,
            environment=EnvironmentPaintEnum(paint.environment),
            finish_type=paint.finish_type,
            features=paint.features,
            line=paint.line,
        )

        try:
            created_paint = self.paint_repository.create(paint)
            # 🔹 creates embedding in the vector
            self.embedding_service.add_paint(self.db_session, created_paint)
            return created_paint
        except Exception as e:
            print(e)
            raise PaintCreationException()

    def update_paint(self, paint_id, updated_paint) -> PaintModel:
        paint = self.get_paint_by_id(paint_id)

        try:
            updated = self.paint_repository.update(paint.id, updated_paint)
            # 🔹 updates embedding
            self.embedding_service.update_paint(self.db_session, updated)
            return updated
        except Exception:
            raise InvalidPaintDataException()

    def delete_paint(self, paint_id) -> bool:
        paint = self.get_paint_by_id(paint_id)
        deleted = self.paint_repository.delete(paint.id)
        if deleted:
            # 🔹 also removes embedding
            self.embedding_service.delete_paint(paint.id)
        return deleted

    def get_all_paints(self) -> list[PaintModel]:
        return self.paint_repository.get_all()

    def get_paint_by_id(self, paint_id) -> PaintModel:
        paint = self.paint_repository.get_by_id(paint_id)
        if not paint:
            raise PaintNotFoundException()
        return paint

    def get_paints_by_name(self, name: str) -> list[PaintModel]:
        return self.paint_repository.get_paints_by_name(name)
    
    def get_paint_by_name_and_color(self, name: str, color: str) -> PaintModel:
        paint = self.paint_repository.get_by_name_and_color(name, color)
        if not paint:
            raise PaintNotFoundException()
        return paint
    
    def get_paints_by_color(self, color: str) -> list[PaintModel]:
        return self.paint_repository.get_paints_by_color(color)
