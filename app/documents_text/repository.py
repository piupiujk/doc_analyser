from sqlalchemy import delete, select

from app.database import async_session_maker
from app.documents_text.models import DocumentsText


class DocumentsTextRepository:
    @classmethod
    async def add_document_text(cls, doc_id: int, text: str):
        async with async_session_maker() as session:
            new_documents_text = DocumentsText(id_doc=doc_id, text=text)
            session.add(new_documents_text)
            await session.commit()
            await session.refresh(new_documents_text)

    @classmethod
    async def get_documents_text(cls, doc_id: int):
        async with async_session_maker() as session:
            query = select(DocumentsText.text).select_from(DocumentsText).where(DocumentsText.id_doc == doc_id)
            result = await session.execute(query)
            documents_text = result.scalar()
            return documents_text