from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.DBDefinitions.BaseModel import BaseDBModel


class CertificateTypeModel(BaseDBModel):
    """
    Katalog typů certifikátů (číselník).
    """
    __tablename__ = "certificate_types"

    name: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None,
        comment="Název typu certifikátu"
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        default=None,
        comment="Popis certifikátu"
    )

    validity: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None,
        comment="Standardní délka platnosti (např. '3 roky', 'neomezeně')"
    )