import strawberry
from src.GraphTypeDefinitions.Domain_Events import Mutation_Domain_Events
from src.GraphTypeDefinitions.Domain_PersonalData import Mutation_Domain_PersonalData
from src.GraphTypeDefinitions.Domain_Education import Mutation_Domain_Education


@strawberry.type(description='Root mutation')
class Mutation(Mutation_Domain_Events, Mutation_Domain_PersonalData, Mutation_Domain_Education):
    pass
