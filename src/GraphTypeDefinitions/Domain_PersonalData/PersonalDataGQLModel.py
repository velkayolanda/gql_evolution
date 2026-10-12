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
class PersonalDataInputFilter:
    user_id: IDType
    citizenship: str
    nationality: str
    id: IDType


@strawberry.federation.type(description='Personal data of a user (max 1 per user)', keys=['id'])
class PersonalDataGQLModel(BaseGQLModel):
    LoaderName = 'PersonalDataModel'

    user_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description='Federation reference to UserGQLModel',
        permission_classes=[OnlyForAuthentized],
    )
    # birth_number is sensitive; full authorization enforcement added in the permission class below
    birth_number: typing.Optional[str] = strawberry.field(
        default=None,
        description='Birth number (rodné číslo) – sensitive personal data, restricted access',
        permission_classes=[OnlyForAuthentized],
    )
    birth_date: typing.Optional[datetime.date] = strawberry.field(
        default=None,
        description='Date of birth',
        permission_classes=[OnlyForAuthentized],
    )
    birth_place: typing.Optional[str] = strawberry.field(
        default=None,
        description='Place of birth',
        permission_classes=[OnlyForAuthentized],
    )
    citizenship: typing.Optional[str] = strawberry.field(
        default=None,
        description='State citizenship',
        permission_classes=[OnlyForAuthentized],
    )
    nationality: typing.Optional[str] = strawberry.field(
        default=None,
        description='Nationality (optional)',
        permission_classes=[OnlyForAuthentized],
    )
    personal_title: typing.Optional[str] = strawberry.field(
        default=None,
        description='Personal title or additional designation',
        permission_classes=[OnlyForAuthentized],
    )
    note: typing.Optional[str] = strawberry.field(
        default=None,
        description='Free-text note',
        permission_classes=[OnlyForAuthentized],
    )



@strawberry.interface(description='PersonalData queries')
class PersonalDataQuery:
    personal_data_by_id: typing.Optional[PersonalDataGQLModel] = strawberry.field(
        description='Get personal data record by its id',
        permission_classes=[OnlyForAuthentized],
        resolver=PersonalDataGQLModel.load_with_loader,
    )
    personal_data_page: typing.List[PersonalDataGQLModel] = strawberry.field(
        description='Get a page of personal data records',
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[PersonalDataGQLModel](whereType=PersonalDataInputFilter),
    )


@strawberry.input(description='Input for creating a PersonalData record')
class PersonalDataInsertGQLModel(InputModelMixin):
    getLoader = PersonalDataGQLModel.getLoader

    user_id: typing.Optional[IDType] = strawberry.field(description='Federation reference to User', default=None)
    birth_number: typing.Optional[str] = strawberry.field(description='Birth number – sensitive', default=None)
    birth_date: typing.Optional[datetime.date] = strawberry.field(description='Date of birth', default=None)
    birth_place: typing.Optional[str] = strawberry.field(description='Place of birth', default=None)
    citizenship: typing.Optional[str] = strawberry.field(description='State citizenship', default=None)
    nationality: typing.Optional[str] = strawberry.field(description='Nationality', default=None)
    personal_title: typing.Optional[str] = strawberry.field(description='Personal title', default=None)
    note: typing.Optional[str] = strawberry.field(description='Note', default=None)
    id: typing.Optional[IDType] = strawberry.field(description='Explicit id (optional)', default=None)
    createdby_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private[IDType] = None


@strawberry.input(description='Input for updating a PersonalData record')
class PersonalDataUpdateGQLModel:
    id: IDType = strawberry.field(description='Id of the record to update')
    lastchange: datetime.datetime = strawberry.field(description='Optimistic locking timestamp')
    birth_number: typing.Optional[str] = strawberry.field(description='Birth number – sensitive', default=strawberry.UNSET)
    birth_date: typing.Optional[datetime.date] = strawberry.field(description='Date of birth', default=strawberry.UNSET)
    birth_place: typing.Optional[str] = strawberry.field(description='Place of birth', default=strawberry.UNSET)
    citizenship: typing.Optional[str] = strawberry.field(description='State citizenship', default=strawberry.UNSET)
    nationality: typing.Optional[str] = strawberry.field(description='Nationality', default=strawberry.UNSET)
    personal_title: typing.Optional[str] = strawberry.field(description='Personal title', default=strawberry.UNSET)
    note: typing.Optional[str] = strawberry.field(description='Note', default=strawberry.UNSET)
    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(description='Input for deleting a PersonalData record')
class PersonalDataDeleteGQLModel:
    id: IDType = strawberry.field(description='Id of the record to delete')
    lastchange: datetime.datetime = strawberry.field(description='Optimistic locking timestamp')


@strawberry.interface(description='PersonalData mutations')
class PersonalDataMutation:
    @strawberry.mutation(
        description='Create a new PersonalData record',
        permission_classes=[OnlyForAuthentized],
    )
    async def personal_data_insert(
        self, info: ApplicationInfo, personal_data: PersonalDataInsertGQLModel
    ) -> typing.Union[PersonalDataGQLModel, InsertError[PersonalDataGQLModel]]:
        service = info.ServiceCtx.Services.PersonalDataService
        return await service.ExecuteServiceMethod(
            service.Create(ctx=info.ServiceCtx, entity=personal_data),
            Error=service.CreateErrorCallback(
                ErrorClass=InsertError[PersonalDataGQLModel],
                code='c2980f1a-eb73-4cd7-960b-94bf16dfa001',
                location='personal_data_insert',
                _input=personal_data,
            ),
            OK=PersonalDataGQLModel.from_dataclass,
        )

    @strawberry.mutation(
        description='Update an existing PersonalData record',
        permission_classes=[OnlyForAuthentized],
    )
    async def personal_data_update(
        self, info: ApplicationInfo, personal_data: PersonalDataUpdateGQLModel
    ) -> typing.Union[PersonalDataGQLModel, UpdateError[PersonalDataGQLModel]]:
        service = info.ServiceCtx.Services.PersonalDataService
        return await service.ExecuteServiceMethod(
            service.Update(ctx=info.ServiceCtx, entity=personal_data),
            Error=service.CreateErrorCallback(
                ErrorClass=UpdateError[PersonalDataGQLModel],
                code='665aecd2-16a4-4560-a828-e043ee61e001',
                location='personal_data_update',
                _input=personal_data,
            ),
            OK=PersonalDataGQLModel.from_dataclass,
        )

    @strawberry.mutation(
        description='Delete a PersonalData record',
        permission_classes=[OnlyForAuthentized],
    )
    async def personal_data_delete(
        self, info: ApplicationInfo, personal_data: PersonalDataDeleteGQLModel
    ) -> typing.Optional[DeleteError[PersonalDataGQLModel]]:
        service = info.ServiceCtx.Services.PersonalDataService
        return await service.ExecuteServiceMethod(
            service.Delete(ctx=info.ServiceCtx, entity=personal_data),
            Error=service.CreateErrorCallback(
                ErrorClass=DeleteError[PersonalDataGQLModel],
                code='4e9caf74-4dce-4c11-bfe3-278f822c0001',
                location='personal_data_delete',
                _input=personal_data,
            ),
            OK=lambda result: None,
        )
