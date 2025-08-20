from sqlalchemy import Column, Integer, String, DateTime, Text, Enum as SqlEnum, func, UniqueConstraint
from enum import Enum
from app.database.base import Base


class EnvironmentPaintEnum(Enum):
	INTERNO = "INTERNO"
	EXTERNO = "EXTERNO"
	AMBOS = "AMBOS"


class PaintModel(Base):
	__tablename__ = "paints"
	__table_args__ = (
        UniqueConstraint('paint_name', 'color', name='uq_paint_name_color'),
    )

	id = Column(Integer, primary_key=True, index=True)
	paint_name = Column(String, nullable=False)
	color = Column(String, nullable=False)
	surface_type = Column(String, nullable=False)
	environment = Column(SqlEnum(EnvironmentPaintEnum), nullable=False)   # indoor, outdoor, both
	finish_type = Column(String, nullable=False)
	features = Column(Text, nullable=True)              				  # lavável, anti-mofo, sem odor, etc.
	line = Column(String, nullable=True)                				  # Premium, Standard, etc.
 
	created_by = Column(Integer, nullable=True)
	updated_at = Column('updated_at', DateTime(), onupdate=func.now())
