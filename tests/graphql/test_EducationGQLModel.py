from __future__ import annotations

import pytest
from tests.support.asserts import assert_insert, assert_update, assert_delete, assert_same


async def education_insert(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("educationInsert")
    return await SchemaExecutor(query=query, variable_values=variables)


async def education_update(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("educationUpdate")
    return await SchemaExecutor(query=query, variable_values=variables)


async def education_delete(SchemaExecutor, CreateMutation, variables):
    query = CreateMutation("educationDelete")
    return await SchemaExecutor(query=query, variable_values=variables)


@pytest.mark.asyncio
async def test_education_insert(SchemaExecutor, CreateMutation, RolePermissionSchemaExtensionOverride):
    education = {
        "institutionName": "Test University",
        "degree": "Bc.",
    }
    result = await education_insert(SchemaExecutor, CreateMutation, education)
    assert_insert(result)


@pytest.mark.asyncio
async def test_education_update(SchemaExecutor, CreateMutation, RolePermissionSchemaExtensionOverride):
    education = {
        "institutionName": "Test University",
        "degree": "Bc.",
    }
    delta = {"degree": "Mgr."}

    result = await education_insert(SchemaExecutor, CreateMutation, education)
    inserted = assert_insert(result)

    payload = {**education, **inserted, **delta}
    result = await education_update(SchemaExecutor, CreateMutation, payload)
    updated = assert_update(result)
    assert_same(delta, updated)


@pytest.mark.asyncio
async def test_education_delete(SchemaExecutor, CreateMutation, RolePermissionSchemaExtensionOverride):
    education = {
        "institutionName": "Test University",
        "degree": "Bc.",
    }
    result = await education_insert(SchemaExecutor, CreateMutation, education)
    inserted = assert_insert(result)

    payload = {**education, **inserted}
    result = await education_delete(SchemaExecutor, CreateMutation, payload)
    assert_delete(result)