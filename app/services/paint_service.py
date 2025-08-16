from sqlalchemy.orm import Session

from app.DTOs.paint_dtos import PaintRegister
from app.models.paint_model import EnvironmentPaintEnum, PaintModel
from app.repositories.paint_repository import PaintRepository
from app.exceptions.paint_exceptions import PaintAlreadyExistsException, PaintCreationException, PaintNotFoundException, InvalidPaintDataException


class PaintService:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.paint_repository = PaintRepository(db_session)

    def create_paint(self, paint: PaintRegister) -> PaintModel:
        existing_paint = self._get_paint_by_name(paint.paint_name)
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
            return self.paint_repository.create(paint)
        except Exception:
            raise PaintCreationException()

    def update_paint(self, paint_id, updated_paint) -> PaintModel:
        paint = self.paint_repository.get_by_id(paint_id)
        try:
            return self.paint_repository.update(paint.id, updated_paint)
        except Exception:
            raise InvalidPaintDataException()

    def get_all_paints(self) -> list[PaintModel]:
        return self.paint_repository.get_all()

    def get_paint_by_id(self, paint_id) -> PaintModel:
        paint = self.paint_repository.get_by_id(paint_id)
        if not paint:
            raise PaintNotFoundException()
        return paint

    def _get_paint_by_name(self, name: str) -> PaintModel:
        return self.paint_repository.get_by_name(name)

    def get_paint_by_name(self, name: str) -> PaintModel:
        paint = self.paint_repository.get_by_name(name)
        if not paint:
            raise PaintNotFoundException()
        return paint

    def delete_paint(self, paint_id) -> bool:
        paint = self.paint_repository.get_by_id(paint_id)
        return self.paint_repository.delete(paint.id)
