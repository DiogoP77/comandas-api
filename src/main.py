#Diogo Pereira da Silva
from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from settings import HOST, PORT, RELOAD

from infra.rate_limit import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from infra import database

# Routers
from routers import (
    HealthRouter,
    AuditoriaRouter,
    AuthRouter,
    FuncionarioRouter,
    ClienteRouter,
    ProdutoRouter
)


# 🔥 LIFESPAN (inicialização da API)
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 API iniciando...")

    # criação das tabelas
    database.cria_tabelas()

    yield

    print("🛑 API finalizada")


# 🔥 INSTÂNCIA DA API
app = FastAPI(
    title="API Pastelaria",
    description="API com Rate Limiting, Auditoria e Health Check",
    version="1.0.0",
    lifespan=lifespan
)


# 🔥 RATE LIMIT GLOBAL (CORRETO)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


# 🌐 ROOT
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "API Pastelaria rodando 🚀",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# 📌 REGISTRO DOS ROUTERS (CORRIGIDO)
app.include_router(AuthRouter.router, prefix="/auth", tags=["Auth"])
app.include_router(FuncionarioRouter.router, prefix="/funcionario", tags=["Funcionário"])
app.include_router(ClienteRouter.router, prefix="/cliente", tags=["Cliente"])
app.include_router(ProdutoRouter.router, prefix="/produto", tags=["Produto"])
app.include_router(AuditoriaRouter.router, prefix="/auditoria", tags=["Auditoria"])
app.include_router(HealthRouter.router, prefix="/health", tags=["Health Check"])


# 🚀 RUN
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=HOST,
        port=int(PORT),
        reload=RELOAD
    )

    # rota padrão
@app.get("/", tags=["Root"], status_code=200, summary="Informações da API - pública")
async def root():
    return {"detail":"API Comandas", "Swagger UI": "http://127.0.0.1:8000/docs", "ReDoc": "http://127.0.0.1:8000/redoc" }