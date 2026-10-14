import strawberry

from .CertificateGQLModel import (
    CertificateGQLModel, CertificateInputFilter,
    CertificateQuery, CertificateMutation,
)


@strawberry.interface(description='Certificate domain queries')
class Query_Domain_Certificates(CertificateQuery):
    pass


@strawberry.interface(description='Certificate domain mutations')
class Mutation_Domain_Certificates(CertificateMutation):
    pass


__all__ = [
    'CertificateGQLModel', 'CertificateInputFilter',
    'Query_Domain_Certificates', 'Mutation_Domain_Certificates',
]