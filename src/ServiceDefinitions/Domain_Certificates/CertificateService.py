from src.ServiceDefinitions.BaseService import BaseService
from src.DBDefinitions import CertificateModel

class CertificateService(BaseService):
    dbModel = CertificateModel

    @classmethod
    async def getLoader(cls, ctx):
        return ctx.loaders.CertificateModel