FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /srv/pdf_service

# Create non-root user for Cloud Run runtime
RUN groupadd -r nvpdf && useradd -r -g nvpdf nvpdf

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

USER nvpdf
EXPOSE 8080

CMD ["uvicorn", "app.services.internal_pdf_worker_service:app", "--host", "0.0.0.0", "--port", "8080", "--limit-max-requests", "1000", "--timeout-keep-alive", "5"]
