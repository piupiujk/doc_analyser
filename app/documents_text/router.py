from fastapi import APIRouter

from app.documents.repository import DocumentsRepository
from app.documents_text.repository import DocumentsTextRepository
from app.tasks.tasks import make_text_from_img

router = APIRouter(
    prefix="/documents_text",
    tags=["Текст документа"],
)


@router.get('/doc_analyse/{doc_id}', summary='Считать текст с документа', description='<h1>Считывает текст с документа и добавляет его в бд<h1>')
async def doc_analyse(doc_id: int):
    image_path = await DocumentsRepository.get_document(doc_id)
    make_text_from_img.delay(doc_id, image_path)
    return {"message": "Задача на обработку документа добавлена в очередь."}


@router.get('/get_text/{doc_id}', summary='Получить текст документа', description='<h1>Получить текст документа из бд<h1>')
async def get_text(doc_id: int):
    text = await DocumentsTextRepository.get_documents_text(doc_id)
    return {"text": text}

