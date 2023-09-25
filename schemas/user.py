from pydantic import BaseModel
from typing import List
from model.user import User
from datetime import datetime


class UserSchema(BaseModel):
    """ Define como um novo usuário deve ser apresentado
    """

    display_name: str = "Pedro Antunes"
    email: str = "pedro.antunes@gmail.com"
    photo_url: str = "https://lh3.googleusercontent.com/a/ACg8ocIrvpwYhjyX1qm7e6iv36iOKMJPyhmEZ9uqmYoj1HEZhE0=s96-c"
    createdAt = datetime


class UserSearchSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na data de cadastro do usuário.
    """
    user_id: int = 1


class UserViewSchema(BaseModel):
    """ Define como um usuário será retornado.
    """
    id: int = 1
    display_name: str = "Pedro Antunes"
    email: str = "pedro.antunes@gmail.com"
    photo_url: str = "https://lh3.googleusercontent.com/a/ACg8ocIrvpwYhjyX1qm7e6iv36iOKMJPyhmEZ9uqmYoj1HEZhE0=s96-c"
    createdAt: datetime = datetime.today().day


def user_show(user: User):
    """ Retorna uma representação da transação seguindo o schema definido em
        UserViewSchema.
    """
    return {
        "id": user.id,
        "display_name": user.display_name,
        "email": user.email,
        "photo_url": user.photo_url,
        "createdAt": user.createdAt,
    }
