"""
Production Gunicorn + Uvicorn Worker Configuration
Numeros Vision & Charm AI — High-Concurrency Production ASGI Server
"""

import multiprocessing
import os

# Worker Processes: Recommended formula (2 x CPU cores) + 1
# On a 4-vCPU production container/VM, this spawns 9 concurrent worker processes
cpu_count = multiprocessing.cpu_count()
workers = int(os.getenv("WEB_CONCURRENCY", (2 * cpu_count) + 1))

# ASGI Worker Class for high-throughput asynchronous I/O
worker_class = "uvicorn.workers.UvicornWorker"

# Network Binding
bind = os.getenv("BIND_ADDRESS", "0.0.0.0:8000")

# High-Concurrency Connection Backlog & Timeouts
backlog = 2048
timeout = 120
keepalive = 5
graceful_timeout = 30

# Memory Leak Prevention: Max requests per worker before recycle
max_requests = 2000
max_requests_jitter = 200

# Logging & Observability
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s µs'
