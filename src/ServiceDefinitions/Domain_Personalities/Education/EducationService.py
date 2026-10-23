from uoishelpers.dataloaders.IDLoader import IDLoader

from src.DBDefinitions import EducationModel
from src.ServiceDefinitions.BaseService import BaseService
from src.ServiceDefinitions.ServiceContext import ServiceContext


class EducationService(BaseService[IDLoader[EducationModel]]):
    dbModel = EducationModel

    @classmethod
    async def getLoader(cls, ctx: ServiceContext) -> IDLoader[EducationModel]:
        return ctx.loaders.EducationModel