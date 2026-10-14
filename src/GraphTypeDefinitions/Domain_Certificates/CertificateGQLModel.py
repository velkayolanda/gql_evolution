import datetime
import typing

import strawberry
from uoishelpers.gqlpermissions import OnlyForAuthentized
from uoishelpers.resolvers import (
    DeleteError,
    InsertError,
    InputModelMixin,
    PageResolver,
    UpdateError,
    createInputs2,
)

from src.GraphTypeDefinitions.ApplicationInfo import ApplicationInfo
from src.GraphTypeDefinitions.BaseGQLModel import BaseGQLModel, IDType

# --- Filtry ---
@createInputs2
class CertificateInputFilter:
    personality_id: IDType
    certificate_type_id: str
    level: str
    id: IDType

# --- Hlavní GQL Model ---
@strawberry.federation.type(description='Záznam o konkrétním získaném certifikátu nebo diplomu', keys=['id'])
class CertificateGQLModel(BaseGQLModel):
    LoaderName = 'CertificateModel'

    personality_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description='Odkaz na osobu (PersonalDataGQLModel)',
        permission_classes=[OnlyForAuthentized],
    )
    certificate_type_id: typing.Optional[str] = strawberry.field(
        default=None,
        description='ID typu certifikátu z modulu gql_personalities',
        permission_classes=[OnlyForAuthentized],
    )
    title: typing.Optional[str] = strawberry.field(
        default=None,
        description='Specifický název certifikátu',
        permission_classes=[OnlyForAuthentized],
    )
    issuer: typing.Optional[str] = strawberry.field(
        default=None,
        description='Vydávající instituce',
        permission_classes=[OnlyForAuthentized],
    )
    certificate_number: typing.Optional[str] = strawberry.field(
        default=None,
        description='Číslo nebo identifikátor certifikátu',
        permission_classes=[OnlyForAuthentized],
    )
    issued: typing.Optional[datetime.date] = strawberry.field(
        default=None,
        description='Datum vydání',
        permission_classes=[OnlyForAuthentized],
    )
    valid_to: typing.Optional[datetime.date] = strawberry.field(
        default=None,
        description='Konec platnosti',
        permission_classes=[OnlyForAuthentized],
    )
    level: typing.Optional[str] = strawberry.field(
        default=None,
        description='Dosažená úroveň',
        permission_classes=[OnlyForAuthentized],
    )
    description: typing.Optional[str] = strawberry.field(
        default=None,
        description='Doplňující informace',
        permission_classes=[OnlyForAuthentized],
    )

# --- Dotazy (Queries) ---
@strawberry.interface(description='Certificate queries')
class CertificateQuery:
    certificate_by_id: typing.Optional[CertificateGQLModel] = strawberry.field(
        description='Získá certifikát podle jeho id',
        permission_classes=[OnlyForAuthentized],
        resolver=CertificateGQLModel.load_with_loader,
    )
    certificate_page: typing.List[CertificateGQLModel] = strawberry.field(
        description='Získá stránku certifikátů s možností filtrace',
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[CertificateGQLModel](whereType=CertificateInputFilter),
    )

# --- Vstupy pro mutace ---
@strawberry.input(description='Input for creating a Certificate record')
class CertificateInsertGQLModel(InputModelMixin):
    getLoader = CertificateGQLModel.getLoader

    personality_id: typing.Optional[IDType] = strawberry.field(description='Odkaz na osobu', default=None)
    certificate_type_id: typing.Optional[str] = strawberry.field(description='Odkaz na typ', default=None)
    title: typing.Optional[str] = strawberry.field(description='Název certifikátu', default=None)
    issuer: typing.Optional[str] = strawberry.field(description='Vydavatel', default=None)
    certificate_number: typing.Optional[str] = strawberry.field(description='Číslo', default=None)
    issued: typing.Optional[datetime.date] = strawberry.field(description='Vydáno', default=None)
    valid_to: typing.Optional[datetime.date] = strawberry.field(description='Platí do', default=None)
    level: typing.Optional[str] = strawberry.field(description='Úroveň', default=None)
    description: typing.Optional[str] = strawberry.field(description='Poznámka', default=None)
    id: typing.Optional[IDType] = strawberry.field(description='Explicit id (optional)', default=None)
    createdby_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private[IDType] = None

@strawberry.input(description='Input for updating a Certificate record')
class CertificateUpdateGQLModel:
    id: IDType = strawberry.field(description='Id of the record to update')
    lastchange: datetime.datetime = strawberry.field(description='Optimistic locking timestamp')
    title: typing.Optional[str] = strawberry.field(description='Název', default=strawberry.UNSET)
    issuer: typing.Optional[str] = strawberry.field(description='Vydavatel', default=strawberry.UNSET)
    certificate_number: typing.Optional[str] = strawberry.field(description='Číslo', default=strawberry.UNSET)
    issued: typing.Optional[datetime.date] = strawberry.field(description='Vydáno', default=strawberry.UNSET)
    valid_to: typing.Optional[datetime.date] = strawberry.field(description='Platí do', default=strawberry.UNSET)
    level: typing.Optional[str] = strawberry.field(description='Úroveň', default=strawberry.UNSET)
    description: typing.Optional[str] = strawberry.field(description='Poznámka', default=strawberry.UNSET)
    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(description='Input for deleting a Certificate record')
class CertificateDeleteGQLModel:
    id: IDType = strawberry.field(description='Id of the record to delete')
    lastchange: datetime.datetime = strawberry.field(description='Optimistic locking timestamp')

# --- Mutace ---
@strawberry.interface(description='Certificate mutations')
class CertificateMutation:
    @strawberry.mutation(
        description='Create a new Certificate record',
        permission_classes=[OnlyForAuthentized],
    )
    async def certificate_insert(
        self, info: ApplicationInfo, certificate: CertificateInsertGQLModel
    ) -> typing.Union[CertificateGQLModel, InsertError[CertificateGQLModel]]:
        service = info.ServiceCtx.Services.CertificateService
        return await service.ExecuteServiceMethod(
            service.Create(ctx=info.ServiceCtx, entity=certificate),
            Error=service.CreateErrorCallback(
                ErrorClass=InsertError[CertificateGQLModel],
                code='a1111111-b222-c333-d444-e55555555551', # Náhodně vygenerované UUID chyby
                location='certificate_insert',
                _input=certificate,
            ),
            OK=CertificateGQLModel.from_dataclass,
        )

    @strawberry.mutation(
        description='Update an existing Certificate record',
        permission_classes=[OnlyForAuthentized],
    )
    async def certificate_update(
        self, info: ApplicationInfo, certificate: CertificateUpdateGQLModel
    ) -> typing.Union[CertificateGQLModel, UpdateError[CertificateGQLModel]]:
        service = info.ServiceCtx.Services.CertificateService
        return await service.ExecuteServiceMethod(
            service.Update(ctx=info.ServiceCtx, entity=certificate),
            Error=service.CreateErrorCallback(
                ErrorClass=UpdateError[CertificateGQLModel],
                code='a1111111-b222-c333-d444-e55555555552',
                location='certificate_update',
                _input=certificate,
            ),
            OK=CertificateGQLModel.from_dataclass,
        )

    @strawberry.mutation(
        description='Delete a Certificate record',
        permission_classes=[OnlyForAuthentized],
    )
    async def certificate_delete(
        self, info: ApplicationInfo, certificate: CertificateDeleteGQLModel
    ) -> typing.Optional[DeleteError[CertificateGQLModel]]:
        service = info.ServiceCtx.Services.CertificateService
        return await service.ExecuteServiceMethod(
            service.Delete(ctx=info.ServiceCtx, entity=certificate),
            Error=service.CreateErrorCallback(
                ErrorClass=DeleteError[CertificateGQLModel],
                code='a1111111-b222-c333-d444-e55555555553',
                location='certificate_delete',
                _input=certificate,
            ),
            OK=lambda result: None,
        )