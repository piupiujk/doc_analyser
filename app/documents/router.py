import base64
import os
import uuid

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.documents.repository import DocumentsRepository

router = APIRouter(
    prefix="/documents",
    tags=["Документы"],
)


class SDoc(BaseModel):
    image_base64: str


UPLOAD_DIR = 'documents_image'
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post('/upload_doc')
async def upload_doc(image_base64: SDoc):
    if 'base64,' in image_base64.image_base64:
        cut = image_base64.image_base64.find('base64,') + 7
        image_base64 = image_base64.image_base64[cut:]  # надо обрезать часть data:image/png;base64, если она есть
    image_data = base64.b64decode(image_base64)

    number_doc = uuid.uuid4().hex
    filename = f'image_{number_doc}.png'

    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, 'wb') as image:
            image.write(image_data)
        document = await DocumentsRepository.add_document(file_path)
        return {"message": f"Изображение успешно сохранено как {filename}",
                "id": document.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при обработке изображения: {str(e)}")


@router.delete('/doc_delete/{document_id}')
async def doc_delete(doc_id: int):
    path = await DocumentsRepository.get_document(doc_id)
    if not path:
        return f'Ошибка при удалении файла'
    path = path[16:]
    for doc in os.listdir(UPLOAD_DIR):
        if path in doc:
            os.remove(os.path.join(UPLOAD_DIR, doc))
            await DocumentsRepository.delete_document(doc_id)
            return f'Файл успешно удален'
