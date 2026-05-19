# Diogo Pereira

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

# 🔥 IMPORT CORRETO
from src.settings import STR_DATABASE, ASYNC_STR_DATABASE


# ==============================
# 🔥 ENGINES
# ==============================

# Engine síncrono (compatibilidade)
engine = create_engine(
    STR_DATABASE,
    echo=True,
    future=True
)

# Engine assíncrono (principal - COMANDA usa esse)
async_engine = create_async_engine(
    ASYNC_STR_DATABASE,
    echo=True,
    future=True
)


# ==============================
# 🔥 SESSÕES
# ==============================

# Sessão síncrona
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

# Sessão assíncrona
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# ==============================
# 🔥 BASE DOS MODELS
# ==============================

Base = declarative_base()


# ==============================
# 🔥 IMPORTAR MODELS (OBRIGATÓRIO)
# ==============================
# ⚠️ Isso garante que o SQLAlchemy "enxergue" as tabelas

from src.infra.orm import (  # noqa: E402
    ClienteModel,
    FuncionarioModel,
    ProdutoModel,
    ComandaModel,
    AuditoriaModel
)


# ==============================
# 🔥 CRIAÇÃO DE TABELAS
# ==============================

def cria_tabelas():
    """
    Cria tabelas no modo síncrono
    👉 Use no startup sem await
    """
    Base.metadata.create_all(bind=engine)


async def cria_tabelas_async():
    """
    Cria tabelas no modo assíncrono
    👉 Opcional (caso queira async)
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ==============================
# 🔥 DEPENDÊNCIAS
# ==============================

# 🔹 Síncrono
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 Assíncrono
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session