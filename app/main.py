from fastapi import FastAPI

from app.documents.router import router as router_docs
from app.documents_text.router import router as router_docs_text

app = FastAPI(title='Документы', summary='Данное API получает текст из фотографии документа')

app.include_router(router_docs)
app.include_router(router_docs_text)
