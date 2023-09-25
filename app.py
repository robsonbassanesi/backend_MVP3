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
    name="Venda", description="Adição, visualização e remoção de vendas à base")
user_tag = Tag(
    name="Usuário", description="Adição, visualização de usuários à base")

JWT_SECRET_KEY = "5QgmGbi)las}r}B~{h6WKw15{f+B"


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/sale', tags=[sale_tag], responses={"200": SaleViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_sales(form: SaleSchema):
    """Adiciona uma nova venda à base de dados

    Retorna uma representação das vendas.
    """
    try:
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

        session = Session()

        session.add(new_sale)

        session.commit()

        return sale_show(new_sale), 200

    except IntegrityError as e:
        error_msg = "Erro de integridade, verifique os valores inseridos"
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar a venda :/"
        return {"message": error_msg}, 400


@app.get('/sales', tags=[sale_tag], responses={"200": SaleListSchema, "404": ErrorSchema})
def get_sales(query: SalesSearchSchema):
    """Faz a busca por todas as vendas cadastradas do usuário logado

    Retorna uma representação da listagem de vendas.
    """
    try:
        user_id = query.user_id
        session = Session()

        sales = session.query(Sale).filter_by(user_id=user_id).all()

        if not sales:
            return {"user_id": user_id, "sales": []}, 200
        else:
            return sales_show(sales, user_id), 200
    except Exception as e:
        print("Erro na rota /sales:", str(e))
        return {"message": "Erro interno na API"}, 500


@app.get('/sale', tags=[sale_tag],
         responses={"200": SaleViewSchema, "404": ErrorSchema})
def get_sale(query: SaleSearchSchema):
    """Faz a busca por uma venda a partir de seu ID

    Retorna uma representação das vendas.
    """
    sale_id = query.sale_id
    session = Session()
    sale = session.query(Sale).filter(Sale.id == sale_id).first()

    if not sale:
        error_msg = "venda não encontrada na base :/"
        return {"mesage": error_msg}, 404
    else:
        return sale_show(sale), 200


@app.delete('/sale', tags=[sale_tag],
            responses={"200": SaleDelSchema, "404": ErrorSchema})
def del_sale(query: SaleSearchSchema):
    """Deleta uma venda a partir de um ID informado

    Retorna uma mensagem de confirmação da remoção.
    """
    sale_id = query.sale_id

    session = Session()
    count = session.query(Sale).filter(Sale.id == sale_id).delete()
    session.commit()

    if count:
        return {"mesage": "venda removida", "id": sale_id}
    else:
        error_msg = "venda não encontrada na base :/"
        return {"mesage": error_msg}, 404


@app.post('/user', tags=[user_tag], responses={"200": UserViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_user(form: UserSchema):
    """Adiciona um novo usuário ao banco de dados ou permite o login se o usuário já existir.

    Retorna uma representação do usuário.
    """
    try:
        session = Session()

        existing_user = session.query(User).filter_by(email=form.email).first()

        if existing_user:
            return user_show(existing_user), 200
        else:
            new_user = User(
                display_name=form.display_name,
                photo_url=form.photo_url,
                email=form.email,
            )

            session.add(new_user)

            session.commit()

            return user_show(new_user), 200

    except IntegrityError as e:
        error_msg = "Erro de integridade, verifique os valores inseridos"
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar o novo usuário :/"
        return {"message": error_msg}, 400


@app.get('/user', tags=[user_tag],
         responses={"200": UserViewSchema, "404": ErrorSchema})
def get_user(query: UserSearchSchema):
    """Faz a busca por um usuário a partir de seu ID

    Retorna uma representação dos usuários.
    """
    user_id = query.user_id
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        error_msg = "Usuário não encontrada na base :/"
        return {"mesage": error_msg}, 404
    else:
        return user_show(user), 200
