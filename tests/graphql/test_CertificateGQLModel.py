from __future__ import annotations

import pytest
from tests.support.asserts import assert_insert, assert_update, assert_delete, assert_same

# CCNA — always seeded because CertificateTypeModel is a TypeModel (loaded without DEMODATA=True)
CCNA_CERTIFICATE_TYPE_ID = "7c8d9e0f-1a2b-3c4d-5e6f-7a8b9c0d1e2f"


async def personal_data_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("personalDataInsert")
    return await SchemaExecutor(query=query, variable_values=variables)


async def certificate_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("certificateInsert")
    return await SchemaExecutor(query=query, variable_values=variables)


async def certificate_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("certificateUpdate")
    return await SchemaExecutor(query=query, variable_values=variables)


async def certificate_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("certificateDelete")
    return await SchemaExecutor(query=query, variable_values=variables)


@pytest.mark.asyncio
async def test_certificate_insert(SchemaExecutor, CreateMutation, RolePermissionSchemaExtensionOverride):
    pd_result = await personal_data_insert(SchemaExecutor, CreateMutation, {"citizenship": "CZ"})
    pd = assert_insert(pd_result)

    certificate = {
        "userId": pd["id"],
        "certificateId": CCNA_CERTIFICATE_TYPE_ID,
        "isValid": True,
    }
    result = await certificate_insert(SchemaExecutor, CreateMutation, certificate)
    assert_insert(result)


@pytest.mark.asyncio
async def test_certificate_update(SchemaExecutor, CreateMutation, RolePermissionSchemaExtensionOverride):
    pd_result = await personal_data_insert(SchemaExecutor, CreateMutation, {"citizenship": "CZ"})
    pd = assert_insert(pd_result)

    certificate = {
        "userId": pd["id"],
        "certificateId": CCNA_CERTIFICATE_TYPE_ID,
        "isValid": True,
    }
    delta = {"isValid": False}

    result = await certificate_insert(SchemaExecutor, CreateMutation, certificate)
    inserted = assert_insert(result)

    payload = {**certificate, **inserted, **delta}
    result = await certificate_update(SchemaExecutor, CreateMutation, payload)
    updated = assert_update(result)
    assert_same(delta, updated)


@pytest.mark.asyncio
async def test_certificate_delete(SchemaExecutor, CreateMutation, RolePermissionSchemaExtensionOverride):
    pd_result = await personal_data_insert(SchemaExecutor, CreateMutation, {"citizenship": "CZ"})
    pd = assert_insert(pd_result)

    certificate = {
        "userId": pd["id"],
        "certificateId": CCNA_CERTIFICATE_TYPE_ID,
        "isValid": True,
    }
    result = await certificate_insert(SchemaExecutor, CreateMutation, certificate)
    inserted = assert_insert(result)

    payload = {**certificate, **inserted}
    result = await certificate_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)
