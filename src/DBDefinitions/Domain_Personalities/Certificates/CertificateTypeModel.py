from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.DBDefinitions.BaseModel import BaseDBModel, IDType

class CertificateTypeModel(BaseDBModel):
    """
    Katalog typů certifikátů (číselník).
    Tato tabulka udržuje hierarchickou strukturu (strom) všech dostupných
    certifikátů a jejich kategorií (např. kategorie Angličtina -> STANAG 6001).
    """
    __tablename__ = "certificate_types"

    # --- Konfigurace stromu pro BaseService ---
    path_attribute_name = "path"
    parent_attribute_name = "master_certificate_type"
    parent_id_attribute_name = "master_certificate_type_id"
    children_attribute_name = "sub_certificate_types"

    # --- Datové atributy ---
    path: Mapped[str] = mapped_column(
        String,
        index=True,
        nullable=True,
        default=None,
        comment="Materiálová cesta (Materialized path) pro rychlé vyhledávání položek a jejich kategorií ve stromu"
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None,
        comment="Oficiální název typu certifikátu nebo obecné kategorie (např. 'STANAG 6001' nebo 'Sítě')"
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=True,
        default=None,
        comment="Detailní popis certifikátu, k čemu slouží a jaké jsou požadavky k jeho získání"
    )

    validity: Mapped[str] = mapped_column(
        String,
        nullable=True,
        default=None,
        comment="Standardní délka platnosti certifikátu zadaná textově (např. '3 roky', 'neomezeně')"
    )

    # --- Stromové vazby (Hierarchie) ---
    master_certificate_type_id: Mapped[IDType] = mapped_column(
        ForeignKey("certificate_types.id"),
        nullable=True,
        default=None,
        index=True,
        comment="Cizí klíč odkazující na nadřazenou kategorii; null znamená, že jde o hlavní uzel"
    )

    master_certificate_type = relationship(
        "CertificateTypeModel",
        viewonly=True,
        remote_side="CertificateTypeModel.id",
        uselist=False,
        back_populates="sub_certificate_types",
    )

    sub_certificate_types = relationship(
        "CertificateTypeModel",
        back_populates="master_certificate_type",
        uselist=True,
        cascade="save-update"
    )