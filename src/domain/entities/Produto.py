from pydantic import BaseModel
from typing import Optional


class Produto(BaseModel):

    id_produto: Optional[int] = None
    nome: str
    preco: float
    foto: Optional[bytes] = None
