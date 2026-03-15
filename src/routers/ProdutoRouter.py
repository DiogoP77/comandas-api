from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from domain.schemas.ProdutoSchemas import (
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoResponse
)

from infra.orm.ProdutoModel import ProdutoDB
from infra.database import get_db

router = APIRouter()

# LISTAR PRODUTOS
@router.get(
    "/produto/",
    response_model=List[ProdutoResponse],
    tags=["Produto"]
)
async def get_produtos(db: Session = Depends(get_db)):

    produtos = db.query(ProdutoDB).all()

    return produtos


# BUSCAR PRODUTO
@router.get(
    "/produto/{id}",
    response_model=ProdutoResponse,
    tags=["Produto"]
)
async def get_produto(id: int, db: Session = Depends(get_db)):

    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return produto


# CRIAR PRODUTO
@router.post(
    "/produto/",
    response_model=ProdutoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Produto"]
)
async def post_produto(produto_data: ProdutoCreate, db: Session = Depends(get_db)):

    novo_produto = ProdutoDB(
        nome=produto_data.nome,
        preco=produto_data.preco,
        foto=produto_data.foto
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


# ATUALIZAR PRODUTO
@router.put(
    "/produto/{id}",
    response_model=ProdutoResponse,
    tags=["Produto"]
)
async def put_produto(id: int, produto_data: ProdutoUpdate, db: Session = Depends(get_db)):

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


# DELETAR PRODUTO
@router.delete(
    "/produto/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Produto"]
)
async def delete_produto(id: int, db: Session = Depends(get_db)):

    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    db.delete(produto)
    db.commit()