import datetime
from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.now(datetime.timezone.utc),
)]


class Documents(Base):
    __tablename__ = 'documents'

    id: Mapped[intpk]
    path: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
