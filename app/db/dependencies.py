from asyncio import current_task
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

from app.core.settings import settings


def get_db_session() -> Session:
    """
    create sync engine
    """
    engine = create_engine(str(settings.db_url), echo=False)
    session: Session = Session(engine)

    return session
