import os
import asyncio

import pytest

from app.config import settings
from app.database import Base, async_session_maker, engine

from app.documents.models import Documents
from app.documents_text.models import DocumentsText

from fastapi.testclient import TestClient
from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        test_document = Documents(path=settings.TEST_DOCUMENT_PATH)
        session.add(test_document)
        await session.commit()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        yield ac

# @pytest.fixture(scope="function")
# async def session():
#     async with async_session_maker() as session:
#         yield session
