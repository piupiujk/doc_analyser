import datetime

from dotenv import load_dotenv
import os

from sqlalchemy import BIGINT, NullPool, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from app.config import get_db_url, get_test_db_url, settings

load_dotenv()

if settings.MODE == "TEST":
    DATABASE_URL = get_test_db_url()
    DATABASE_PARAMS = {'poolclass': NullPool}
else:
    DATABASE_URL = get_db_url()
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    type_annotation_map = {
        BIGINT: BIGINT
    }

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.now(datetime.timezone.utc),
    )
