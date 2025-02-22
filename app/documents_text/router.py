from fastapi import APIRouter

from app.documents.repository import DocumentsRepository
from app.documents_text.repository import DocumentsTextRepository
from app.tasks.tasks import make_text_from_img

router = APIRouter(
    prefix="/documents_text",
    tags=["Текст документа"],
)


@router.get('/doc_analyse/{doc_id}')
async def doc_analyse(doc_id: int):
    image_path = await DocumentsRepository.get_document(doc_id)
    make_text_from_img.delay(doc_id, image_path)
    return {"message": "Задача на обработку документа добавлена в очередь."}


@router.get('/get_text/{doc_id}')
async def get_text(doc_id: int):
    text = await DocumentsTextRepository.get_documents_text(doc_id)
    return {"text": text}

