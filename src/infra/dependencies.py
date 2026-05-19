from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.infra.database import get_db
from src.infra.orm.FuncionarioModel import FuncionarioDB
from src.infra.security import verify_access_token

from src.domain.schemas.AuthSchemas import FuncionarioAuth


# 🔐 Scheme para extrair token
security = HTTPBearer(auto_error=True)


# 🔑 PEGA USUÁRIO PELO TOKEN
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> FuncionarioAuth:

    # 🔒 Valida token
    try:
        payload = verify_access_token(credentials.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    cpf: str = payload.get("sub")
    id_funcionario: int = payload.get("id")

    # ❌ Token inválido
    if not cpf or not id_funcionario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido - dados incompletos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 🔎 Busca no banco
    funcionario = db.query(FuncionarioDB).filter(
        FuncionarioDB.id == id_funcionario
    ).first()

    if not funcionario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Funcionário não encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # ❌ CPF não bate
    if funcionario.cpf != cpf:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido - CPF não corresponde",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # ✅ Retorna usuário
    return FuncionarioAuth(
        id=funcionario.id,
        nome=funcionario.nome,
        matricula=funcionario.matricula,
        cpf=funcionario.cpf,
        grupo=funcionario.grupo
    )


# 👤 USUÁRIO AUTENTICADO
def get_current_active_user(
    current_user: FuncionarioAuth = Depends(get_current_user)
) -> FuncionarioAuth:
    return current_user


# 🔒 CONTROLE DE GRUPO
def require_group(group_required: list[int] | None = None):

    def check_group(
        current_user: FuncionarioAuth = Depends(get_current_active_user)
    ) -> FuncionarioAuth:

        # ✅ Qualquer autenticado
        if group_required is None:
            return current_user

        # ❌ Sem permissão
        if current_user.grupo not in group_required:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permissão insuficiente"
            )

        return current_user

    return check_group