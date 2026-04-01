from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from domain.schemas.ProdutoSchemas import (
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoResponse
)
from domain.schemas.AuthSchemas import FuncionarioAuth

from infra.orm.ProdutoModel import ProdutoDB
from infra.database import get_db
from infra.dependencies import get_current_active_user, require_group

router = APIRouter()


# 🌍 LISTAR PRODUTOS (PÚBLICO - SEM PREÇO)
@router.get(
    "/produto/publico",
    tags=["Produto"],
    summary="Listar produtos público (sem preço)"
)
async def get_produtos_publico(db: Session = Depends(get_db)):
    try:
        produtos = db.query(ProdutoDB).all()

        # Remove preço da resposta
        return [
            {
                "id": p.id,
                "nome": p.nome,
                "foto": p.foto
            }
            for p in produtos
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar produtos públicos: {str(e)}"
        )


# 🔐 LISTAR PRODUTOS COMPLETO (PROTEGIDO)
@router.get(
    "/produto/",
    response_model=List[ProdutoResponse],
    tags=["Produto"],
    status_code=status.HTTP_200_OK,
    summary="Listar produtos completo"
)
async def get_produtos(
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user)
):
    try:
        return db.query(ProdutoDB).all()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar produtos: {str(e)}"
        )


# 🔐 BUSCAR PRODUTO POR ID (PROTEGIDO)
@router.get(
    "/produto/{id}",
    response_model=ProdutoResponse,
    tags=["Produto"],
    status_code=status.HTTP_200_OK,
    summary="Buscar produto por ID"
)
async def get_produto(
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(get_current_active_user)
):
    try:
        produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()

        if not produto:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        return produto

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar produto: {str(e)}"
        )


# ➕ CRIAR PRODUTO (GRUPO 1)
@router.post(
    "/produto/",
    response_model=ProdutoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Produto"],
    summary="Criar produto"
)
async def post_produto(
    produto_data: ProdutoCreate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    try:
        novo_produto = ProdutoDB(
            nome=produto_data.nome,
            preco=produto_data.preco,
            foto=produto_data.foto
        )

        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)

        return novo_produto

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar produto: {str(e)}"
        )


# ✏️ ATUALIZAR PRODUTO (GRUPO 1)
@router.put(
    "/produto/{id}",
    response_model=ProdutoResponse,
    tags=["Produto"],
    status_code=status.HTTP_200_OK,
    summary="Atualizar produto"
)
async def put_produto(
    id: int,
    produto_data: ProdutoUpdate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    try:
        produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()

        if not produto:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        update_data = produto_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(produto, field, value)

        db.commit()
        db.refresh(produto)

        return produto

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar produto: {str(e)}"
        )


# ❌ DELETAR PRODUTO (GRUPO 1)
@router.delete(
    "/produto/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Produto"],
    summary="Deletar produto"
)
async def delete_produto(
    id: int,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    try:
        produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()

        if not produto:
            raise HTTPException(
                status_code=404,
                detail="Produto não encontrado"
            )

        db.delete(produto)
        db.commit()

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar produto: {str(e)}"
        )
    @router.get(
    "/produto/publico",
    response_model=List[ProdutoResponse],
    tags=["Produto Público"]
)
    async def get_produtos_publicos(db: Session = Depends(get_db)):
        produtos = db.query(ProdutoDB).all()
        return produtos