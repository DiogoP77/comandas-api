# Diogo Pereira

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from src.infra.rate_limit import limiter
from src.domain.schemas.ClienteSchemas import ClienteCreate, ClienteUpdate, ClienteResponse
from src.domain.schemas.AuthSchemas import FuncionarioAuth

from src.infra.orm.ClienteModel import ClienteDB
from src.infra.database import get_db
from src.infra.dependencies import require_group

router = APIRouter(
    prefix="/cliente",
    tags=["Cliente"]
)


# ==============================
# ➕ CRIAR CLIENTE
# ==============================
@router.post("/", response_model=ClienteResponse)
@limiter.limit("10/minute")
async def post_cliente(
    request: Request,
    cliente_data: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 3]))
):
    try:
        novo = ClienteDB(**cliente_data.model_dump())

        db.add(novo)
        db.commit()
        db.refresh(novo)

        return novo

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar cliente: {str(e)}")


# ==============================
# 🔎 BUSCAR CLIENTE
# ==============================
@router.get("/{id}", response_model=ClienteResponse)
@limiter.limit("20/minute")
async def get_cliente(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 3]))
):
    cliente = db.query(ClienteDB).filter(ClienteDB.id == id).first()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    return cliente


# ==============================
# 📄 LISTAR CLIENTES
# ==============================
@router.get("/", response_model=List[ClienteResponse])
@limiter.limit("20/minute")
async def list_clientes(
    request: Request,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 3]))
):
    return db.query(ClienteDB).all()


# ==============================
# ✏️ ATUALIZAR CLIENTE
# ==============================
@router.put("/{id}", response_model=ClienteResponse)
@limiter.limit("10/minute")
async def put_cliente(
    id: int,
    request: Request,
    cliente_data: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1, 3]))
):
    try:
        cliente = db.query(ClienteDB).filter(ClienteDB.id == id).first()

        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        update_data = cliente_data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado enviado")

        for k, v in update_data.items():
            setattr(cliente, k, v)

        db.commit()
        db.refresh(cliente)

        return cliente

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar cliente: {str(e)}")


# ==============================
# ❌ DELETAR CLIENTE
# ==============================
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
async def delete_cliente(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    try:
        cliente = db.query(ClienteDB).filter(ClienteDB.id == id).first()

        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")

        db.delete(cliente)
        db.commit()

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar cliente: {str(e)}")