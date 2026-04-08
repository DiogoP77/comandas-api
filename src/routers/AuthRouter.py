from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta

from domain.schemas.AuthSchemas import (
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    FuncionarioAuth
)

from infra.orm.FuncionarioModel import FuncionarioDB
from infra.database import get_db
from infra.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token
)
from infra.dependencies import get_current_active_user
from services.AuditoriaService import AuditoriaService

from infra.rate_limit import limiter  # ✅ ADICIONADO

from settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

router = APIRouter()


# 🔐 LOGIN
@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")  # ✅ RATE LIMIT
async def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
        funcionario = db.query(FuncionarioDB).filter(
            FuncionarioDB.cpf == login_data.cpf
        ).first()

        if not funcionario or not verify_password(login_data.senha, funcionario.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="CPF ou senha inválidos",
                headers={"WWW-Authenticate": "Bearer"},
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

        # 🔥 AUDITORIA LOGIN
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
            refresh_expires_in=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Erro ao realizar login: {str(e)}")


# 🔄 REFRESH TOKEN
@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("10/minute")  # ✅ RATE LIMIT
async def refresh_token(
    request: Request,
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    try:
        payload = verify_refresh_token(refresh_data.refresh_token)

        cpf = payload.get("sub")

        funcionario = db.query(FuncionarioDB).filter(
            FuncionarioDB.cpf == cpf
        ).first()

        if not funcionario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Funcionário não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
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

        # 🔥 AUDITORIA REFRESH
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
            refresh_expires_in=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Erro ao renovar token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


# 👤 USUÁRIO ATUAL
@router.get("/me", response_model=FuncionarioAuth)
@limiter.limit("30/minute")  # ✅ RATE LIMIT
async def get_current_user_info(
    request: Request,
    current_user: FuncionarioAuth = Depends(get_current_active_user)
):
    return current_user


# 🚪 LOGOUT
@router.post("/logout")
@limiter.limit("20/minute")  # ✅ RATE LIMIT
async def logout(
    request: Request,
    current_user: FuncionarioAuth = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    AuditoriaService.registrar_acao(
        db=db,
        funcionario_id=current_user.id,
        acao="LOGOUT",
        recurso="AUTH",
        request=request
    )

    return {"message": "Logout realizado com sucesso"}