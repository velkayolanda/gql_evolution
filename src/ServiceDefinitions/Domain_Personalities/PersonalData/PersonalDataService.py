from uoishelpers.dataloaders.IDLoader import IDLoader

from src.DBDefinitions import PersonalDataModel
from src.ServiceDefinitions.BaseService import BaseService
from src.ServiceDefinitions.ServiceContext import ServiceContext


class PersonalDataService(BaseService[IDLoader[PersonalDataModel]]):
    dbModel = PersonalDataModel

    @classmethod
    async def getLoader(cls, ctx: ServiceContext) -> IDLoader[PersonalDataModel]:
        return ctx.loaders.PersonalDataModel