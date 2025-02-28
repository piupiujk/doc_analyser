from fastapi import APIRouter

from app.documents.router import router as router_docs
from app.documents_text.router import router as router_docs_text

router = APIRouter()

router.include_router(router_docs)
router.include_router(router_docs_text)
