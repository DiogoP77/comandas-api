from pydantic import BaseModel
from typing import Optional


class Funcionario(BaseModel):

    id_funcionario: Optional[int] = None
    nome: str
    matricula: str
    cpf: str
    telefone: Optional[str] = None
    grupo: int
    senha: Optional[str] = None
