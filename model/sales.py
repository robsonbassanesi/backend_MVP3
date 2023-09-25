from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from typing import Union

from model import Base

# estrtutura da tabela de vendas que será criada


class Sale(Base):
    __tablename__ = 'sales'

    id = Column("pk_date", Integer, primary_key=True)
    customer = Column(String(140))
    product = Column(String(140))
    category = Column(String(140))
    amount = Column(Integer)
    unitary_value = Column(Float)
    total = Column(Float)
    user_id = Column(Integer)
    createdAt = Column(DateTime, default=datetime.now())

    def __init__(self, customer: str, product: str, category: str, unitary_value: float, total: float, amount: float, user_id: int, createdAt: Union[DateTime, None] = None):

        self.customer = customer
        self.product = product
        self.category = category
        self.amount = amount
        self.unitary_value = unitary_value
        self.total = unitary_value * amount
        self.user_id = user_id

        # se não for informada, será o data exata da inserção no banco
        if createdAt:
            self.createdAt = createdAt
