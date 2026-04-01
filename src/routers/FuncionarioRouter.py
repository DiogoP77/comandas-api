from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from domain.schemas.FuncionarioSchemas import (
    FuncionarioCreate,
    FuncionarioUpdate,
    FuncionarioResponse
)
from domain.schemas.AuthSchemas import FuncionarioAuth

from infra.orm.FuncionarioModel import FuncionarioDB
from infra.database import get_db
from infra.security import get_password_hash
from infra.dependencies import get_current_active_user, require_group

router = APIRouter()


# 🔎 LISTAR FUNCIONÁRIOS (ADMIN)
@router.get(
    "/funcionario/",
    response_model=List[FuncionarioResponse],
    status_code=status.HTTP_200_OK,
    tags=["Funcionário"],
    summary="Listar todos os funcionários"
)
async def get_funcionarios(
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    try:
        return db.query(FuncionarioDB).all()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar funcionários: {str(e)}"
        )


# 🔎 BUSCAR POR ID (AUTENTICADO)
@router.get(
    "/funcionario/{id}",
    response_model=FuncionarioResponse,
    status_code=status.HTTP_200_OK,
    tags=["Funcionário"],
    summary="Buscar funcionário por ID"
)
async def get_funcionario(
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user)
):
    try:
        funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()

        if not funcionario:
            raise HTTPException(
                status_code=404,
                detail="Funcionário não encontrado"
            )

        return funcionario

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar funcionário: {str(e)}"
        )


# ➕ CRIAR FUNCIONÁRIO (ADMIN)
@router.post(
    "/funcionario/",
    response_model=FuncionarioResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Funcionário"],
    summary="Criar novo funcionário"
)
async def post_funcionario(
    funcionario_data: FuncionarioCreate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    try:
        # Verifica CPF duplicado
        existing_funcionario = db.query(FuncionarioDB).filter(
            FuncionarioDB.cpf == funcionario_data.cpf
        ).first()

        if existing_funcionario:
            raise HTTPException(
                status_code=400,
                detail="Já existe um funcionário com este CPF"
            )

        # Hash da senha
        hashed_password = get_password_hash(funcionario_data.senha)

        novo_funcionario = FuncionarioDB(
            nome=funcionario_data.nome,
            matricula=funcionario_data.matricula,
            cpf=funcionario_data.cpf,
            telefone=funcionario_data.telefone,
            grupo=funcionario_data.grupo,
            senha=hashed_password
        )

        db.add(novo_funcionario)
        db.commit()
        db.refresh(novo_funcionario)

        return novo_funcionario

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar funcionário: {str(e)}"
        )


# ✏️ ATUALIZAR FUNCIONÁRIO (ADMIN)
@router.put(
    "/funcionario/{id}",
    response_model=FuncionarioResponse,
    status_code=status.HTTP_200_OK,
    tags=["Funcionário"],
    summary="Atualizar funcionário"
)
async def put_funcionario(
    id: int,
    funcionario_data: FuncionarioUpdate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    try:
        funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()

        if not funcionario:
            raise HTTPException(
                status_code=404,
                detail="Funcionário não encontrado"
            )

        # Verifica CPF duplicado
        if funcionario_data.cpf and funcionario_data.cpf != funcionario.cpf:
            existing = db.query(FuncionarioDB).filter(
                FuncionarioDB.cpf == funcionario_data.cpf
            ).first()

            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="Já existe um funcionário com este CPF"
                )

        update_data = funcionario_data.model_dump(exclude_unset=True)

        # Hash se atualizar senha
        if "senha" in update_data:
            update_data["senha"] = get_password_hash(update_data["senha"])

        for field, value in update_data.items():
            setattr(funcionario, field, value)

        db.commit()
        db.refresh(funcionario)

        return funcionario

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar funcionário: {str(e)}"
        )


# ❌ DELETAR FUNCIONÁRIO (ADMIN)
@router.delete(
    "/funcionario/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Funcionário"],
    summary="Remover funcionário"
)
async def delete_funcionario(
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    try:
        funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == id).first()

        if not funcionario:
            raise HTTPException(
                status_code=404,
                detail="Funcionário não encontrado"
            )

        # Evita deletar a si mesmo
        if current_user.id == id:
            raise HTTPException(
                status_code=400,
                detail="Não é possível excluir seu próprio usuário"
            )

        db.delete(funcionario)
        db.commit()

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar funcionário: {str(e)}"
        )