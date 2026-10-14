import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.DBDefinitions.BaseModel import BaseDBModel, UUIDFKey, IDType


class EducationModel(BaseDBModel):
    __tablename__ = "education"

    # soft federation reference – Personality (PersonalData) lives in the same service
    personality_id: Mapped[IDType] = UUIDFKey(nullable=True, comment="reference to PersonalDataModel / personality")

    institution_name: Mapped[str] = mapped_column(default=None, nullable=True)
    study_program: Mapped[str] = mapped_column(default=None, nullable=True)
    degree: Mapped[str] = mapped_column(default=None, nullable=True)
    started: Mapped[datetime.date] = mapped_column(default=None, nullable=True)
    finished: Mapped[datetime.date] = mapped_column(default=None, nullable=True)
    graduated: Mapped[bool] = mapped_column(default=None, nullable=True)
    description: Mapped[str] = mapped_column(default=None, nullable=True)

    type_id: Mapped[IDType] = mapped_column(
        ForeignKey("educationtypes.id"),
        index=True,
        nullable=True,
        default=None,
        comment="reference to education type tree"
    )
    type = relationship("EducationTypeModel", viewonly=True)