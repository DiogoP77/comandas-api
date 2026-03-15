from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from domain.schemas.FuncionarioSchemas import (
    FuncionarioCreate,
    FuncionarioUpdate,
    FuncionarioResponse
)

from infra.orm.FuncionarioModel import FuncionarioDB
from infra.database import get_db

router = APIRouter()

# LISTAR FUNCIONARIOS
@router.get(
    "/funcionario/",
    response_model=List[FuncionarioResponse],
    tags=["Funcionário"]
)
async def get_funcionarios(db: Session = Depends(get_db)):
    try:
        funcionarios = db.query(FuncionarioDB).all()
        return funcionarios
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar funcionários: {str(e)}"
        )


# BUSCAR POR ID
@router.get(
    "/funcionario/{id}",
    response_model=FuncionarioResponse,
    tags=["Funcionário"]
)
async def get_funcionario(id: int, db: Session = Depends(get_db)):

    funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()

    if not funcionario:
        raise HTTPException(
            status_code=404,
            detail="Funcionário não encontrado"
        )

    return funcionario


# CRIAR FUNCIONARIO
@router.post(
    "/funcionario/",
    response_model=FuncionarioResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Funcionário"]
)
async def post_funcionario(funcionario_data: FuncionarioCreate, db: Session = Depends(get_db)):

    existing_funcionario = db.query(FuncionarioDB).filter(
        FuncionarioDB.cpf == funcionario_data.cpf
    ).first()

    if existing_funcionario:
        raise HTTPException(
            status_code=400,
            detail="Já existe um funcionário com este CPF"
        )

    novo_funcionario = FuncionarioDB(
        nome=funcionario_data.nome,
        matricula=funcionario_data.matricula,
        cpf=funcionario_data.cpf,
        telefone=funcionario_data.telefone,
        grupo=funcionario_data.grupo,
        senha=funcionario_data.senha
    )

    db.add(novo_funcionario)
    db.commit()
    db.refresh(novo_funcionario)

    return novo_funcionario


# ATUALIZAR FUNCIONARIO
@router.put(
    "/funcionario/{id}",
    response_model=FuncionarioResponse,
    tags=["Funcionário"]
)
async def put_funcionario(id: int, funcionario_data: FuncionarioUpdate, db: Session = Depends(get_db)):

    funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()

    if not funcionario:
        raise HTTPException(
            status_code=404,
            detail="Funcionário não encontrado"
        )

    existing_funcionario = None

    if funcionario_data.cpf and funcionario_data.cpf != funcionario.cpf:
        existing_funcionario = db.query(FuncionarioDB).filter(
            FuncionarioDB.cpf == funcionario_data.cpf
        ).first()

    if existing_funcionario:
        raise HTTPException(
            status_code=400,
            detail="Já existe um funcionário com este CPF"
        )

    update_data = funcionario_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(funcionario, field, value)

    db.commit()
    db.refresh(funcionario)

    return funcionario


# DELETAR FUNCIONARIO
@router.delete(
    "/funcionario/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Funcionário"]
)
async def delete_funcionario(id: int, db: Session = Depends(get_db)):

    funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()

    if not funcionario:
        raise HTTPException(
            status_code=404,
            detail="Funcionário não encontrado"
        )

    db.delete(funcionario)
    db.commit()
