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
    user_id: int = 1
    createdAt = datetime


class SaleSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na data de inserção da venda.
    """
    sale_id: int = 1


class SalesSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na data de inserção da venda.
    """
    user_id: int = 1


class SaleListSchema(BaseModel):
    """ Define como uma listagem de venda será retornada.
    """
    user_id: int = 1
    sales: List[SaleSchema]


def sales_show(sales: List[Sale], user_id: int):
    """ Retorna uma representação da venda seguindo o schema definido em
        SaleListSchema, filtrando as vendas pelo ID do usuário.
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
            "user_id": sale.user_id,
            "createdAt": sale.createdAt,
        })

    return {"user_id": user_id, "sales": result}


class SaleViewSchema(BaseModel):
    """ Define como uma venda será retornada
    """
    id: int = 1
    customer: str = "Pedro Antunes"
    product: str = "tenis nike"
    category: str = "calçados"
    amount: int = 1
    unitary_value: float = 550
    total: float = 550
    user_id: int = 1
    createdAt: datetime = datetime.today().day


class SaleDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    title: str


def sale_show(sale: Sale):
    """ Retorna uma representação da transação seguindo o schema definido em
        SaleViewSchema.
    """
    return {
        "id": sale.id,
        "customer": sale.customer,
        "product": sale.product,
        "category": sale.category,
        "amount": sale.amount,
        "unitary_value": sale.unitary_value,
        "total": sale.unitary_value * sale.amount,
        "user_id": sale.user_id,
        "createdAt": sale.createdAt,
    }
