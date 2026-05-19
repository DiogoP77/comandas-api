from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import re


class IPAccessMiddleware(BaseHTTPMiddleware):
    """
    Middleware para bloquear acesso externo baseado em CORS_ORIGINS.

    Extrai IPs e domínios permitidos da configuração CORS_ORIGINS e bloqueia
    qualquer requisição de IP/domínio não autorizado.
    """

    def __init__(self, app, allowed_origins):
        super().__init__(app)

        self.allowed_hosts = []
        self.allow_all = False

        # 🔎 Processa origens permitidas
        for origin in allowed_origins:
            if not origin or origin.strip() == "":
                continue

            origin = origin.strip()

            # 🔥 Permitir tudo
            if origin == "*":
                self.allow_all = True
                return

            # 🌐 Se for URL → extrair hostname
            if origin.startswith("http://") or origin.startswith("https://"):
                hostname = re.sub(r"^https?://", "", origin).split("/")[0]
                self.allowed_hosts.append(hostname)
            else:
                # 📌 IP ou domínio direto
                self.allowed_hosts.append(origin)

        # 🔒 Sempre permitir localhost
        if "127.0.0.1" not in self.allowed_hosts:
            self.allowed_hosts.append("127.0.0.1")

        if "localhost" not in self.allowed_hosts:
            self.allowed_hosts.append("localhost")

    async def dispatch(self, request: Request, call_next):
        client_host = request.client.host if request.client else None

        # 🔥 Se permitir tudo
        if self.allow_all:
            return await call_next(request)

        # ❌ Bloqueia host não permitido
        if client_host and client_host not in self.allowed_hosts:
            return Response(
                content="Access denied: Host not allowed",
                status_code=403,
                media_type="text/plain"
            )

        # ✅ Continua fluxo normal
        return await call_next(request)