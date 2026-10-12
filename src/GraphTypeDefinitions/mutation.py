import strawberry
from src.GraphTypeDefinitions.Domain_Events import Mutation_Domain_Events
from src.GraphTypeDefinitions.Domain_PersonalData import Mutation_Domain_PersonalData


@strawberry.type(description='Root mutation')
class Mutation(Mutation_Domain_Events, Mutation_Domain_PersonalData):
    pass
