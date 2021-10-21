from uuid import uuid4

from sqlalchemy import Column, String, Boolean

from service.db.base_class import Base


class User(Base):
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
