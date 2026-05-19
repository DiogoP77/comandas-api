# Diogo

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import uvicorn

# 🔹 CONFIG
from src.settings import CORS_ORIGINS

# 🔹 DATABASE
from src.infra.database import cria_tabelas

# 🔹 ROUTERS
from src.routers.AuthRouter import router as auth_router
from src.routers.ClienteRouter import router as cliente_router
from src.routers.FuncionarioRouter import router as funcionario_router
from src.routers.ProdutoRouter import router as produto_router
from src.routers.ComandaRouter import router as comanda_router
from src.routers.AuditoriaRouter import router as auditoria_router
from src.routers.HealthRouter import router as health_router


# ==============================
# 🔥 LIFESPAN
# ==============================
@asynccontextmanager
async def lifespan(app: FastAPI):
    cria_tabelas()
    yield


# ==============================
# 🔥 APP
# ==============================
app = FastAPI(
    title="Comandas API",
    version="1.0.0",
    description="API para gerenciamento de comandas",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Auth", "description": "Autenticação"},
        {"name": "Funcionário", "description": "Gerenciamento de funcionários"},
        {"name": "Cliente", "description": "Gerenciamento de clientes"},
        {"name": "Produto", "description": "Gerenciamento de produtos"},
        {"name": "Comanda", "description": "Gerenciamento de comandas"},
        {"name": "Auditoria", "description": "Logs do sistema"},
        {"name": "Health", "description": "Monitoramento da API"},
    ]
)


# ==============================
# 🔥 CORS
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# 🔥 ROTAS
# ==============================
app.include_router(auth_router, tags=["Auth"])

app.include_router(funcionario_router, prefix="/funcionario", tags=["Funcionário"])
app.include_router(cliente_router, prefix="/cliente", tags=["Cliente"])
app.include_router(produto_router, prefix="/produto", tags=["Produto"])
app.include_router(comanda_router, prefix="/comanda", tags=["Comanda"])
app.include_router(auditoria_router, prefix="/auditoria", tags=["Auditoria"])
app.include_router(health_router, tags=["Health"])


# ==============================
# 🔥 ROOT
# ==============================
@app.get("/", tags=["Root"])
async def root():
    return {
        "detail": "API Comandas",
        "docs": "http://127.0.0.1:8000/docs",
        "redoc": "http://127.0.0.1:8000/redoc"
    }


# ==============================
# 🚀 RUN SERVER
# ==============================
if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True

    )
    #DIogo Pereira 
    #python -m src.main código para rodar
    #https://localhost:8000