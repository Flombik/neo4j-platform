from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from service.settings import settings

connect_args = {"check_same_thread": False} if settings.SQLALCHEMY_DATABASE_URL.startswith('sqlite') else {}

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
