from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect
from flask import request
from flask import jsonify

from model import Session, Sale, User
from schemas import *
from schemas.sale import sale_show
from schemas.user import user_show

info = Info(title="Financial Control API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
sale_tag = Tag(
    name="Venda", description="Adição, visualização e remoção de transações à base")
user_tag = Tag(
    name="Usuário", description="Adição, visualização e remoção de transações à base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/sale', tags=[sale_tag], responses={"200": SaleViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_sales(form: SaleSchema):
    """Adiciona uma nova transação a base de dados

    Retorna uma representação das transações.
    """
    data = request.json

    # Crie um novo usuário com os dados recebidos

    new_sale = Sale(
        customer=data.get("customer"),
        product=data.get("product"),
        category=data.get("category"),
        amount=data.get("amount"),
        unitary_value=data.get("unitary_value"),
        total=data.get("amount") * data.get("unitary_value"),
        # createdAt=form.createdAt
    )

    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(new_sale)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return sale_show(new_sale), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Erro de integridade, verifique os valores inseridos"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar nova transação :/"
        return {"mesage": error_msg}, 400


@app.get('/sales', tags=[sale_tag], responses={"200": SaleListSchema, "404": ErrorSchema})
def get_sales():
    """Faz a busca por todas as transações cadastradas

    Retorna uma representação da listagem de transações em formato JSON.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    sales = session.query(Sale).all()

    if not sales:
        # se não há transações cadastradas
        return jsonify({"sales": []}), 200
    else:
        # cria uma lista de dicionários a partir dos objetos Sale
        sales_data = [{"customer": sale.customer,
                       "product": sale.product,
                       "category": sale.category,
                       "amount": sale.amount,
                       "unitary_value": sale.unitary_value,
                       "total": sale.total} for sale in sales]

        return jsonify({"sales": sales_data}), 200


@app.get('/sale', tags=[sale_tag],
         responses={"200": SaleViewSchema, "404": ErrorSchema})
def get_sale(query: SaleSearchSchema):
    """Faz a busca por uma transação a partir de seu ID

    Retorna uma representação das transações.
    """
    sale_id = query.sale_id
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    sale = session.query(Sale).filter(Sale.id == sale_id).first()

    if not sale:
        # se o produto não foi encontrado
        error_msg = "Transação não encontrada na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de produto
        return sale_show(sale), 200


@app.delete('/sale', tags=[sale_tag],
            responses={"200": SaleDelSchema, "404": ErrorSchema})
def del_sale(query: SaleSearchSchema):
    """Deleta uma transação a partir de um ID informado

    Retorna uma mensagem de confirmação da remoção.
    """
    sale_id = query.sale_id

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Sale).filter(Sale.id == sale_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Transação removido", "id": sale_id}
    else:
        # se o produto não foi encontrado
        error_msg = "Transação não encontrada na base :/"
        return {"mesage": error_msg}, 404


@app.post('/user', tags=[user_tag], responses={"200": UserViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_users():
    """Adiciona um novo usuário ao banco de dados a partir dos dados enviados via API

    Retorna uma representação do usuário adicionado.
    """

    # Obtenha os dados do corpo da solicitação POST
    data = request.json

    # Crie um novo usuário com os dados recebidos
    new_user = User(
        display_name=data.get('display_name'),
        email=data.get('email'),
        photo_url=data.get('photo_url'),
    )

    try:
        # Crie uma conexão com o banco de dados
        session = Session()
        # Adicione o novo usuário
        session.add(new_user)
        # Efetue o commit da transação
        session.commit()
        return user_show(new_user), 200

    except IntegrityError as e:
        # Trate os erros de integridade (por exemplo, duplicação de dados)
        error_msg = "Erro de integridade, verifique os valores inseridos"
        return {"message": error_msg}, 409

    except Exception as e:
        # Trate outros erros não previstos
        error_msg = "Não foi possível salvar o novo usuário :/"
        return {"message": error_msg}, 400


@app.get('/user', tags=[user_tag],
         responses={"200": UserViewSchema, "404": ErrorSchema})
def get_user(query: UserSearchSchema):
    """Faz a busca por uma transação a partir de seu ID

    Retorna uma representação das transações.
    """
    user_id = query.user_id
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    sale = session.query(User).filter(User.id == user_id).first()

    if not User:
        # se o produto não foi encontrado
        error_msg = "Transação não encontrada na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de produto
        return user_show(sale), 200
