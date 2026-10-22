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
class EducationInputFilter:
    personality_id: IDType
    degree: str
    graduated: bool
    id: IDType


@strawberry.federation.type(description='Education record for a person (multiple records per person)', keys=['id'])
class EducationGQLModel(BaseGQLModel):
    LoaderName = 'EducationModel'

    personality_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description='Reference to the person (PersonalData / personality)',
        permission_classes=[OnlyForAuthentized],
    )
    institution_name: typing.Optional[str] = strawberry.field(
        default=None,
        description='Name of the school or institution',
        permission_classes=[OnlyForAuthentized],
    )
    study_program: typing.Optional[str] = strawberry.field(
        default=None,
        description='Study programme or field of study',
        permission_classes=[OnlyForAuthentized],
    )
    degree: typing.Optional[str] = strawberry.field(
        default=None,
        description='Academic degree or qualification obtained',
        permission_classes=[OnlyForAuthentized],
    )
    started: typing.Optional[datetime.date] = strawberry.field(
        default=None,
        description='Start date of the study (year or full date)',
        permission_classes=[OnlyForAuthentized],
    )
    finished: typing.Optional[datetime.date] = strawberry.field(
        default=None,
        description='End date of the study (year or full date)',
        permission_classes=[OnlyForAuthentized],
    )
    graduated: typing.Optional[bool] = strawberry.field(
        default=None,
        description='Whether the person successfully graduated',
        permission_classes=[OnlyForAuthentized],
    )
    description: typing.Optional[str] = strawberry.field(
        default=None,
        description='Additional information about the education record',
        permission_classes=[OnlyForAuthentized],
    )


@strawberry.interface(description='Education queries')
class EducationQuery:
    education_by_id: typing.Optional[EducationGQLModel] = strawberry.field(
        description='Get an education record by its id',
        permission_classes=[OnlyForAuthentized],
        resolver=EducationGQLModel.load_with_loader,
    )
    education_page: typing.List[EducationGQLModel] = strawberry.field(
        description='Get a page of education records',
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[EducationGQLModel](whereType=EducationInputFilter),
    )


@strawberry.input(description='Input for creating an Education record')
class EducationInsertGQLModel(InputModelMixin):
    getLoader = EducationGQLModel.getLoader

    personality_id: typing.Optional[IDType] = strawberry.field(description='Reference to the person (personality)', default=None)
    institution_name: typing.Optional[str] = strawberry.field(description='Name of the school or institution', default=None)
    study_program: typing.Optional[str] = strawberry.field(description='Study programme or field of study', default=None)
    degree: typing.Optional[str] = strawberry.field(description='Academic degree or qualification', default=None)
    started: typing.Optional[datetime.date] = strawberry.field(description='Start date of the study', default=None)
    finished: typing.Optional[datetime.date] = strawberry.field(description='End date of the study', default=None)
    graduated: typing.Optional[bool] = strawberry.field(description='Whether the person successfully graduated', default=None)
    description: typing.Optional[str] = strawberry.field(description='Additional information', default=None)
    id: typing.Optional[IDType] = strawberry.field(description='Explicit id (optional)', default=None)
    createdby_id: strawberry.Private[IDType] = None
    rbacobject_id: strawberry.Private[IDType] = None


@strawberry.input(description='Input for updating an Education record')
class EducationUpdateGQLModel:
    id: IDType = strawberry.field(description='Id of the record to update')
    lastchange: datetime.datetime = strawberry.field(description='Optimistic locking timestamp')
    institution_name: typing.Optional[str] = strawberry.field(description='Name of the school or institution', default=strawberry.UNSET)
    study_program: typing.Optional[str] = strawberry.field(description='Study programme or field of study', default=strawberry.UNSET)
    degree: typing.Optional[str] = strawberry.field(description='Academic degree or qualification', default=strawberry.UNSET)
    started: typing.Optional[datetime.date] = strawberry.field(description='Start date of the study', default=strawberry.UNSET)
    finished: typing.Optional[datetime.date] = strawberry.field(description='End date of the study', default=strawberry.UNSET)
    graduated: typing.Optional[bool] = strawberry.field(description='Whether the person successfully graduated', default=strawberry.UNSET)
    description: typing.Optional[str] = strawberry.field(description='Additional information', default=strawberry.UNSET)
    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(description='Input for deleting an Education record')
class EducationDeleteGQLModel:
    id: IDType = strawberry.field(description='Id of the record to delete')
    lastchange: datetime.datetime = strawberry.field(description='Optimistic locking timestamp')


@strawberry.interface(description='Education mutations')
class EducationMutation:
    @strawberry.mutation(
        description='Create a new Education record',
        permission_classes=[OnlyForAuthentized],
    )
    async def education_insert(
        self, info: ApplicationInfo, education: EducationInsertGQLModel
    ) -> typing.Union[EducationGQLModel, InsertError[EducationGQLModel]]:
        service = info.ServiceCtx.Services.EducationService
        return await service.ExecuteServiceMethod(
            service.Create(ctx=info.ServiceCtx, entity=education),
            Error=service.CreateErrorCallback(
                ErrorClass=InsertError[EducationGQLModel],
                code='a1b2c3d4-e5f6-7890-abcd-ef1234560001',
                location='education_insert',
                _input=education,
            ),
            OK=EducationGQLModel.from_dataclass,
        )

    @strawberry.mutation(
        description='Update an existing Education record',
        permission_classes=[OnlyForAuthentized],
    )
    async def education_update(
        self, info: ApplicationInfo, education: EducationUpdateGQLModel
    ) -> typing.Union[EducationGQLModel, UpdateError[EducationGQLModel]]:
        service = info.ServiceCtx.Services.EducationService
        return await service.ExecuteServiceMethod(
            service.Update(ctx=info.ServiceCtx, entity=education),
            Error=service.CreateErrorCallback(
                ErrorClass=UpdateError[EducationGQLModel],
                code='b2c3d4e5-f6a7-8901-bcde-f12345670001',
                location='education_update',
                _input=education,
            ),
            OK=EducationGQLModel.from_dataclass,
        )

    @strawberry.mutation(
        description='Delete an Education record',
        permission_classes=[OnlyForAuthentized],
    )
    async def education_delete(
        self, info: ApplicationInfo, education: EducationDeleteGQLModel
    ) -> typing.Optional[DeleteError[EducationGQLModel]]:
        service = info.ServiceCtx.Services.EducationService
        return await service.ExecuteServiceMethod(
            service.Delete(ctx=info.ServiceCtx, entity=education),
            Error=service.CreateErrorCallback(
                ErrorClass=DeleteError[EducationGQLModel],
                code='c3d4e5f6-a7b8-9012-cdef-123456780001',
                location='education_delete',
                _input=education,
            ),
            OK=lambda result: None,
        )