import datetime
from typing import Annotated

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.documents.models import Documents

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.now(datetime.timezone.utc),
)]


class DocumentsText(Base):
    __tablename__ = 'documents_text'

    id: Mapped[intpk]
    id_doc: Mapped[int] = mapped_column(ForeignKey('documents.id', ondelete='CASCADE'))
    text: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
