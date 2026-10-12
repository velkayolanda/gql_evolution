import strawberry
from src.GraphTypeDefinitions.Domain_Events import Query_Domain_Events
from src.GraphTypeDefinitions.Domain_PersonalData import Query_Domain_PersonalData
from src.GraphTypeDefinitions.Domain_Education import Query_Domain_Education


@strawberry.type(description='Root query')
class Query(Query_Domain_Events, Query_Domain_PersonalData, Query_Domain_Education):
    pass
