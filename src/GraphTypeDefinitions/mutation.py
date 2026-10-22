import strawberry
from .Domain_Events import Mutation_Domain_Events
from .Domain_Personalities.PersonalData import Mutation_Domain_PersonalData
from .Domain_Personalities.Education import Mutation_Domain_Education
from .Domain_Personalities.Certificates import Mutation_Domain_Certificates


@strawberry.type(description='Root mutation')
class Mutation(Mutation_Domain_Events, Mutation_Domain_PersonalData, Mutation_Domain_Education, Mutation_Domain_Certificates):
    pass
