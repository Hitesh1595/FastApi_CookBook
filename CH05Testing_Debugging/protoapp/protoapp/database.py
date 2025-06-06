from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)

DATABASE_URL = "sqlite:///./production.db"


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(
        primary_key=True, index=True
    )
    name: Mapped[str] = mapped_column(index=True)
    color: Mapped[str]


engine = create_engine(DATABASE_URL)


Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)