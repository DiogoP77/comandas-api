from pydantic import BaseModel
from typing import Optional

class Cliente(BaseModel):

    id_cliente: Optional[int] = None
    nome: str
    cpf: str
    telefone: Optional[str] = None