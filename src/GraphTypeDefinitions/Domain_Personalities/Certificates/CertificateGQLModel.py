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


@createInputs2
class CertificateInputFilter:
    user_id: IDType
    certificate_id: IDType
    is_valid: bool
    id: IDType


@strawberry.federation.type(description='Assignment of a certificate type to a person (user_certificates table)', keys=['id'])
class CertificateGQLModel(BaseGQLModel):
    LoaderName = 'UserCertificateModel'

    user_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description='Reference to PersonalData (personal_data.id)',
        permission_classes=[OnlyForAuthentized],
    )
    certificate_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description='Reference to CertificateTypeModel (certificate_types.id)',
        permission_classes=[OnlyForAuthentized],
    )
    issue_date: typing.Optional[datetime.date] = strawberry.field(
        default=None,
        description='Date the certificate was issued',
        permission_classes=[OnlyForAuthentized],
    )
    expiration_date: typing.Optional[datetime.date] = strawberry.field(
        default=None,
        description='Expiration date of the certificate',
        permission_classes=[OnlyForAuthentized],
    )
    is_valid: typing.Optional[bool] = strawberry.field(
        default=None,
        description='Whether the certificate is currently valid',
        permission_classes=[OnlyForAuthentized],
    )


@strawberry.interface(description='Certificate queries')
class CertificateQuery:
    certificate_by_id: typing.Optional[CertificateGQLModel] = strawberry.field(
        description='Get a user certificate record by its id',
        permission_classes=[OnlyForAuthentized],
        resolver=CertificateGQLModel.load_with_loader,
    )
    certificate_page: typing.List[CertificateGQLModel] = strawberry.field(
        description='Get a page of user certificate records with optional filtering',
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[CertificateGQLModel](whereType=CertificateInputFilter),
    )


@strawberry.input(description='Input for creating a user certificate record')
class CertificateInsertGQLModel(InputModelMixin):
    getLoader = CertificateGQLModel.getLoader

    user_id: typing.Optional[IDType] = strawberry.field(description='Reference to PersonalData (personal_data.id)', default=None)
    certificate_id: typing.Optional[IDType] = strawberry.field(description='Reference to CertificateTypeModel', default=None)
    issue_date: typing.Optional[datetime.date] = strawberry.field(description='Issue date', default=None)
    expiration_date: typing.Optional[datetime.date] = strawberry.field(description='Expiration date', default=None)
    is_valid: typing.Optional[bool] = strawberry.field(description='Whether the certificate is valid', default=None)
    id: typing.Optional[IDType] = strawberry.field(description='Explicit id (optional)', default=None)
    createdby_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private[IDType] = None


@strawberry.input(description='Input for updating a user certificate record')
class CertificateUpdateGQLModel:
    id: IDType = strawberry.field(description='Id of the record to update')
    lastchange: datetime.datetime = strawberry.field(description='Optimistic locking timestamp')
    issue_date: typing.Optional[datetime.date] = strawberry.field(description='Issue date', default=strawberry.UNSET)
    expiration_date: typing.Optional[datetime.date] = strawberry.field(description='Expiration date', default=strawberry.UNSET)
    is_valid: typing.Optional[bool] = strawberry.field(description='Whether the certificate is valid', default=strawberry.UNSET)
    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(description='Input for deleting a user certificate record')
class CertificateDeleteGQLModel:
    id: IDType = strawberry.field(description='Id of the record to delete')
    lastchange: datetime.datetime = strawberry.field(description='Optimistic locking timestamp')


@strawberry.interface(description='Certificate mutations')
class CertificateMutation:
    @strawberry.mutation(
        description='Create a new user certificate record',
        permission_classes=[OnlyForAuthentized],
    )
    async def certificate_insert(
        self, info: ApplicationInfo, certificate: CertificateInsertGQLModel
    ) -> typing.Union[CertificateGQLModel, InsertError[CertificateGQLModel]]:
        service = info.ServiceCtx.Services.UserCertificateService
        return await service.ExecuteServiceMethod(
            service.Create(ctx=info.ServiceCtx, entity=certificate),
            Error=service.CreateErrorCallback(
                ErrorClass=InsertError[CertificateGQLModel],
                code='a1111111-b222-c333-d444-e55555555551',
                location='certificate_insert',
                _input=certificate,
            ),
            OK=CertificateGQLModel.from_dataclass,
        )

    @strawberry.mutation(
        description='Update an existing user certificate record',
        permission_classes=[OnlyForAuthentized],
    )
    async def certificate_update(
        self, info: ApplicationInfo, certificate: CertificateUpdateGQLModel
    ) -> typing.Union[CertificateGQLModel, UpdateError[CertificateGQLModel]]:
        service = info.ServiceCtx.Services.UserCertificateService
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
        description='Delete a user certificate record',
        permission_classes=[OnlyForAuthentized],
    )
    async def certificate_delete(
        self, info: ApplicationInfo, certificate: CertificateDeleteGQLModel
    ) -> typing.Optional[DeleteError[CertificateGQLModel]]:
        service = info.ServiceCtx.Services.UserCertificateService
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
