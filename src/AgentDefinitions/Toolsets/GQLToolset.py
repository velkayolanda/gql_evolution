from __future__ import annotations

import json

from pydantic_ai import RunContext
from pydantic_ai.toolsets import FunctionToolset

from ..Context import AgentContext


def create_gql_toolset() -> FunctionToolset[AgentContext]:
    toolset = FunctionToolset[AgentContext]()

    @toolset.tool
    async def list_personal_data(
        ctx: RunContext[AgentContext],
        limit: int = 50,
    ) -> str:
        """
        Return a list of personal data records stored in the system.

        Each record belongs to exactly one user and contains personal identity
        information: birth date, birth place, citizenship, nationality,
        personal title and a free-text note.

        Use this to browse all personal data records or to find records for
        specific users.
        """
        query = """
        query PersonalDataPage($limit: Int!) {
          personalDataPage(limit: $limit) {
            id
            userId
            birthDate
            birthPlace
            citizenship
            nationality
            personalTitle
            note
          }
        }
        """
        result = await ctx.deps.executor(query, {"limit": limit})
        records = (result.get("data") or {}).get("personalDataPage", [])
        errors = result.get("errors")
        if errors:
            return f"GraphQL errors: {json.dumps(errors, default=str)}"
        if not records:
            return "No personal data records found."
        return json.dumps(records, default=str, ensure_ascii=False, indent=2)

    @toolset.tool
    async def get_personal_data_by_id(
        ctx: RunContext[AgentContext],
        id: str,
    ) -> str:
        """
        Return a single personal data record identified by its UUID.

        Use this when you already know the specific record id and need its
        full details: birth date, birth place, citizenship, nationality,
        personal title, note.
        """
        query = """
        query PersonalDataById($id: UUID!) {
          personalDataById(id: $id) {
            id
            userId
            birthDate
            birthPlace
            citizenship
            nationality
            personalTitle
            note
          }
        }
        """
        result = await ctx.deps.executor(query, {"id": id})
        errors = result.get("errors")
        if errors:
            return f"GraphQL errors: {json.dumps(errors, default=str)}"
        record = (result.get("data") or {}).get("personalDataById")
        if record is None:
            return f"No personal data record found with id={id}."
        return json.dumps(record, default=str, ensure_ascii=False, indent=2)

    @toolset.tool
    async def list_education_records(
        ctx: RunContext[AgentContext],
        limit: int = 50,
    ) -> str:
        """
        Return a list of education records stored in the system.

        Each record captures one study period for a person: institution name,
        study programme, academic degree, start date, end date, graduation
        status and an optional description.

        Use this to browse all education history, find records for specific
        degrees, institutions or study programmes.
        """
        query = """
        query EducationPage($limit: Int!) {
          educationPage(limit: $limit) {
            id
            personalityId
            institutionName
            studyProgram
            degree
            started
            finished
            graduated
            description
          }
        }
        """
        result = await ctx.deps.executor(query, {"limit": limit})
        errors = result.get("errors")
        if errors:
            return f"GraphQL errors: {json.dumps(errors, default=str)}"
        records = (result.get("data") or {}).get("educationPage", [])
        if not records:
            return "No education records found."
        return json.dumps(records, default=str, ensure_ascii=False, indent=2)

    @toolset.tool
    async def get_education_by_id(
        ctx: RunContext[AgentContext],
        id: str,
    ) -> str:
        """
        Return a single education record identified by its UUID.

        Use this when you already know the specific record id and need its
        full details: institution, programme, degree, dates, graduation status.
        """
        query = """
        query EducationById($id: UUID!) {
          educationById(id: $id) {
            id
            personalityId
            institutionName
            studyProgram
            degree
            started
            finished
            graduated
            description
          }
        }
        """
        result = await ctx.deps.executor(query, {"id": id})
        errors = result.get("errors")
        if errors:
            return f"GraphQL errors: {json.dumps(errors, default=str)}"
        record = (result.get("data") or {}).get("educationById")
        if record is None:
            return f"No education record found with id={id}."
        return json.dumps(record, default=str, ensure_ascii=False, indent=2)

    @toolset.tool
    async def list_certificates(
        ctx: RunContext[AgentContext],
        limit: int = 50,
    ) -> str:
        """
        Return a list of certificate records stored in the system.

        Each record represents a qualification or certification held by a
        person: title, issuing organisation, certificate number, issue date,
        expiry date, level and an optional description.

        Use this to browse all certificates or to find specific qualifications.
        """
        query = """
        query CertificatePage($limit: Int!) {
          certificatePage(limit: $limit) {
            id
            personalityId
            certificateTypeId
            title
            issuer
            certificateNumber
            issued
            validTo
            level
            description
          }
        }
        """
        result = await ctx.deps.executor(query, {"limit": limit})
        errors = result.get("errors")
        if errors:
            return f"GraphQL errors: {json.dumps(errors, default=str)}"
        records = (result.get("data") or {}).get("certificatePage", [])
        if not records:
            return "No certificate records found."
        return json.dumps(records, default=str, ensure_ascii=False, indent=2)

    @toolset.tool
    async def get_certificate_by_id(
        ctx: RunContext[AgentContext],
        id: str,
    ) -> str:
        """
        Return a single certificate record identified by its UUID.

        Use this when you already know the specific record id and need its
        full details: title, issuer, number, issue/expiry dates, level.
        """
        query = """
        query CertificateById($id: UUID!) {
          certificateById(id: $id) {
            id
            personalityId
            certificateTypeId
            title
            issuer
            certificateNumber
            issued
            validTo
            level
            description
          }
        }
        """
        result = await ctx.deps.executor(query, {"id": id})
        errors = result.get("errors")
        if errors:
            return f"GraphQL errors: {json.dumps(errors, default=str)}"
        record = (result.get("data") or {}).get("certificateById")
        if record is None:
            return f"No certificate record found with id={id}."
        return json.dumps(record, default=str, ensure_ascii=False, indent=2)

    return toolset