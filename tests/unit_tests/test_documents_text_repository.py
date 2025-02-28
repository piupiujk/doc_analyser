import pytest

from app.config import settings
from app.documents_text.models import DocumentsText
from app.documents_text.repository import DocumentsTextRepository

@pytest.mark.parametrize('doc_id, text', [
    (1, 'ДЛЯ ТЕСТОВ')
])
async def test_add_document_text(doc_id, text):
    new_documents_text = DocumentsText(id_doc=doc_id, text=text)
    assert new_documents_text.id_doc == doc_id
    assert new_documents_text.text == text

@pytest.mark.parametrize('doc_id, text', [
    (1, 'ДЛЯ ТЕСТОВ'), # комментировать при тесте удаления
    # (2, 'ДЛЯ ТЕСТОВ'), # комментировать при тесте без удаления
])
async def test_get_documents_text(doc_id, text):
    await DocumentsTextRepository.add_document_text(doc_id=doc_id, text=text)
    doc_text = await DocumentsTextRepository.get_documents_text(doc_id)
    assert doc_text == text

