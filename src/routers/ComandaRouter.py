# Diogo Pereira

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional
from datetime import datetime

from src.domain.schemas.ComandaSchemas import (
    ComandaCreate,
    ComandaResponse,
    FuncionarioResponse,
    ClienteResponse,
    ComandaProdutosCreate,
    ComandaProdutosResponse
)

from src.domain.schemas.AuthSchemas import FuncionarioAuth

from src.infra.orm.ComandaModel import ComandaDB, ComandaProdutoDB
from src.infra.orm.FuncionarioModel import FuncionarioDB
from src.infra.orm.ClienteModel import ClienteDB

from src.infra.database import get_async_db
from src.infra.dependencies import require_group, get_current_active_user
from src.infra.rate_limit import limiter


router = APIRouter(
    prefix="/comanda",
    tags=["Comanda"]
)


# ==============================
# 🔎 GET COMANDA POR ID
# ==============================
@router.get("/{id}", response_model=ComandaResponse)
@limiter.limit("20/minute")
async def get_comanda(
    id: int,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user)
):
    try:
        result = await db.execute(
            select(ComandaDB, FuncionarioDB, ClienteDB)
            .outerjoin(FuncionarioDB, FuncionarioDB.id == ComandaDB.funcionario_id)
            .outerjoin(ClienteDB, ClienteDB.id == ComandaDB.cliente_id)
            .where(ComandaDB.id == id)
        )

        row = result.first()

        if not row:
            raise HTTPException(status_code=404, detail="Comanda não encontrada")

        comanda, funcionario, cliente = row

        return ComandaResponse(
            id=comanda.id,
            comanda=comanda.comanda,
            data_hora=comanda.data_hora,
            status=comanda.status,
            cliente_id=comanda.cliente_id,
            funcionario_id=comanda.funcionario_id,
            funcionario=FuncionarioResponse.model_validate(funcionario) if funcionario else None,
            cliente=ClienteResponse.model_validate(cliente) if cliente else None
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# 📄 LISTAR COMANDAS
# ==============================
@router.get("/", response_model=List[ComandaResponse])
@limiter.limit("20/minute")
async def list_comandas(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    status_filter: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_async_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user)
):
    try:
        query = (
            select(ComandaDB, FuncionarioDB, ClienteDB)
            .outerjoin(FuncionarioDB, FuncionarioDB.id == ComandaDB.funcionario_id)
            .outerjoin(ClienteDB, ClienteDB.id == ComandaDB.cliente_id)
        )

        if status_filter is not None:
            query = query.where(ComandaDB.status == status_filter)

        result = await db.execute(query.offset(skip).limit(limit))
        rows = result.all()

        return [
            ComandaResponse(
                id=comanda.id,
                comanda=comanda.comanda,
                data_hora=comanda.data_hora,
                status=comanda.status,
                cliente_id=comanda.cliente_id,
                funcionario_id=comanda.funcionario_id,
                funcionario=FuncionarioResponse.model_validate(funcionario) if funcionario else None,
                cliente=ClienteResponse.model_validate(cliente) if cliente else None
            )
            for comanda, funcionario, cliente in rows
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# ➕ CRIAR COMANDA
# ==============================
@router.post("/", response_model=ComandaResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_comanda(
    comanda_data: ComandaCreate,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user)
):
    try:
        nova = ComandaDB(
            comanda=comanda_data.comanda,
            data_hora=datetime.utcnow(),
            status=0,
            cliente_id=comanda_data.cliente_id,
            funcionario_id=comanda_data.funcionario_id
        )

        db.add(nova)
        await db.commit()
        await db.refresh(nova)

        return ComandaResponse.model_validate(nova)

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# ✏️ ATUALIZAR COMANDA
# ==============================
@router.put("/{id}", response_model=ComandaResponse)
@limiter.limit("10/minute")
async def update_comanda(
    id: int,
    comanda_data: ComandaCreate,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user)
):
    try:
        result = await db.execute(
            select(ComandaDB).where(ComandaDB.id == id)
        )

        comanda = result.scalar_one_or_none()

        if not comanda:
            raise HTTPException(status_code=404, detail="Comanda não encontrada")

        comanda.comanda = comanda_data.comanda
        comanda.cliente_id = comanda_data.cliente_id
        comanda.funcionario_id = comanda_data.funcionario_id

        await db.commit()
        await db.refresh(comanda)

        return ComandaResponse.model_validate(comanda)

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# ❌ DELETAR COMANDA
# ==============================
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
async def delete_comanda(
    id: int,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    try:
        result = await db.execute(
            select(ComandaDB).where(ComandaDB.id == id)
        )

        comanda = result.scalar_one_or_none()

        if not comanda:
            raise HTTPException(status_code=404, detail="Comanda não encontrada")

        await db.delete(comanda)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# ➕ ADICIONAR PRODUTO
# ==============================
@router.post("/{comanda_id}/produto", response_model=ComandaProdutosResponse)
@limiter.limit("10/minute")
async def add_produto(
    comanda_id: int,
    produto_data: ComandaProdutosCreate,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user)
):
    try:
        item = ComandaProdutoDB(
            comanda_id=comanda_id,
            produto_id=produto_data.produto_id,
            funcionario_id=produto_data.funcionario_id,
            quantidade=produto_data.quantidade,
            valor_unitario=produto_data.valor_unitario
        )

        db.add(item)
        await db.commit()
        await db.refresh(item)

        return ComandaProdutosResponse.model_validate(item)

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ==============================
# ❌ REMOVER PRODUTO
# ==============================
@router.delete("/{comanda_id}/produto/{produto_id}")
@limiter.limit("10/minute")
async def delete_produto_comanda(
    comanda_id: int,
    produto_id: int,
    request: Request,
    db: AsyncSession = Depends(get_async_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user)
):
    try:
        result = await db.execute(
            select(ComandaProdutoDB).where(
                and_(
                    ComandaProdutoDB.comanda_id == comanda_id,
                    ComandaProdutoDB.produto_id == produto_id
                )
            )
        )

        item = result.scalar_one_or_none()

        if not item:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado na comanda"
            )

        await db.delete(item)
        await db.commit()

        return {"message": "Produto removido com sucesso"}

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))