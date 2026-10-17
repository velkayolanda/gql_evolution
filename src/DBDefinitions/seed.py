from __future__ import annotations

import datetime
import os
import re
import uuid

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.exc import NoInspectionAvailable

_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')

def _convert_dates(json_data: dict) -> dict:
    """Convert bare ISO date strings (YYYY-MM-DD) to datetime.date objects.
    asyncpg rejects plain strings for DATE columns.
    """
    result = {}
    for table, rows in json_data.items():
        if not isinstance(rows, list):
            result[table] = rows
            continue
        converted = []
        for row in rows:
            new_row = {}
            for k, v in row.items():
                if isinstance(v, str) and _DATE_RE.match(v):
                    try:
                        new_row[k] = datetime.date.fromisoformat(v)
                    except ValueError:
                        new_row[k] = v
                else:
                    new_row[k] = v
            converted.append(new_row)
        result[table] = converted
    return result

from uoishelpers.dataloaders import readJsonFile
from uoishelpers.feeders import ImportModels

from src.DBDefinitions import BaseDBModel
from src.DBDefinitions.Domain_Events.EventTypeModel import EventTypeModel


DEFAULT_EVENT_TYPES = (
    {
        'id': uuid.UUID('11111111-1111-1111-1111-111111111111'),
        'name': 'Událost',
        'name_en': 'Event',
    },
    {
        'id': uuid.UUID('22222222-2222-2222-2222-222222222222'),
        'name': 'Schůzka',
        'name_en': 'Meeting',
    },
)

def is_sqlalchemy_model(cls: type) -> bool:
    """Return True only for SQLAlchemy mapped model classes."""
    try:
        mapper = sa_inspect(cls, raiseerr=False)
        return mapper is not None
    except NoInspectionAvailable:
        return False
    
get_demodata = lambda :readJsonFile(jsonFileName="./systemdata.json")

async def init_database_data(raw_session_factory, get_demodata=get_demodata) -> None:
    """Idempotent seed hook for application startup.

    Keep this function small and explicit. It is called once from
    DatabaseRuntime.start(), after metadata.create_all().
    """

    json_data = _convert_dates(get_demodata())

    Models = [
        mapper.class_
        for mapper in BaseDBModel.registry.mappers
        if is_sqlalchemy_model(mapper.class_)
    ]

    ModelNames = [Model.__name__ for Model in Models]

    TypeNames = [
        Model.__name__
        for Model in Models
        if Model.__name__.endswith("TypeModel")
    ]

    isDemo = os.environ.get("DEMODATA", None) in ["True", "true", True]

    ModelNamesToImport = ModelNames if isDemo else TypeNames

    print(
        f"Importing models: (isDemo = {isDemo})\n{ModelNamesToImport}",
        flush=True,
    )

    ModelsToImport = [
        Model
        for Model in Models
        if Model.__name__ in ModelNamesToImport
        and is_sqlalchemy_model(Model)
        and hasattr(Model, "__tablename__")
    ]
    table_names = [Model.__tablename__ for Model in ModelsToImport]
    modelIndex = dict((DBModel.__tablename__, DBModel) for DBModel in ModelsToImport)
    print(f"Models to import: {ModelsToImport}\nTable names: {table_names}\nModel index: {modelIndex}", flush=True)

    @asynccontextmanager
    async def session_maker():
        session = raw_session_factory()
        try:
            yield session
        finally:
            await session.close()

    await ImportModels(session_maker, ModelsToImport, json_data)

    print("Data initialized", flush=True)
