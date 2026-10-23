import dataclasses
import typing

from src.Dataloaders import LoaderMap

if typing.TYPE_CHECKING:
    from src.ServiceDefinitions.Domain_Events.EventService import EventService as _EventService
    from src.ServiceDefinitions.Domain_Events.EventInvitationService import EventInvitationService as _EventInvitationService
    from ServiceDefinitions.Domain_Personalities.PersonalData.PersonalDataService import PersonalDataService as _PersonalDataService
    from ServiceDefinitions.Domain_Personalities.Education.EducationService import EducationService as _EducationService
    from ServiceDefinitions.Domain_Personalities.Certificates import CertificateTypeService as _CertificateTypeService
    from ServiceDefinitions.Domain_Personalities.Certificates.UserCertificateService import UserCertificateService as _UserCertificateService

@dataclasses.dataclass(frozen=True)
class ServiceRegistry:
    @property
    def EventService(self) -> type['_EventService']:
        from src.ServiceDefinitions.Domain_Events.EventService import EventService
        return EventService

    @property
    def EventInvitationService(self) -> type['_EventInvitationService']:
        from src.ServiceDefinitions.Domain_Events.EventInvitationService import EventInvitationService
        return EventInvitationService

    @property
    def PersonalDataService(self) -> type['_PersonalDataService']:
        from ServiceDefinitions.Domain_Personalities.PersonalData.PersonalDataService import PersonalDataService
        return PersonalDataService

    @property
    def EducationService(self) -> type['_EducationService']:
        from ServiceDefinitions.Domain_Personalities.Education.EducationService import EducationService
        return EducationService

    @property
    def CertificateTypeService(self) -> type['_CertificateTypeService']:
        from ServiceDefinitions.Domain_Personalities.Certificates import CertificateTypeService
        return CertificateTypeService

    @property
    def UserCertificateService(self) -> type['_UserCertificateService']:
        from ServiceDefinitions.Domain_Personalities.Certificates.UserCertificateService import UserCertificateService
        return UserCertificateService

SERVICES = ServiceRegistry()


@dataclasses.dataclass
class ServiceContext:
    loaders: LoaderMap
    user: typing.Any = None
    ug_client: typing.Callable[..., typing.Awaitable[typing.Any]] | None = None
    request: typing.Any = None
    session: typing.Any = None
    Services: ServiceRegistry = SERVICES

    # uoishelpers helpers commonly expect info.context to behave like a dict
    # with at least the key "loaders". Keeping these methods lets us pass a
    # typed ServiceContext directly as Strawberry context.
    def __getitem__(self, key: str) -> typing.Any:
        return getattr(self, key)

    def get(self, key: str, default: typing.Any = None) -> typing.Any:
        return getattr(self, key, default)

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)
