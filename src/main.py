from fastapi import FastAPI
import uvicorn

from settings import HOST, PORT, RELOAD

from routers import FuncionarioRouter
from routers import ClienteRouter
from routers import ProdutoRouter

app = FastAPI(
    title="API Comandas",
    version="1.0"
)

app.include_router(FuncionarioRouter.router)
app.include_router(ClienteRouter.router)
app.include_router(ProdutoRouter.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "msg": "API Comandas funcionando",
        "docs": "http://127.0.0.1:8000/docs"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=int(PORT),
        reload=RELOAD
    )
