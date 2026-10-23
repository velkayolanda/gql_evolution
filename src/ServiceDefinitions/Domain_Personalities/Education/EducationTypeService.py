from uoishelpers.dataloaders.IDLoader import IDLoader

from src.DBDefinitions import EducationTypeModel
from src.ServiceDefinitions.BaseService import BaseService
from src.ServiceDefinitions.ServiceContext import ServiceContext


class EducationTypeService(BaseService[IDLoader[EducationTypeModel]]):
    dbModel = EducationTypeModel

    @classmethod
    async def getLoader(cls, ctx: ServiceContext) -> IDLoader[EducationTypeModel]:
        return ctx.loaders.EducationTypeModel