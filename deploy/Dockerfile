# Production Multi-Stage Dockerfile for Numeros Vision & Charm AI
FROM python:3.11-slim as builder

WORKDIR /build

# Install build essentials for C-extensions (numpy, scipy, swisseph if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install to virtual environment
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
# Note: In case requirements.txt has UTF-16 encoding, convert or install direct dependencies
RUN pip install --no-cache-dir \
    fastapi==0.110.0 \
    uvicorn[standard]==0.28.0 \
    gunicorn==21.2.0 \
    pydantic==2.6.4 \
    jinja2==3.1.3 \
    python-multipart==0.0.9 \
    requests==2.31.0 \
    httpx==0.27.0 \
    numpy \
    redis==5.0.3

# Final Production Runner Stage
FROM python:3.11-slim as runner

# Security: Non-root application user
RUN groupadd -g 1001 numeros && useradd -u 1001 -g numeros -m numeros

WORKDIR /app

# Copy virtualenv from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy application code, static assets, and templates
COPY --chown=numeros:numeros app/ ./app/
COPY --chown=numeros:numeros data/ ./data/
COPY --chown=numeros:numeros deploy/ ./deploy/
COPY --chown=numeros:numeros VERSION .

# Switch to non-root user
USER numeros

# Expose internal ASGI port
EXPOSE 8000

# Health check probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/health || exit 1

# Production Start Command via Gunicorn with Uvicorn ASGI workers
CMD ["gunicorn", "-c", "deploy/gunicorn_conf.py", "app.main:app"]
