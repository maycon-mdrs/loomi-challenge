import pandas as pd
from app.config import crypt_context
from app.models.paint_model import EnvironmentPaintEnum
from app.DTOs.paint_dtos import PaintRegister
from app.services.paint_service import PaintService
from app.models.user_model import UserModel, UserRole
from app.repositories.user_repository import UserRepository


class SeedService:
    @staticmethod
    def populate_all(db_session, csv_path: str):
        user_repository = UserRepository(db_session)

        # Users
        if not user_repository.get_by_email("admin@example.com"):
            admin = UserModel(
                first_name="Admin",
                last_name="User",
                email="admin@example.com",
                password=crypt_context.hash("123"),
                role=UserRole.ADMIN,
            )
            user_repository.create(admin)
        if not user_repository.get_by_email("user@example.com"):
            user = UserModel(
                first_name="Normal",
                last_name="User",
                email="user@example.com",
                password=crypt_context.hash("123"),
                role=UserRole.USER,
            )
            user_repository.create(user)

        # Paints by CSV
        SeedService.populate_paints_from_csv(db_session, csv_path)

    @staticmethod
    def populate_paints_from_csv(db_session, csv_path: str):
        paint_service = PaintService(db_session)
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            paint_name = row.get("nome")
            color = row.get("cor", "")
            if not paint_name or not color:
                continue
            # Check if it already exists
            try:
                paint_service.get_paint_by_name_and_color(paint_name, color)
                continue  # Already exists, skip
            except Exception:
                pass  # Does not exist, can create

            ambiente = row.get("ambiente", "Interno/Externo")
            if ambiente == "Interno/Externo":
                ambiente_enum = EnvironmentPaintEnum.AMBOS
            elif ambiente == "Interno":
                ambiente_enum = EnvironmentPaintEnum.INTERNO
            elif ambiente == "Externo":
                ambiente_enum = EnvironmentPaintEnum.EXTERNO
            else:
                ambiente_enum = EnvironmentPaintEnum.AMBOS

            paint_dto = PaintRegister(
                paint_name=paint_name,
                color=color,
                surface_type=row.get("tipo_parede", ""),
                environment=ambiente_enum,
                finish_type=row.get("acabamento", ""),
                features=row.get("features", ""),
                line=row.get("linha", ""),
            )
            paint_service.create_paint(paint_dto)
