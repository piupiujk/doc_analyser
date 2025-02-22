from sqlalchemy import delete, select

from app.database import async_session_maker
from app.documents.models import Documents


class DocumentsRepository:
    @classmethod
    async def add_document(cls, file_path):
        async with async_session_maker() as session:
            new_documents = Documents(path=file_path)
            session.add(new_documents)
            await session.commit()
            await session.refresh(new_documents)
            return new_documents

    @classmethod
    async def get_document(cls, document_id):
        async with async_session_maker() as session:
            query = select(Documents.path).select_from(Documents).where(Documents.id == document_id)
            result = await session.execute(query)
            path = result.scalar()
            return path


    @classmethod
    async def delete_document(cls, document_id):
        async with async_session_maker() as session:
            query = delete(Documents).where(Documents.id == document_id)
            await session.execute(query)
            await session.commit()