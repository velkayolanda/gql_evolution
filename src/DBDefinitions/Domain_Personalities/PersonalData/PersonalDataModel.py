import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.DBDefinitions.BaseModel import BaseDBModel, UUIDFKey, IDType


class PersonalDataModel(BaseDBModel):
    __tablename__ = "personal_data"
    __table_args__ = (UniqueConstraint("user_id", name="uq_personaldata_user_id"),)

    # soft federation reference – User lives in a different service
    user_id: Mapped[IDType] = UUIDFKey(nullable=True, comment="federation reference to UserGQLModel")

    birth_number: Mapped[str] = mapped_column(default=None, nullable=True, comment="sensitive – birth number (rodné číslo)")
    birth_date: Mapped[datetime.date] = mapped_column(default=None, nullable=True)
    birth_place: Mapped[str] = mapped_column(default=None, nullable=True)
    citizenship: Mapped[str] = mapped_column(default=None, nullable=True)
    nationality: Mapped[str] = mapped_column(default=None, nullable=True)
    personal_title: Mapped[str] = mapped_column(default=None, nullable=True)
    note: Mapped[str] = mapped_column(default=None, nullable=True)
