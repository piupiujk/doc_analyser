import pytest

from app.config import settings
from app.documents.repository import DocumentsRepository

@pytest.mark.parametrize('document_id, path', [
    (1, settings.TEST_DOCUMENT_PATH),
    (10, None),
])
async def test_get_document(document_id, path):
    document_path = await DocumentsRepository.get_document(document_id)
    assert document_path == path

@pytest.mark.parametrize('document_id', [
    1,
    10,
])
async def test_delete_document(document_id):
    await DocumentsRepository.delete_document(document_id)
    assert await DocumentsRepository.get_document(document_id) is None