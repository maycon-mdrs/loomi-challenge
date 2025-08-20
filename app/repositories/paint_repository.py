from sqlalchemy.orm import Session
from app.models.paint_model import PaintModel


class PaintRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        
    def get_all(self) -> list[PaintModel]:
        return self.db_session.query(PaintModel).all()
    
    def get_by_id(self, paint_id: int) -> PaintModel:
        return self.db_session.query(PaintModel).filter(PaintModel.id == paint_id).first()
    
    def get_paints_by_name(self, name: str) -> list[PaintModel]:
        return self.db_session.query(PaintModel).filter(
            PaintModel.paint_name.ilike(f"%{name}%")
        ).all()
    
    def get_paints_by_color(self, color: str) -> list[PaintModel]:
        return self.db_session.query(PaintModel).filter(
            PaintModel.color.ilike(f"%{color}%")
        ).all()
    
    def get_by_name_and_color(self, name: str, color: str) -> PaintModel:
        return self.db_session.query(PaintModel).filter(
            PaintModel.paint_name.ilike(name),
            PaintModel.color.ilike(color)
        ).first()
    
    def create(self, paint: PaintModel) -> PaintModel:
        self.db_session.add(paint)
        self.db_session.commit()
        self.db_session.refresh(paint)
        return paint
    
    def update(self, paint_id: int, updated_paint: dict) -> PaintModel:
        paint = self.get_by_id(paint_id)
        if not paint:
            return None
        for key, value in updated_paint.items():
            setattr(paint, key, value)
        self.db_session.commit()
        self.db_session.refresh(paint)
        return paint
        
    def delete(self, paint_id: int) -> bool:
        paint = self.get_by_id(paint_id)
        if paint:
            self.db_session.delete(paint)
            self.db_session.commit()
            return True
        return False
