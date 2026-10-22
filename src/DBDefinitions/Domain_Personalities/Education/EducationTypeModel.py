from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.DBDefinitions.BaseModel import BaseDBModel, IDType


class EducationTypeModel(BaseDBModel):
    __tablename__ = "education_types"

    path_attribute_name = "path"
    parent_attribute_name = "parent"
    parent_id_attribute_name = "parent_id"
    children_attribute_name = "children"

    path: Mapped[str] = mapped_column(
        index=True,
        nullable=True,
        default=None,
        comment="Materialized path technique, not implemented"
    )

    name: Mapped[str] = mapped_column(
        default=None,
        nullable=True,
        comment="e.g. Bakalářské studium, Magisterské studium, Doktorské studium"
    )
    name_en: Mapped[str] = mapped_column(default=None, nullable=True)

    parent_id: Mapped[IDType] = mapped_column(
        ForeignKey("education_types.id"),
        index=True,
        nullable=True,
        default=None,
        comment="parent node in the education type tree"
    )

    parent = relationship(
        "EducationTypeModel",
        viewonly=True,
        remote_side="EducationTypeModel.id",
        uselist=False,
    )

    children = relationship(
        "EducationTypeModel",
        back_populates="parent",
        uselist=True,
        init=True,
        cascade="save-update"
    )

    educations = relationship(
        "EducationModel",
        back_populates="type",
        viewonly=True
    )
