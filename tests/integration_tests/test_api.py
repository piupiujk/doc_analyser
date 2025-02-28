from http import HTTPStatus

from httpx import AsyncClient
import pytest

from app.config import settings

@pytest.mark.parametrize('image, status_code', [
    (settings.TEST_IMAGE_64, 200),
    (settings.TEST_IMAGE_64[22:], 200),
    (1, 422),
    ('IMAGE', 200)
])
async def test_upload_doc(image, status_code, ac: AsyncClient):
    response = await ac.post('/documents/upload_doc', json={
        "image_base64": image
    })
    assert response.status_code == status_code

@pytest.mark.parametrize('doc_id, status_code', [
    (1, 200),
    (2, 200),
    (3, 200),
])
async def test_delete_doc(doc_id, status_code, ac: AsyncClient):
    response = await ac.delete(f'/documents/doc_delete/{doc_id}')
    assert response.status_code == status_code