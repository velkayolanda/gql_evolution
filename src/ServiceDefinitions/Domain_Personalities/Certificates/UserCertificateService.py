from src.ServiceDefinitions.BaseService import BaseService
from src.DBDefinitions import UserCertificateModel

class UserCertificateService(BaseService):
    dbModel = UserCertificateModel

    @classmethod
    async def getLoader(cls, ctx):
        return ctx.loaders.UserCertificateModel