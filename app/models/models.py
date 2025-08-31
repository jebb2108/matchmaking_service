from sqlalchemy import Column, Integer, String, DateTime, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

engine = create_engine('postgresql+asyncpg://onlynone:NonGrata21@localhost:5432/mydb')

class User(Base):
    __tablename__ = "searching_users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, index=True)
    username = Column(String)
    is_searching = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer)
    user2_id = Column(Integer)
    room_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now())
    is_active = Column(Boolean, default=True)

# Создаем все таблицы
Base.metadata.create_all(engine)
# Создаем сессию для работы с БД
Session = sessionmaker(bind=engine)
session = Session()