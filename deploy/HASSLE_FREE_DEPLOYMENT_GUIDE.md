# Numeros Vision & Charm AI — Hassle-Free Production Deployment Guide
**Zero-Downtime · Zero-Disturbance · Cloud-Native · Dual-Engine Scalability**

---

## 1. Zero-Hammering Architecture Guarantee

The implementation of the **Enterprise Agentic AI Architecture Blueprint** has been engineered strictly using the **Decorator/Gateway Pattern**:
- **Existing Occult Engines Untouched**: Vedic Numerology, Chaldean, Lo Shu 3x3 Grid, Vimshottari Dasha, Lal Kitab, KP Astrology, and Bhrigu Nandi Nadi remain mathematically identical with sub-millisecond in-memory execution.
- **Frontend & Visual Identity Preserved**: The Venus Pearl (`#FFFDF7`) and Jupiter Gold (`#C9A227`) design system, AstroTalk 2-step consultation UX, Crystal Remedies, and dynamic calculators operate with zero disruption.
- **Additive Security Perimeter**: The `EnterpriseAgentGateway` wraps input queries, enforces data perimeters, checks circuit breakers, and generates immutable audit traces (`NV-TRC-...`) without altering core calculation pipelines.
- **Backward-Compatible Session Management**: Payment sessions operate flawlessly from local JSON storage by default, and automatically activate Redis distributed cluster caching when `REDIS_URL` is set in production.

---

## 2. Hassle-Free Deployment Options

### Option A: Docker Compose (Recommended for Single VM / VPS)
*Turnkey stack with FastAPI ASGI application, Redis 7 caching, and Nginx reverse proxy.*

1. **Clone/Navigate to Project**:
   ```bash
   cd "AI Numrology"
   ```
2. **Launch Container Stack**:
   ```bash
   docker-compose -f deploy/docker-compose.prod.yml up -d --build
   ```
3. **Verify Health**:
   ```bash
   curl http://localhost/health
   curl http://localhost/api/v1/agent/status
   ```

---

### Option B: Google Cloud Run (Fully Managed Serverless Autoscaling)
*Zero server management, automatic scaling from 0 to 1000 concurrent containers.*

1. **Build and Submit Container**:
   ```bash
   gcloud builds submit --tag gcr.io/[PROJECT-ID]/numeros-vision-agent:v4.1.0 -f deploy/Dockerfile .
   ```
2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy numeros-vision \
       --image gcr.io/[PROJECT-ID]/numeros-vision-agent:v4.1.0 \
       --platform managed \
       --region asia-south1 \
       --allow-unauthenticated \
       --concurrency 80 \
       --min-instances 1 \
       --max-instances 25 \
       --memory 2Gi \
       --cpu 2
   ```

---

### Option C: Bare-Metal Linux / Ubuntu VPS (Systemd Service)
*Direct host deployment using Gunicorn and Uvicorn workers.*

1. **Run Hassle-Free Launch Script**:
   ```bash
   chmod +x deploy/deploy_production.sh
   ./deploy/deploy_production.sh
   ```
2. **(Optional) Install Systemd Service**:
   Create `/etc/systemd/system/numeros-vision.service`:
   ```ini
   [Unit]
   Description=Numeros Vision & Charm AI Enterprise Agent Engine
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/ai-numerology
   Environment="PATH=/var/www/ai-numerology/.venv/bin"
   Environment="WEB_CONCURRENCY=9"
   ExecStart=/var/www/ai-numerology/.venv/bin/gunicorn -c deploy/gunicorn_conf.py app.main:app
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```
   Enable and start:
   ```bash
   sudo systemctl enable --now numeros-vision
   ```

---

### Option D: Kubernetes (Enterprise Orchestration)
*Multi-pod rolling updates, liveness/readiness probes, and Horizontal Pod Autoscaler.*

```bash
kubectl apply -f deploy/k8s-deployment.yaml
kubectl get hpa numeros-vision-hpa
```

---

## 3. Production Health & Observability Endpoints

| Endpoint | Method | Purpose | Sample Output |
| :--- | :---: | :--- | :--- |
| `/health` | `GET` | Container/Load Balancer Health Probe | `{"status": "ok"}` |
| `/api/v1/agent/status` | `GET` | Enterprise Agent Gateway Health & Manifest | Identity, Perimeters, Tool tiers |
| `/api/v1/agent/traces` | `GET` | Real-time Decision Traceability Ledger | Trace IDs, latencies, circuit status |
| `/disclaimer` | `GET` | Institutional Statutory Legal Disclosure | Full legal & non-medical disclosure |

---

## 4. Disaster Recovery & Rollback

- **Instant Rollback**: If an emergency occurs, the pre-change clean snapshot is safely archived at:
  - `backups/numeros_vision_backup_v4.1.0-enterprise-agentic-gateway_20261015_004839.tar.gz`
  - Uncompressed baseline copy: `backups/version_copy_v4.0.5/`
- **Zero Schema Migrations**: All engines and session stores use schema-less or forward-compatible structures, guaranteeing 100% safe rollbacks.
