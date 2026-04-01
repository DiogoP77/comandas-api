from fastapi import FastAPI
from settings import HOST, PORT, RELOAD
import uvicorn

# import das rotas
from routers import AuthRouter
from routers import FuncionarioRouter
from routers import ClienteRouter
from routers import ProdutoRouter

# banco de dados
from infra import database

# ciclo de vida da aplicação
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):

    # STARTUP
    print("API has started")

    # cria as tabelas se não existirem
    await database.cria_tabelas()

    yield

    # SHUTDOWN
    print("API is shutting down")


# cria aplicação
app = FastAPI(lifespan=lifespan)


# rota raiz
@app.get("/", tags=["Root"], status_code=200)
async def root():
    return {
        "detail": "API Pastelaria",
        "Swagger UI": "http://127.0.0.1:8000/docs",
        "ReDoc": "http://127.0.0.1:8000/redoc"
    }


# incluir routers
app.include_router(AuthRouter.router)
app.include_router(FuncionarioRouter.router)
app.include_router(ClienteRouter.router)
app.include_router(ProdutoRouter.router)


# executar servidor
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=int(PORT),
        reload=RELOAD
    )
    #Diogo Pereira