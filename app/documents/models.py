from sqlalchemy.orm import Mapped

from app.database import Base


class Documents(Base):
    __tablename__ = 'documents'

    path: Mapped[str]
