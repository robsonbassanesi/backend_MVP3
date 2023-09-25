from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from typing import Union

from model import Base

# estrtutura da tabela de usuários que será criada


class User(Base):
    __tablename__ = 'user'

    id = Column("pk_date", Integer, primary_key=True)
    display_name = Column(String)
    email = Column(String)
    photo_url = Column(String)
    createdAt = Column(DateTime, default=datetime.now())

    def __init__(self, display_name: str, email: str, photo_url: str,
                 createdAt: Union[DateTime, None] = None):

        self.display_name = display_name
        self.email = email
        self.photo_url = photo_url

        # se não for informada, será o data exata da inserção no banco
        if createdAt:
            self.createdAt = createdAt
