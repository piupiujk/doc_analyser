from http import HTTPStatus

from fastapi import APIRouter

from app.documents.repository import DocumentsRepository
from app.documents_text.repository import DocumentsTextRepository
from app.documents_text.schemas import Analyse
from app.tasks.tasks import make_text_from_img

router = APIRouter(
    prefix="/documents_text",
    tags=["Текст документа"],
)


@router.get('/doc_analyse/{doc_id}',
            summary='Считать текст с документа',
            description='<h1>Считывает текст с документа и добавляет его в бд<h1>',
            response_model=Analyse)
async def doc_analyse(doc_id: int):
    image_path = await DocumentsRepository.get_document(doc_id)
    if not image_path:
        return {
            "status_code": HTTPStatus.BAD_REQUEST,
            "id": doc_id,
            "message": f"Файла с id {doc_id} не существует"
        }
    make_text_from_img.delay(doc_id, image_path)
    return {
        "status_code": HTTPStatus.ACCEPTED,
        "id": doc_id,
        "message": "Задача успешно добавлена в очередь"
    }


@router.get('/get_text/{doc_id}',
            summary='Получить текст документа',
            description='<h1>Получить текст документа из бд<h1>',
            response_model=Analyse)
async def get_text(doc_id: int):
    text = await DocumentsTextRepository.get_documents_text(doc_id)
    return {
        "status_code": HTTPStatus.ACCEPTED,
        "id": doc_id,
        "message": text
    }
