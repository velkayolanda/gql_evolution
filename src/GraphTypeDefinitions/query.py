import strawberry
from src.GraphTypeDefinitions.Domain_Events import Query_Domain_Events
from GraphTypeDefinitions.Domain_Personalities.PersonalData import Query_Domain_PersonalData
from GraphTypeDefinitions.Domain_Personalities.Education import Query_Domain_Education
from GraphTypeDefinitions.Domain_Personalities.Certificates import Query_Domain_Certificates


@strawberry.type(description='Root query')
class Query(Query_Domain_Events, Query_Domain_PersonalData, Query_Domain_Education, Query_Domain_Certificates):
    pass
