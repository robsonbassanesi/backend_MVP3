from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from typing import Union

from model import Base


class Sale(Base):
    __tablename__ = 'Sales'

    id = Column("pk_date", Integer, primary_key=True)
    customer = Column(String(140))
    product = Column(String(140))
    category = Column(String(140))
    amount = Column(Integer)
    unitary_value = Column(Float)
    total = Column(Float)
    createdAt = Column(DateTime, default=datetime.now())

    def __init__(self, customer: str, product: str, category: str, unitary_value: float, total: float, amount: float, createdAt: Union[DateTime, None] = None):

        self.customer = customer
        self.product = product
        self.category = category
        self.amount = amount
        self.unitary_value = unitary_value
        self.total = unitary_value * amount

        # se não for informada, será o data exata da inserção no banco
        if createdAt:
            self.createdAt = createdAt
