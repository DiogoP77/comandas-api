# Diogo Pereira

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

from src.domain.schemas.AuditoriaSchemas import AuditoriaResponse, FuncionarioSimple
from src.domain.schemas.AuthSchemas import FuncionarioAuth
from src.infra.orm.AuditoriaModel import AuditoriaDB
from src.infra.orm.FuncionarioModel import FuncionarioDB
from src.infra.database import get_db
from src.infra.dependencies import require_group
from src.infra.rate_limit import limiter, get_rate_limit


router = APIRouter(
    prefix="/auditoria",
    tags=["Auditoria"]
)


# ==============================
# 🔎 LISTAR AUDITORIA
# ==============================
@router.get("/")
@limiter.limit(get_rate_limit("moderate"))
async def listar_auditoria(
    request: Request,
    funcionario_id: Optional[int] = Query(None),
    acao: Optional[str] = Query(None),
    recurso: Optional[str] = Query(None),
    data_inicio: Optional[str] = Query(None),
    data_fim: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limite: int = Query(100, ge=1),
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    try:
        query = db.query(AuditoriaDB, FuncionarioDB).join(
            FuncionarioDB,
            FuncionarioDB.id == AuditoriaDB.funcionario_id
        )

        if funcionario_id:
            query = query.filter(AuditoriaDB.funcionario_id == funcionario_id)

        if acao:
            query = query.filter(AuditoriaDB.acao.in_(acao.split(",")))

        if recurso:
            query = query.filter(AuditoriaDB.recurso.in_(recurso.split(",")))

        if data_inicio:
            try:
                data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d")
                query = query.filter(AuditoriaDB.data_hora >= data_inicio_dt)
            except ValueError:
                raise HTTPException(400, "Formato de data_inicio inválido. Use YYYY-MM-DD")

        if data_fim:
            try:
                data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d")
                query = query.filter(AuditoriaDB.data_hora <= data_fim_dt)
            except ValueError:
                raise HTTPException(400, "Formato de data_fim inválido. Use YYYY-MM-DD")

        registros = (
            query
            .order_by(desc(AuditoriaDB.data_hora))
            .offset(skip)
            .limit(limite)
            .all()
        )

        return [
            AuditoriaResponse(
                id=a.id,
                funcionario_id=a.funcionario_id,
                funcionario=FuncionarioSimple(
                    id=f.id,
                    nome=f.nome,
                    matricula=f.matricula,
                    grupo=f.grupo
                ),
                acao=a.acao,
                recurso=a.recurso,
                recurso_id=a.recurso_id,
                dados_antigos=a.dados_antigos,
                dados_novos=a.dados_novos,
                ip_address=a.ip_address,
                user_agent=a.user_agent,
                data_hora=a.data_hora
            )
            for a, f in registros
        ]

    except Exception as e:
        raise HTTPException(500, f"Erro ao buscar auditoria: {str(e)}")


# ==============================
# 📊 LISTAR AÇÕES E RECURSOS
# ==============================
@router.get("/acoes")
@limiter.limit(get_rate_limit("default"))
async def listar_acoes(
    request: Request,   # 🔥 AQUI ESTAVA O PROBLEMA
    db: Session = Depends(get_db),
    current_user: FuncionarioAuth = Depends(require_group([1]))
):
    try:
        acoes = db.query(AuditoriaDB.acao).distinct().all()
        recursos = db.query(AuditoriaDB.recurso).distinct().all()

        return {
            "acoes": [a[0] for a in acoes],
            "recursos": [r[0] for r in recursos]
        }

    except Exception as e:
        raise HTTPException(500, f"Erro ao buscar ações: {str(e)}")