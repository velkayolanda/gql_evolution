import strawberry
from .Domain_Events import Query_Domain_Events
from .Domain_Personalities.PersonalData import Query_Domain_PersonalData
from .Domain_Personalities.Education import Query_Domain_Education
from .Domain_Personalities.Certificates import Query_Domain_Certificates


@strawberry.type(description='Root query')
class Query(Query_Domain_Events, Query_Domain_PersonalData, Query_Domain_Education, Query_Domain_Certificates):
    pass
