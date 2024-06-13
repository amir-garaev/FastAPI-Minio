# from uuid import uuid4
#
# from config import DATABASE_URL
# from contextvars import Token
# from sqlalchemy.sql.expression import Update, Delete, Insert
# from typing import Union
#
# from sqlalchemy.ext.asyncio import (
#     AsyncSession,
#     create_async_engine,
#     async_scoped_session,
# )
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session
#
#
# session_context = str(uuid4())
#
# engines = {
#     "writer": create_async_engine(DATABASE_URL, pool_recycle=3600),
#     "reader": create_async_engine(DATABASE_URL, pool_recycle=3600),
# }
#
#
# class RoutingSession(Session):
#     def get_bind(self, mapper=None, clause=None, **kw):
#         if self._flushing or isinstance(clause, (Update, Delete, Insert)):
#             return engines["writer"].sync_engine
#         else:
#             return engines["reader"].sync_engine
#
#
# def get_session_context() -> str:
#     return session_context
#
#
# def set_session_context(session_id: str) -> Token:
#     session_context = session_id
#
#
# def reset_session_context(context: Token) -> None:
#     session_context = context
#
#
# async_session_factory = sessionmaker(
#     class_=AsyncSession,
#     sync_session_class=RoutingSession,
#     expire_on_commit=False
# )
#
# session: Union[AsyncSession, async_scoped_session] = async_scoped_session(
#     session_factory=async_session_factory,
#     scopefunc=get_session_context,
# )
# Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from base.models import Base
from config import DATABASE_URL


SQLALCHEMY_DATABASE_URI = DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()