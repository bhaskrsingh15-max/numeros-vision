FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /srv/engine_service

RUN groupadd -r nvengine && useradd -r -g nvengine nvengine

COPY engine_service/requirements.txt ./requirements.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update \
    && apt-get install -y --no-install-recommends tesseract-ocr fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

COPY app/ ./app/
COPY data/ ./data/

USER nvengine
EXPOSE 8080

CMD ["sh", "-c", "exec uvicorn app.services.internal_engine_service:app --host 0.0.0.0 --port ${PORT:-8080} --limit-max-requests 2000 --timeout-keep-alive 5"]
