# Como executar em ambiente local

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

> OBS: para iniciar o ambiente virtual em máquina windows, digite o comando .\env\Scripts\Activate
> OBS: para encerrar o ambiente virtual em máquina windows, digite o comando .\env\Scripts\Deactivate

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 4500
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte.

```
(env)$ flask run --host 0.0.0.0 --port 4500 --reload
```

Abra o [http://localhost:4500/#/](http://localhost:4500/#/) no navegador para verificar o status da API em execução.

# Como executar com Docker

Para iniciar utilizando Docker digite os comandos abaixo:

```shell
docker build -t backend .
```

E então digite:

```shell
docker run -p 4500:4500 backend
```

Observe que em ambos os códigos o nome da imagem deve ser "backend".

> OBS: a porta para execução do backend precisa ser 4500, pois o frontend está fixo nessa porta.
