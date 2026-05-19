from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List

from src.infra.rate_limit import limiter
from src.domain.schemas.ProdutoSchemas import (
    ProdutoCreate,
    ProdutoUpdate,
    ProdutoResponse
)
from src.domain.schemas.AuthSchemas import FuncionarioAuth

from src.infra.orm.ProdutoModel import ProdutoDB
from src.infra.database import get_db
from src.infra.dependencies import require_group

router = APIRouter(
    prefix="/produto",
    tags=["Produto"]
)


# ==============================
# ➕ CRIAR PRODUTO
# ==============================
@router.post("/", response_model=ProdutoResponse)
@limiter.limit("10/minute")
async def post_produto(
    request: Request,
    produto_data: ProdutoCreate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    novo = ProdutoDB(**produto_data.model_dump())

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


# ==============================
# 🔎 BUSCAR PRODUTO
# ==============================
@router.get("/{id}", response_model=ProdutoResponse)
@limiter.limit("20/minute")
async def get_produto(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return produto


# ==============================
# 📄 LISTAR PRODUTOS
# ==============================
@router.get("/", response_model=List[ProdutoResponse])
@limiter.limit("20/minute")
async def list_produtos(
    request: Request,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    return db.query(ProdutoDB).all()


# ==============================
# ✏️ ATUALIZAR PRODUTO
# ==============================
@router.put("/{id}", response_model=ProdutoResponse)
@limiter.limit("10/minute")
async def put_produto(
    id: int,
    request: Request,
    produto_data: ProdutoUpdate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    for k, v in produto_data.model_dump(exclude_unset=True).items():
        setattr(produto, k, v)

    db.commit()
    db.refresh(produto)

    return produto


# ==============================
# ❌ DELETAR PRODUTO
# ==============================
@router.delete("/{id}")
@limiter.limit("10/minute")
async def delete_produto(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()

    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(produto)
    db.commit()

    return {"message": "Produto deletado"}