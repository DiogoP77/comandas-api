from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from src.domain.schemas.FuncionarioSchemas import FuncionarioResponse
from src.domain.schemas.ClienteSchemas import ClienteResponse
from src.domain.schemas.ProdutoSchemas import ProdutoResponse


# ==============================
# 🔥 COMANDA
# ==============================

class ComandaCreate(BaseModel):
    comanda: str
    status: Optional[int] = 0
    cliente_id: Optional[int] = None
    funcionario_id: int


class ComandaUpdate(BaseModel):
    comanda: Optional[str] = None
    status: Optional[int] = None
    cliente_id: Optional[int] = None
    funcionario_id: Optional[int] = None


class ComandaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    comanda: str
    data_hora: datetime
    status: int

    funcionario_id: int
    funcionario: Optional[FuncionarioResponse] = None

    cliente_id: Optional[int] = None
    cliente: Optional[ClienteResponse] = None


# ==============================
# 🔥 COMANDA PRODUTOS
# ==============================

class ComandaProdutosCreate(BaseModel):
    produto_id: int
    funcionario_id: int
    quantidade: int
    valor_unitario: float


class ComandaProdutosUpdate(BaseModel):
    quantidade: Optional[int] = None
    valor_unitario: Optional[float] = None


class ComandaProdutosResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    comanda_id: int

    produto_id: int
    produto: Optional[ProdutoResponse] = None

    funcionario_id: int
    funcionario: Optional[FuncionarioResponse] = None

    quantidade: int
    valor_unitario: float