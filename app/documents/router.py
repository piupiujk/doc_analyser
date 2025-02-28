import base64
import os
import uuid
from http import HTTPStatus

from fastapi import APIRouter

from app.documents.repository import DocumentsRepository
from app.documents.schemas import UploadDeleteResponse, SDoc

router = APIRouter(
    prefix="/documents",
    tags=["Документы"],
)

UPLOAD_DIR = 'documents_image'
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post('/upload_doc',
             summary='Добавить документ',
             description='<h1>Добавить документ в формате b64<h1>',
             response_model=UploadDeleteResponse)
async def upload_doc(image_base64: SDoc):
    try:
        if 'base64,' in image_base64.image_base64:
            cut = image_base64.image_base64.find('base64,') + 7
            image_base64 = image_base64.image_base64[cut:]  # надо обрезать часть data:image/png;base64, если она есть
        image_data = base64.b64decode(image_base64)
    except Exception as e:
        return {"status_code": HTTPStatus.BAD_REQUEST,
                "id": -1,
                "message": f"Ошибка при обработке изображения: {str(e)}"}

    number_doc = uuid.uuid4().hex
    filename = f'image_{number_doc}.png'

    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, 'wb') as image:
            image.write(image_data)
        document = await DocumentsRepository.add_document(file_path)
        return {"status_code": HTTPStatus.CREATED,
                "id": document.id,
                "message": f"Изображение успешно сохранено как {filename}"}
    except Exception as e:
        return {"status_code": HTTPStatus.BAD_REQUEST,
                "id": -1,
                "message": f"Ошибка при обработке изображения: {str(e)}"}


@router.delete('/doc_delete/{doc_id}',
               summary='Удалить документ',
               description='<h1>Удаляет документ из бд и диска<h1>',
               response_model=UploadDeleteResponse)
async def doc_delete(doc_id: int):
    path = await DocumentsRepository.get_document(doc_id)
    if not path:
        return {"status_code": HTTPStatus.BAD_REQUEST,
                "id": doc_id,
                "message": f"Файла с id {doc_id} не существует"}
    path = path[16:]
    for doc in os.listdir(UPLOAD_DIR):
        if path in doc:
            os.remove(os.path.join(UPLOAD_DIR, doc))
            await DocumentsRepository.delete_document(doc_id)
            return {"status_code": HTTPStatus.ACCEPTED,
                    "id": doc_id,
                    "message": f"Файл успешно удален"}
