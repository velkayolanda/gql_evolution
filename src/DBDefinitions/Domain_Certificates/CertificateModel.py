import datetime
from sqlalchemy import String, Date, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.DBDefinitions.BaseModel import BaseDBModel, IDType


class CertificateModel(BaseDBModel):
    """
    Záznam o konkrétním získaném certifikátu nebo diplomu pro osobu.
    """
    __tablename__ = "certificates"

    # --- Cizí klíče ---
    # Přidáno default=None
    personality_id: Mapped[IDType] = mapped_column(
        ForeignKey("personaldata.id"),
        index=True,
        nullable=False,
        default=None,
        comment="Osoba, které certifikát patří"
    )

    # --- Datové atributy ---
    title: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None,
        comment="Specifický název certifikátu (např. Cambridge English: Advanced)"
    )

    issuer: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None,
        comment="Vydávající instituce"
    )

    certificate_number: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None,
        comment="Číslo nebo identifikátor certifikátu"
    )

    issued: Mapped[datetime.date] = mapped_column(
        Date,
        nullable=True,
        default=None,
        comment="Datum vydání"
    )

    valid_to: Mapped[datetime.date] = mapped_column(
        Date,
        nullable=True,
        default=None,
        comment="Konec platnosti (pokud je omezená)"
    )

    level: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None,
        comment="Dosažená úroveň (např. C1, SLP 3332)"
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        default=None,
        comment="Doplňující informace"
    )

    # "Soft link" na číselník certifikátů v cizí službě
    certificate_type_id: Mapped[str] = mapped_column(
        String,
        index=True,
        nullable=True,
        default=None,
        comment="Odkaz na typ certifikátu z externí služby gql_personalities"
    )