import datetime
from sqlalchemy import Date, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.DBDefinitions.BaseModel import BaseDBModel, IDType

class UserCertificateModel(BaseDBModel):
    """
    Spojovací tabulka pro přiřazení konkrétního certifikátu konkrétní osobě.
    Zaznamenává reálný stav (kdy byl vydán a do kdy platí).
    """
    __tablename__ = "user_certificates"

    # --- Cizí klíče ---
    user_id: Mapped[IDType] = mapped_column(
        ForeignKey("personal_data.id"),
        index=True,
        nullable=False,
        default=None,
        comment="Cizí klíč na konkrétní osobu (uživatele), která certifikát vlastní"
    )

    certificate_id: Mapped[IDType] = mapped_column(
        ForeignKey("certificate_types.id"),
        index=True,
        nullable=False,
        default=None,
        comment="Cizí klíč propojující uživatele s konkrétním typem certifikátu z katalogu"
    )

    # --- Datové atributy ---
    issue_date: Mapped[datetime.date] = mapped_column(
        Date,
        nullable=True,
        default=None,
        comment="Reálné datum, kdy byl certifikát uživateli oficiálně vydán"
    )

    expiration_date: Mapped[datetime.date] = mapped_column(
        Date,
        nullable=True,
        default=None,
        comment="Datum plánovaného konce platnosti (expirace) certifikátu pro daného uživatele"
    )

    is_valid: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True,
        default=None,
        comment="Příznak platnosti: True, pokud je certifikát aktivní a nebyl uživateli předčasně odebrán"
    )