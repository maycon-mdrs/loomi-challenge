from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.DTOs.paint_dtos import PaintRegister, PaintResponse, PaintUpdate
from app.services.paint_service import PaintService
from app.utils.depends import get_db_session

paint_router = APIRouter(prefix="/paints", tags=["Paints"])


@paint_router.post("/register", response_model=PaintResponse, status_code=status.HTTP_201_CREATED)
def create_paint(paint: PaintRegister, db_session: Session = Depends(get_db_session)):
    paint_service = PaintService(db_session=db_session)
    paint_model = paint_service.create_paint(paint=paint)
    return PaintResponse(
        id=paint_model.id,
        paint_name=paint_model.paint_name,
        color=paint_model.color,
        surface_type=paint_model.surface_type,
        environment=paint_model.environment,
        finish_type=paint_model.finish_type,
        features=paint_model.features,
        line=paint_model.line,
    )


@paint_router.patch("/{paint_id}", response_model=PaintResponse, status_code=status.HTTP_200_OK)
def update_paint(paint_id: int, paint: PaintUpdate, db_session: Session = Depends(get_db_session)):
    paint_service = PaintService(db_session=db_session)
    updated_paint = paint.model_dump(exclude_unset=True)
    paint_model = paint_service.update_paint(paint_id, updated_paint)
    return PaintResponse(
        id=paint_model.id,
        paint_name=paint_model.paint_name,
        color=paint_model.color,
        surface_type=paint_model.surface_type,
        environment=paint_model.environment,
        finish_type=paint_model.finish_type,
        features=paint_model.features,
        line=paint_model.line,
    )


@paint_router.get("/", response_model=list[PaintResponse])
def get_all_paints(db_session: Session = Depends(get_db_session)):
    paint_service = PaintService(db_session=db_session)
    paints = paint_service.get_all_paints()
    return [
        PaintResponse(
            id=paint.id,
            paint_name=paint.paint_name,
            color=paint.color,
            surface_type=paint.surface_type,
            environment=paint.environment,
            finish_type=paint.finish_type,
            features=paint.features,
            line=paint.line,
        )
        for paint in paints
    ]


@paint_router.get("/{paint_id}", response_model=PaintResponse)
def get_paint_by_id(paint_id: int, db_session: Session = Depends(get_db_session)):
    paint_service = PaintService(db_session=db_session)
    paint = paint_service.get_paint_by_id(paint_id=paint_id)
    return PaintResponse(
        id=paint.id,
        paint_name=paint.paint_name,
        color=paint.color,
        surface_type=paint.surface_type,
        environment=paint.environment,
        finish_type=paint.finish_type,
        features=paint.features,
        line=paint.line,
    )


@paint_router.get("/name/{name}", response_model=PaintResponse)
def get_paint_by_name(name: str, db_session: Session = Depends(get_db_session)):
    paint_service = PaintService(db_session=db_session)
    paint = paint_service.get_paint_by_name(name=name)
    return PaintResponse(
        id=paint.id,
        paint_name=paint.paint_name,
        color=paint.color,
        surface_type=paint.surface_type,
        environment=paint.environment,
        finish_type=paint.finish_type,
        features=paint.features,
        line=paint.line,
    )


@paint_router.delete("/{paint_id}", status_code=status.HTTP_200_OK)
def delete_paint(paint_id: int, db_session: Session = Depends(get_db_session)):
    paint_service = PaintService(db_session=db_session)
    return paint_service.delete_paint(paint_id=paint_id)
