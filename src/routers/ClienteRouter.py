from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from infra.rate_limit import limiter
from domain.schemas.ClienteSchemas import ClienteCreate, ClienteUpdate, ClienteResponse
from domain.schemas.AuthSchemas import FuncionarioAuth

from infra.orm.ClienteModel import ClienteDB
from infra.database import get_db
from infra.dependencies import require_group
from services.AuditoriaService import AuditoriaService

router = APIRouter()

def to_dict(obj):
    return {c.name: str(getattr(obj, c.name)) for c in obj.__table__.columns}


@router.post("/cliente/", response_model=ClienteResponse)
@limiter.limit("10/minute")
async def post_cliente(cliente_data: ClienteCreate, request: Request,
                       db: Session = Depends(get_db),
                       current_user: FuncionarioAuth = Depends(require_group([1, 3]))):

    novo = ClienteDB(**cliente_data.model_dump())

    db.add(novo)
    db.commit()
    db.refresh(novo)

    AuditoriaService.registrar_acao(
        db=db,
        funcionario_id=current_user.id,
        acao="CREATE",
        recurso="CLIENTE",
        recurso_id=novo.id,
        dados_novos=to_dict(novo),
        request=request
    )

    return novo


@router.put("/cliente/{id}", response_model=ClienteResponse)
@limiter.limit("10/minute")
async def put_cliente(id: int, cliente_data: ClienteUpdate,
                      request: Request, db: Session = Depends(get_db),
                      current_user: FuncionarioAuth = Depends(require_group([1, 3]))):

    cliente = db.query(ClienteDB).filter(ClienteDB.id == id).first()

    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")

    dados_antigos = to_dict(cliente)

    update_data = cliente_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(400, "Nenhum dado enviado")

    for k, v in update_data.items():
        setattr(cliente, k, v)

    db.commit()
    db.refresh(cliente)

    AuditoriaService.registrar_acao(
        db=db,
        funcionario_id=current_user.id,
        acao="UPDATE",
        recurso="CLIENTE",
        recurso_id=cliente.id,
        dados_antigos=dados_antigos,
        dados_novos=to_dict(cliente),
        request=request
    )

    return cliente


@router.delete("/cliente/{id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
async def delete_cliente(id: int, request: Request,
                         db: Session = Depends(get_db),
                         current_user: FuncionarioAuth = Depends(require_group([1]))):

    cliente = db.query(ClienteDB).filter(ClienteDB.id == id).first()

    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")

    dados_antigos = to_dict(cliente)

    db.delete(cliente)
    db.commit()

    AuditoriaService.registrar_acao(
        db=db,
        funcionario_id=current_user.id,
        acao="DELETE",
        recurso="CLIENTE",
        recurso_id=id,
        dados_antigos=dados_antigos,
        request=request
    )