"""
ZERO-COST STRUCTURED JSON SECURITY & AUDIT LOGGER
Zero external dependencies (uses standard Python logging + json).
Logs API access, execution latency, security blocks, and consent audit events in structured JSON.
"""

import logging
import json
import time
from typing import Dict, Any

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage()
        }
        if hasattr(record, "extra_data"):
            log_record["data"] = record.extra_data
        return json.dumps(log_record)

def get_logger(name: str = "prediction_engine"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

app_logger = get_logger()

def log_security_event(event_type: str, details: Dict[str, Any]):
    app_logger.warning(f"SECURITY_EVENT: {event_type}", extra={"extra_data": details})

def log_audit_event(event_type: str, details: Dict[str, Any]):
    app_logger.info(f"AUDIT_EVENT: {event_type}", extra={"extra_data": details})
