from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List

from src.infra.rate_limit import limiter, get_rate_limit
from src.services.AuditoriaService import AuditoriaService

from src.domain.schemas.FuncionarioSchemas import (
    FuncionarioCreate,
    FuncionarioUpdate,
    FuncionarioResponse
)
from src.domain.schemas.AuthSchemas import FuncionarioAuth

from src.infra.orm.FuncionarioModel import FuncionarioDB
from src.infra.database import get_db
from src.infra.security import get_password_hash
from src.infra.dependencies import require_group

router = APIRouter(
    prefix="/funcionario",
    tags=["Funcionário"]
)


def to_dict(obj):
    return {c.name: str(getattr(obj, c.name)) for c in obj.__table__.columns}


# ==============================
# ➕ CRIAR FUNCIONÁRIO
# ==============================
@router.post("/", response_model=FuncionarioResponse)
@limiter.limit(get_rate_limit("critical"))
async def post_funcionario(
    request: Request,
    funcionario_data: FuncionarioCreate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    novo = FuncionarioDB(
        nome=funcionario_data.nome,
        matricula=funcionario_data.matricula,
        cpf=funcionario_data.cpf,
        telefone=funcionario_data.telefone,
        grupo=funcionario_data.grupo,
        senha=get_password_hash(funcionario_data.senha)
    )

    db.add(novo)
    db.commit()
    db.refresh(novo)

    AuditoriaService.registrar_acao(
        db=db,
        funcionario_id=current_user.id,
        acao="CREATE",
        recurso="FUNCIONARIO",
        recurso_id=novo.id,
        dados_novos=to_dict(novo),
        request=request
    )

    return novo


# ==============================
# 🔎 BUSCAR POR ID
# ==============================
@router.get("/{id}", response_model=FuncionarioResponse)
@limiter.limit(get_rate_limit("default"))
async def get_funcionario(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()

    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    return funcionario


# ==============================
# 📄 LISTAR
# ==============================
@router.get("/", response_model=List[FuncionarioResponse])
@limiter.limit(get_rate_limit("default"))
async def list_funcionarios(
    request: Request,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    return db.query(FuncionarioDB).offset(skip).limit(limit).all()


# ==============================
# ✏️ ATUALIZAR
# ==============================
@router.put("/{id}", response_model=FuncionarioResponse)
@limiter.limit(get_rate_limit("critical"))
async def put_funcionario(
    id: int,
    request: Request,
    funcionario_data: FuncionarioUpdate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()

    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    update_data = funcionario_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado enviado")

    if "senha" in update_data:
        update_data["senha"] = get_password_hash(update_data["senha"])

    for k, v in update_data.items():
        setattr(funcionario, k, v)

    db.commit()
    db.refresh(funcionario)

    return funcionario


# ==============================
# ❌ DELETAR
# ==============================
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(get_rate_limit("critical"))
async def delete_funcionario(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()

    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    db.delete(funcionario)
    db.commit()