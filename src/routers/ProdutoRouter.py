from fastapi import APIRouter, Depends, HTTPException, Request

from infra.rate_limit import limiter
from domain.schemas.ProdutoSchemas import ProdutoCreate, ProdutoUpdate, ProdutoResponse
from domain.schemas.AuthSchemas import FuncionarioAuth

from infra.orm.ProdutoModel import ProdutoDB
from infra.database import get_db
from infra.dependencies import require_group
from services.AuditoriaService import AuditoriaService

router = APIRouter()

def to_dict(obj):
    return {c.name: str(getattr(obj, c.name)) for c in obj.__table__.columns}


@router.post("/produto/", response_model=ProdutoResponse)
@limiter.limit("10/minute")
async def post_produto(produto_data: ProdutoCreate, request: Request,
                       db=Depends(get_db),
                       current_user: FuncionarioAuth = Depends(require_group([1]))):

    novo = ProdutoDB(**produto_data.model_dump())

    db.add(novo)
    db.commit()
    db.refresh(novo)

    AuditoriaService.registrar_acao(
        db=db,
        funcionario_id=current_user.id,
        acao="CREATE",
        recurso="PRODUTO",
        recurso_id=novo.id,
        dados_novos=to_dict(novo),
        request=request
    )

    return novo


@router.put("/produto/{id}", response_model=ProdutoResponse)
@limiter.limit("10/minute")
async def put_produto(id: int, produto_data: ProdutoUpdate,
                      request: Request, db=Depends(get_db),
                      current_user: FuncionarioAuth = Depends(require_group([1]))):

    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()

    if not produto:
        raise HTTPException(404, "Produto não encontrado")

    dados_antigos = to_dict(produto)

    update_data = produto_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(400, "Nenhum dado enviado")

    for k, v in update_data.items():
        setattr(produto, k, v)

    db.commit()
    db.refresh(produto)

    AuditoriaService.registrar_acao(
        db=db,
        funcionario_id=current_user.id,
        acao="UPDATE",
        recurso="PRODUTO",
        recurso_id=produto.id,
        dados_antigos=dados_antigos,
        dados_novos=to_dict(produto),
        request=request
    )

    return produto


@router.delete("/produto/{id}")
@limiter.limit("5/minute")
async def delete_produto(id: int, request: Request,
                         db=Depends(get_db),
                         current_user: FuncionarioAuth = Depends(require_group([1]))):

    produto = db.query(ProdutoDB).filter(ProdutoDB.id == id).first()

    if not produto:
        raise HTTPException(404, "Produto não encontrado")

    dados_antigos = to_dict(produto)

    AuditoriaService.registrar_acao(
        db=db,
        funcionario_id=current_user.id,
        acao="DELETE",
        recurso="PRODUTO",
        recurso_id=id,
        dados_antigos=dados_antigos,
        request=request
    )

    db.delete(produto)
    db.commit()

    return {"message": "Produto deletado"}