# Diogo Pereira

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta

from src.domain.schemas.AuthSchemas import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    FuncionarioAuth
)

from src.infra.orm.FuncionarioModel import FuncionarioDB
from src.infra.database import get_db
from src.infra.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)
from src.infra.dependencies import get_current_active_user
from src.services.AuditoriaService import AuditoriaService

from src.infra.rate_limit import limiter
from src.settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


# ==============================
# 🔐 LOGIN
# ==============================
@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
async def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        funcionario = db.query(FuncionarioDB).filter(
            FuncionarioDB.cpf == login_data.cpf
        ).first()

        # LOGIN TEMPORÁRIO PARA TESTE
        if login_data.cpf == "admin" and login_data.senha == "123":
            access_token = create_access_token(
                data={
                    "sub": "admin",
                    "id": 1,
                    "grupo": "ADMIN"
                },
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            )

            refresh_token = create_refresh_token(
                data={
                    "sub": "admin",
                    "id": 1,
                    "grupo": "ADMIN"
                }
            )

            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type="bearer",
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                refresh_expires_in=REFRESH_TOKEN_EXPIRE_DAYS * 86400
            )

        # LOGIN NORMAL DO BANCO
        if not funcionario or not verify_password(login_data.senha, funcionario.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="CPF ou senha inválidos"
            )

        access_token = create_access_token(
            data={
                "sub": funcionario.cpf,
                "id": funcionario.id,
                "grupo": funcionario.grupo
            },
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        refresh_token = create_refresh_token(
            data={
                "sub": funcionario.cpf,
                "id": funcionario.id,
                "grupo": funcionario.grupo
            }
        )

        AuditoriaService.registrar_acao(
            db=db,
            funcionario_id=funcionario.id,
            acao="LOGIN",
            recurso="AUTH",
            request=request
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_expires_in=REFRESH_TOKEN_EXPIRE_DAYS * 86400
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no login: {str(e)}")


# ==============================
# 🔄 REFRESH TOKEN
# ==============================
@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("10/minute")
async def refresh_token(
    request: Request,
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    try:
        payload = verify_refresh_token(refresh_data.refresh_token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido"
            )

        cpf = payload.get("sub")

        funcionario = db.query(FuncionarioDB).filter(
            FuncionarioDB.cpf == cpf
        ).first()

        if not funcionario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Funcionário não encontrado"
            )

        access_token = create_access_token(
            data={
                "sub": funcionario.cpf,
                "id": funcionario.id,
                "grupo": funcionario.grupo
            },
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        new_refresh_token = create_refresh_token(
            data={
                "sub": funcionario.cpf,
                "id": funcionario.id,
                "grupo": funcionario.grupo
            }
        )

        AuditoriaService.registrar_acao(
            db=db,
            funcionario_id=funcionario.id,
            acao="REFRESH",
            recurso="AUTH",
            request=request
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            refresh_expires_in=REFRESH_TOKEN_EXPIRE_DAYS * 86400
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no refresh: {str(e)}")


# ==============================
# 👤 USUÁRIO ATUAL
# ==============================
@router.get("/me", response_model=FuncionarioAuth)
@limiter.limit("30/minute")
async def me(
    request: Request,
    current_user: FuncionarioAuth = Depends(get_current_active_user)
):
    return current_user


# ==============================
# 🚪 LOGOUT
# ==============================
@router.post("/logout")
@limiter.limit("20/minute")
async def logout(
    request: Request,
    current_user: FuncionarioAuth = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        AuditoriaService.registrar_acao(
            db=db,
            funcionario_id=current_user.id,
            acao="LOGOUT",
            recurso="AUTH",
            request=request
        )

        return {"message": "Logout realizado com sucesso"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no logout: {str(e)}")