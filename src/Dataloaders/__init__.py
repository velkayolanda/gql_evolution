from uoishelpers.dataloaders.LoaderMapBase import LoaderMapBase
from uoishelpers.dataloaders.IDLoader import IDLoader

import src.DBDefinitions
from src.DBDefinitions import BaseDBModel, EventModel, EventInvitationModel
from src.DBDefinitions import PersonalDataModel, EducationModel, EducationTypeModel
from src.DBDefinitions import CertificateTypeModel, UserCertificateModel

class LoaderMap(LoaderMapBase[BaseDBModel]):
    BaseModel = BaseDBModel

    EventModel: IDLoader[src.DBDefinitions.EventModel] = None
    EventInvitationModel: IDLoader[src.DBDefinitions.EventInvitationModel] = None
    PersonalDataModel: IDLoader[src.DBDefinitions.PersonalDataModel] = None
    EducationModel: IDLoader[src.DBDefinitions.EducationModel] = None
    EducationTypeModel: IDLoader[src.DBDefinitions.EducationTypeModel] = None
    CertificateTypeModel: IDLoader[src.DBDefinitions.CertificateTypeModel] = None
    UserCertificateModel: IDLoader[src.DBDefinitions.UserCertificateModel] = None

    def __init__(self, session):
        super().__init__(session)
        self.EventModel = self.get(EventModel)
        self.EventInvitationModel = self.get(EventInvitationModel)
        self.PersonalDataModel = self.get(PersonalDataModel)
        self.EducationModel = self.get(EducationModel)
        self.EducationTypeModel = self.get(EducationTypeModel)
        self.CertificateTypeModel = self.get(CertificateTypeModel)
        self.UserCertificateModel = self.get(UserCertificateModel)

    def get_by_name(self, name: str):
        return getattr(self, name)


def createLoadersContext(session):
    """Compatibility helper for places expecting a dict context."""
    return {'loaders': LoaderMap(session)}
