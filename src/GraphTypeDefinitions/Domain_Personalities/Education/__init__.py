import strawberry

from .EducationGQLModel import (
    EducationGQLModel, EducationInputFilter,
    EducationMutation, EducationQuery,
)


@strawberry.interface(description='Education domain queries')
class Query_Domain_Education(EducationQuery):
    pass


@strawberry.interface(description='Education domain mutations')
class Mutation_Domain_Education(EducationMutation):
    pass


__all__ = [
    'EducationGQLModel', 'EducationInputFilter',
    'Query_Domain_Education', 'Mutation_Domain_Education',
]