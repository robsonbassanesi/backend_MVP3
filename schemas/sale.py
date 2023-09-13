from pydantic import BaseModel
from typing import List
from model.sales import Sale
from datetime import datetime


class SaleSchema(BaseModel):
    """ Define como uma nova transação deve ser apresentada
    """

    customer: str = "Pedro Antunes"
    product: str = "tenis nike"
    category: str = "calçados"
    amount: int = 1
    unitary_value: float = 550
    total: float = 550
    createdAt = datetime


class SaleSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na data de inserção da transação.
    """
    sale_id: int = 1


class SaleListSchema(BaseModel):
    """ Define como uma listagem de transações será retornada.
    """
    sales: List[SaleSchema]


def sales_show(sales: List[Sale]):
    """ Retorna uma representação da transação seguindo o schema definido em
        TransactionViewSchema.
    """
    result = []
    for sale in sales:
        result.append({
            "id": sale.id,
            "customer": sale.customer,
            "product": sale.product,
            "category": sale.category,
            "amount": sale.amount,
            "unitary_value": sale.unitary_value,
            "total": sale.total,
            "createdAt": sale.createdAt,
        })

    return {"sales": result}


class SaleViewSchema(BaseModel):
    """ Define como uma transação será retornada
    """
    id: int = 1
    customer: str = "Pedro Antunes"
    product: str = "tenis nike"
    category: str = "calçados"
    amount: int = 1
    unitary_value: float = 550
    total: float = 550
    createdAt: datetime = datetime.today().day


class SaleDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    title: str


def sale_show(sale: Sale):
    """ Retorna uma representação da transação seguindo o schema definido em
        TransactionViewSchema.
    """
    return {
        "id": sale.id,
        "customer": sale.customer,
        "product": sale.product,
        "category": sale.category,
        "amount": sale.amount,
        "unitary_value": sale.unitary_value,
        "total": sale.total,
        "createdAt": sale.createdAt,
    }
