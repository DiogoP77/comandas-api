from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from datetime import datetime, timezone

# 🔥 Cria limiter baseado no IP
limiter = Limiter(key_func=get_remote_address)


# 🔥 Handler personalizado
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """
    Retorna erro JSON amigável quando estoura o limite
    """

    # tempo de espera baseado no tipo
    if "minute" in str(exc.detail):
        retry_after = 60
    elif "hour" in str(exc.detail):
        retry_after = 3600
    elif "second" in str(exc.detail):
        retry_after = 1
    else:
        retry_after = 60

    response = Response(
        content=f"""
        {{
            "error": "Rate limit exceeded",
            "message": "Too many requests. Limit: {exc.detail}",
            "retry_after": {retry_after},
            "timestamp": "{datetime.now(timezone.utc).isoformat()}"
        }}
        """,
        status_code=429,
        media_type="application/json"
    )

    # headers úteis
    response.headers["X-RateLimit-Limit"] = str(exc.detail)
    response.headers["X-RateLimit-Remaining"] = "0"
    response.headers["X-RateLimit-Reset"] = str(int(datetime.now(timezone.utc).timestamp()) + retry_after)
    response.headers["Retry-After"] = str(retry_after)

    return response


# 🔥 LIMITES (AJUSTADO PRA APRESENTAÇÃO)
RATE_LIMITS = {
    "critical": "2/minute",     # login, delete
    "restrictive": "3/minute",  # criação e update
    "moderate": "5/minute",     # listagem 🔥 USADO NA SUA ROTA
    "low": "10/minute",
    "light": "20/minute",
    "default": "5/minute"
}


# 🔥 Função para pegar limite
def get_rate_limit(endpoint_type: str) -> str:
    return RATE_LIMITS.get(endpoint_type, RATE_LIMITS["default"])