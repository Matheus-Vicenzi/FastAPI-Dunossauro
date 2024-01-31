# Fast-Zero

O Projeto tem por finalidade por em prática o ciclo de vida completo de uma aplicação FastAPI

### Tecnologías
 - FastAPI -> Criação de endpoints para a comunicação HTTP e criação de documentação (Swagger)
 - Alembic -> Criação das migrations do banco de dados
 - Pytest -> Realização de testes
 - Docker -> Containerização da aplicação
 - Uvicorn -> Servidor ASGI que sustenta a aplicação
 - GitHub Actions -> Pipeline CI para validar as funcionalidades antes da integração ao repositório

### Funcionalidades
A aplicação tem por objetivo ser um gerenciado de tarefas (To do app), utilizando de autenticação (JWT)
para validar que os usuários possam gerenciar apenas suas próprias tarefas

### Variáveis de ambiente
Para o funcionamento corredo da aplicação, é necessário criar um arquivo .env e adicionar as seguintes variáveis:

 - DATABASE_URL -> Url de conexão para o banco de dados
 - SECRET_KEY -> Chave de criptografia para a autenticação JWT
 - ALGORITHM -> Algoritmo de encriptação para a autenticação JWT
 - ACCESS_TOKEN_EXPIRE_MINUTES -> Tempo para a expiração do token JWT

#### Poetry
A biblioteca Poetry está sendo utilizada como gerenciador de dependencias do projeto.

###### Instalar o poetry
```sh
curl -sSL https://install.python-poetry.org | python3 -
```

###### Entrar no ambiente virtual do poetry
```sh
poetry shell
```

###### Executar os testes
```sh
task test
```

#### Alembic
Utilize o seguinte comando para criar as tabelas no banco de dados
```sh
alembic upgrade head
```

Caso necessário criar uma nova migração para acompanhar as mudanças das models do projeto
```sh
alembic revision --autogenerate -m "mensagem da revisão"

alembic upgrade head
```

#### Docker
Para rodar a aplicação em docker, executar o comando: 
```sh
docker compose up -d
```
