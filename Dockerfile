# =========================
# BUILDER
# =========================
FROM python:3.11-alpine AS builder

RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

WORKDIR /install

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# =========================
# PRODUÇÃO
# =========================
FROM python:3.11-alpine

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PATH="/usr/local/bin:$PATH"

RUN apk add --no-cache curl

# usuário
RUN addgroup -g 1001 appuser && \
    adduser -D -u 1001 -G appuser appuser

WORKDIR /app

# dependências do builder
COPY --from=builder /install /usr/local

# 🔥 CORREÇÃO PRINCIPAL (mantém src como pasta)
COPY --chown=appuser:appuser ./src /app/src

# logs e cert
RUN mkdir -p /app/logs /cert && \
    chown -R appuser:appuser /app /cert

USER appuser

# healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
CMD curl -f https://localhost:4443/health --insecure || exit 1

EXPOSE 4443

# comando correto
ENTRYPOINT ["hypercorn"]
CMD ["--bind", "0.0.0.0:4443", "--quic-bind", "0.0.0.0:4443", "src.main:app"]
