import asyncio

from app.documents_text.repository import DocumentsTextRepository
from app.tasks.celery_conf import celery

from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


@celery.task
def make_text_from_img(doc_id: int, image_path: str):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='rus+eng')
    asyncio.run(DocumentsTextRepository.add_document_text(doc_id, text))
    return f"Текст документа {doc_id} сохранен."
