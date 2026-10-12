import strawberry

from .PersonalDataGQLModel import (
    PersonalDataGQLModel, PersonalDataInputFilter,
    PersonalDataMutation, PersonalDataQuery,
)


@strawberry.interface(description='PersonalData domain queries')
class Query_Domain_PersonalData(PersonalDataQuery):
    pass


@strawberry.interface(description='PersonalData domain mutations')
class Mutation_Domain_PersonalData(PersonalDataMutation):
    pass


__all__ = [
    'PersonalDataGQLModel', 'PersonalDataInputFilter',
    'Query_Domain_PersonalData', 'Mutation_Domain_PersonalData',
]