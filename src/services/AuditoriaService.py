from sqlalchemy.orm import Session
from fastapi import Request
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import json

from src.infra.orm.AuditoriaModel import AuditoriaDB


class AuditoriaService:

    @staticmethod
    def registrar_acao(
        db: Session,
        funcionario_id: int,
        acao: str,
        recurso: str,
        recurso_id: Optional[int] = None,
        dados_antigos: Optional[Dict[str, Any]] = None,
        dados_novos: Optional[Dict[str, Any]] = None,
        request: Optional[Request] = None
    ) -> bool:

        try:
            ip_address = None
            user_agent = None

            # 🌐 Captura dados da requisição
            if request:
                forwarded_for = request.headers.get("X-Forwarded-For")

                if forwarded_for:
                    ip_address = forwarded_for.split(",")[0].strip()
                else:
                    ip_address = request.client.host if request.client else None

                user_agent = request.headers.get("User-Agent")

            # 🔄 Converte dict para JSON
            def to_json(data):
                if not data:
                    return None
                return json.dumps(data, default=str)

            # 🧾 Cria auditoria
            auditoria = AuditoriaDB(
                funcionario_id=funcionario_id,
                acao=acao.upper(),
                recurso=recurso.upper(),
                recurso_id=recurso_id,
                dados_antigos=to_json(dados_antigos),
                dados_novos=to_json(dados_novos),
                ip_address=ip_address,
                user_agent=user_agent,
                data_hora=datetime.now(timezone.utc)
            )

            db.add(auditoria)

            # ⚠️ flush pra garantir ID (commit fica fora)
            db.flush()

            return True

        except Exception as e:
            print(f"Erro auditoria: {e}")
            return False