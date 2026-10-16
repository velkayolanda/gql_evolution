from src.ServiceDefinitions.BaseService import BaseService
from src.DBDefinitions import CertificateTypeModel

class CertificateTypeService(BaseService):
    dbModel = CertificateTypeModel

    @classmethod
    async def getLoader(cls, ctx):
        return ctx.loaders.CertificateTypeModel