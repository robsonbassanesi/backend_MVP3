from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect, request, jsonify
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

JWT_SECRET_KEY = "5QgmGbi)las}r}B~{h6WKw15{f+B"


def auth_middleware(next):
    def middleware():
        authorization = request.headers.get("Authorization")

        if not authorization:
            return jsonify({"error": "Token not provided"}), 401

        _, token = authorization.split(" ")

        try:
            decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            user_id = decoded["id"]

            request.user_id = user_id
            return next()
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token invalid"}), 401

    return middleware


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/sale', tags=[sale_tag], responses={"200": SaleViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_sales(form: SaleSchema):
    """Adiciona uma nova transação à base de dados

    Retorna uma representação das transações.
    """
    try:
        # Crie uma nova venda com os dados recebidos
        new_sale = Sale(
            customer=form.customer,
            product=form.product,
            category=form.category,
            amount=form.amount,
            unitary_value=form.unitary_value,
            total=form.amount * form.unitary_value,
            user_id=form.user_id,
        )
        print(new_sale)

        # Criando conexão com a base de dados
        session = Session()

        # Adicione a venda à sessão
        session.add(new_sale)

        # Efetue a operação de commit para salvar a nova venda no banco de dados
        session.commit()

        # Retorne a representação da nova venda
        return sale_show(new_sale), 200

    except IntegrityError as e:
        # Como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Erro de integridade, verifique os valores inseridos"
        return {"message": error_msg}, 409

    except Exception as e:
        # Caso ocorra um erro inesperado
        error_msg = "Não foi possível salvar a nova transação :/"
        return {"message": error_msg}, 400


@app.get('/sales', tags=[sale_tag], responses={"200": SaleListSchema, "404": ErrorSchema})
def get_sales(query: SalesSearchSchema):
    """Faz a busca por todas as transações cadastradas do usuário logado

    Retorna uma representação da listagem de transações.
    """
    try:
        # criando conexão com a base
        user_id = query.user_id
        session = Session()

        # fazendo a busca por vendas relacionadas ao usuário logado
        sales = session.query(Sale).filter_by(user_id=user_id).all()

        if not sales:
            # se não há transações cadastradas para esse usuário
            return {"user_id": user_id, "sales": []}, 200
        else:
            # retorna a representação das transações
            return sales_show(sales, user_id), 200
    except Exception as e:
        print("Erro na rota /sales:", str(e))
        return {"message": "Erro interno na API"}, 500


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
def add_user(form: UserSchema):
    """Adiciona um novo usuário ao banco de dados ou permite o login se o usuário já existir.

    Retorna uma representação do usuário.
    """
    try:
        # Criando conexão com o banco de dados
        session = Session()

        # Verifique se o usuário com o mesmo email já existe
        existing_user = session.query(User).filter_by(email=form.email).first()

        if existing_user:
            # Se o usuário já existir, permita o login
            return user_show(existing_user), 200
        else:
            # Caso contrário, crie um novo usuário
            new_user = User(
                display_name=form.display_name,
                photo_url=form.photo_url,
                email=form.email,
            )

            # Adicione o novo usuário à sessão
            session.add(new_user)

            # Efetue a operação de commit para salvar o novo usuário no banco de dados
            session.commit()

            # Retorne a representação do novo usuário
            return user_show(new_user), 200

    except IntegrityError as e:
        # Como a duplicidade do email é a provável razão do IntegrityError
        error_msg = "Erro de integridade, verifique os valores inseridos"
        return {"message": error_msg}, 409

    except Exception as e:
        # Caso ocorra um erro inesperado
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
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        # se o produto não foi encontrado
        error_msg = "Transação não encontrada na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de produto
        return user_show(user), 200
