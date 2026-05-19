from datetime import datetime, timezone

from fastapi import Request, Response
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


# 🔥 Cria limiter baseado no IP
limiter = Limiter(key_func=get_remote_address)


# 🔥 Handler personalizado
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """
    Retorna erro JSON amigável quando estoura o limite
    """

    # tempo de espera baseado no tipo
    detail_str = str(exc.detail).lower()

    if "minute" in detail_str:
        retry_after = 60
    elif "hour" in detail_str:
        retry_after = 3600
    elif "second" in detail_str:
        retry_after = 1
    else:
        retry_after = 60

    body = {
        "error": "Rate limit exceeded",
        "message": f"Too many requests. Limit: {exc.detail}",
        "retry_after": retry_after,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    response = Response(
        content=str(body).replace("'", '"'),  # garante JSON válido
        status_code=429,
        media_type="application/json",
    )

    # headers úteis
    response.headers["X-RateLimit-Limit"] = str(exc.detail)
    response.headers["X-RateLimit-Remaining"] = "0"
    response.headers["X-RateLimit-Reset"] = str(
        int(datetime.now(timezone.utc).timestamp()) + retry_after
    )
    response.headers["Retry-After"] = str(retry_after)

    return response


# 🔥 LIMITES
RATE_LIMITS = {
    "critical": "2/minute",     # login, delete
    "restrictive": "3/minute",  # criação e update
    "moderate": "5/minute",     # listagem
    "low": "10/minute",
    "light": "20/minute",
    "default": "5/minute",
}


# 🔥 Função para pegar limite
def get_rate_limit(endpoint_type: str) -> str:
    return RATE_LIMITS.get(endpoint_type, RATE_LIMITS["default"])