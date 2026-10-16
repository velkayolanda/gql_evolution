import datetime
from sqlalchemy import Date, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.DBDefinitions.BaseModel import BaseDBModel, IDType


class UserCertificateModel(BaseDBModel):
    """
    Spojovací tabulka pro přiřazení konkrétního certifikátu konkrétní osobě.
    """
    __tablename__ = "user_certificates"

    # --- Cizí klíče ---
    user_id: Mapped[IDType] = mapped_column(
        ForeignKey("personaldata.id"),
        index=True,
        nullable=False,
        default=None,
        comment="ID uživatele/osoby"
    )

    certificate_id: Mapped[IDType] = mapped_column(
        ForeignKey("certificate_types.id"),
        index=True,
        nullable=False,
        default=None,
        comment="ID typu certifikátu z číselníku"
    )

    # --- Datové atributy ---
    issue_date: Mapped[datetime.date] = mapped_column(
        Date,
        nullable=True,
        default=None,
        comment="Datum vydání"
    )

    expiration_date: Mapped[datetime.date] = mapped_column(
        Date,
        nullable=True,
        default=None,
        comment="Konec platnosti (datum expirace)"
    )

    is_valid: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True,
        default=None,
        comment="Příznak, zda je certifikát aktuálně platný (nebyl zrušen/odebrán)"
    )