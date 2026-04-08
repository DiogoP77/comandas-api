from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List

from infra.rate_limit import limiter, get_rate_limit
from services.AuditoriaService import AuditoriaService

from domain.schemas.FuncionarioSchemas import (
    FuncionarioCreate, FuncionarioUpdate, FuncionarioResponse
)
from domain.schemas.AuthSchemas import FuncionarioAuth

from infra.orm.FuncionarioModel import FuncionarioDB
from infra.database import get_db
from infra.security import get_password_hash
from infra.dependencies import require_group

router = APIRouter()

def to_dict(obj):
    return {c.name: str(getattr(obj, c.name)) for c in obj.__table__.columns}


@router.post("/funcionario/", response_model=FuncionarioResponse)
@limiter.limit(get_rate_limit("critical"))
async def post_funcionario(funcionario_data: FuncionarioCreate, request: Request,
                           db: Session = Depends(get_db),
                           current_user: FuncionarioAuth = Depends(require_group([1]))):

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


@router.put("/funcionario/{id}", response_model=FuncionarioResponse)
@limiter.limit(get_rate_limit("critical"))
async def put_funcionario(id: int, funcionario_data: FuncionarioUpdate,
                          request: Request, db: Session = Depends(get_db),
                          current_user: FuncionarioAuth = Depends(require_group([1]))):

    funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()

    if not funcionario:
        raise HTTPException(404, "Funcionário não encontrado")

    dados_antigos = to_dict(funcionario)

    update_data = funcionario_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(400, "Nenhum dado enviado")

    if "senha" in update_data:
        update_data["senha"] = get_password_hash(update_data["senha"])

    for k, v in update_data.items():
        setattr(funcionario, k, v)

    db.commit()
    db.refresh(funcionario)

    AuditoriaService.registrar_acao(
        db=db,
        funcionario_id=current_user.id,
        acao="UPDATE",
        recurso="FUNCIONARIO",
        recurso_id=funcionario.id,
        dados_antigos=dados_antigos,
        dados_novos=to_dict(funcionario),
        request=request
    )

    return funcionario


@router.delete("/funcionario/{id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit(get_rate_limit("critical"))
async def delete_funcionario(id: int, request: Request,
                             db: Session = Depends(get_db),
                             current_user: FuncionarioAuth = Depends(require_group([1]))):

    funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()

    if not funcionario:
        raise HTTPException(404, "Funcionário não encontrado")

    dados_antigos = to_dict(funcionario)

    db.delete(funcionario)
    db.commit()

    AuditoriaService.registrar_acao(
        db=db,
        funcionario_id=current_user.id,
        acao="DELETE",
        recurso="FUNCIONARIO",
        recurso_id=id,
        dados_antigos=dados_antigos,
        request=request
    )