from pydantic import BaseModel, ConfigDict
from typing import Optional


# 🔐 Request de login
class LoginRequest(BaseModel):
    cpf: str
    senha: str


# 🔑 Resposta com tokens
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    refresh_expires_in: int


# 🔄 Request para refresh token
class RefreshTokenRequest(BaseModel):
    refresh_token: str


# 📦 Dados internos do token
class TokenData(BaseModel):
    cpf: Optional[str] = None
    id_funcionario: Optional[int] = None


# 👤 Usuário autenticado (retornado nas rotas protegidas)
class FuncionarioAuth(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    matricula: str
    cpf: str
    grupo: int