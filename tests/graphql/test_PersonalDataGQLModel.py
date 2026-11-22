from __future__ import annotations

import pytest
from tests.support.asserts import assert_insert, assert_update, assert_delete, assert_same


async def personal_data_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("personalDataInsert")
    return await SchemaExecutor(query=query, variable_values=variables)


async def personal_data_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("personalDataUpdate")
    return await SchemaExecutor(query=query, variable_values=variables)


async def personal_data_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("personalDataDelete")
    return await SchemaExecutor(query=query, variable_values=variables)


@pytest.mark.asyncio
async def test_personal_data_insert(SchemaExecutor, CreateMutation, RolePermissionSchemaExtensionOverride):
    personal_data = {
        "citizenship": "CZ",
        "birthPlace": "Praha",
    }
    result = await personal_data_insert(SchemaExecutor, CreateMutation, personal_data)
    assert_insert(result)


@pytest.mark.asyncio
async def test_personal_data_update(SchemaExecutor, CreateMutation, RolePermissionSchemaExtensionOverride):
    personal_data = {
        "citizenship": "CZ",
        "birthPlace": "Praha",
    }
    delta = {"citizenship": "SK"}

    result = await personal_data_insert(SchemaExecutor, CreateMutation, personal_data)
    inserted = assert_insert(result)

    payload = {**personal_data, **inserted, **delta}
    result = await personal_data_update(SchemaExecutor, CreateMutation, payload)
    updated = assert_update(result)
    assert_same(delta, updated)


@pytest.mark.asyncio
async def test_personal_data_delete(SchemaExecutor, CreateMutation, RolePermissionSchemaExtensionOverride):
    personal_data = {
        "citizenship": "CZ",
        "birthPlace": "Praha",
    }
    result = await personal_data_insert(SchemaExecutor, CreateMutation, personal_data)
    inserted = assert_insert(result)

    payload = {**personal_data, **inserted}
    result = await personal_data_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)