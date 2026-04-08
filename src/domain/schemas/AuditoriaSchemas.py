from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# 🔹 FUNCIONÁRIO SIMPLIFICADO (NECESSÁRIO)
class FuncionarioSimple(BaseModel):
    id: int
    nome: str
    matricula: str
    grupo: int

    class Config:
        from_attributes = True


# 🔹 RESPOSTA DA AUDITORIA
class AuditoriaResponse(BaseModel):
    id: int
    funcionario_id: int
    funcionario: Optional[FuncionarioSimple]  # 🔥 ADICIONADO
    acao: str
    recurso: str
    recurso_id: Optional[int]
    dados_antigos: Optional[str]
    dados_novos: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    data_hora: datetime

    class Config:
        from_attributes = True