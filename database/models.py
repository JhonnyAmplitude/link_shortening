from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid
import os


SCHEMA_NAME = os.getenv("DB_SCHEMA")


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False, unique=True)
    login = Column(String(25), nullable=False, unique=True)
    password = Column(String(), nullable=False)

    __table_args__ = {'schema': SCHEMA_NAME}
    