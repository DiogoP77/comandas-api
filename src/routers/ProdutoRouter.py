from fastapi import APIRouter
from domain.entities.Produto import Produto

router = APIRouter(
    prefix="/produto",
    tags=["Produto"]
)


@router.get("/")
def get_produtos():
    return {"msg": "listar produtos"}


@router.post("/")
def criar_produto(produto: Produto):
    return {"msg": "produto criado", "produto": produto}
