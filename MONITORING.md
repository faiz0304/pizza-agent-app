# Monitoring & Error Tracking Setup

## 📊 Error Tracking with Sentry

### Backend Setup

1. **Install Sentry**:
```bash
pip install sentry-sdk[fastapi]
```

2. **Add to `main.py`**:
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("ENVIRONMENT", "development"),
    traces_sample_rate=1.0,
    integrations=[FastApiIntegration()]
)
```

### Frontend Setup

1. **Install Sentry**:
```bash
npm install @sentry/nextjs
```

2. **Create `sentry.client.config.js`**:
```javascript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
});
```

---

## 📈 Performance Monitoring

### Application Performance Monitoring (APM)

**Prometheus + Grafana Setup**:

1. **Add prometheus-fastapi-instrumentator**:
```bash
pip install prometheus-fastapi-instrumentator
```

2. **In `main.py`**:
```python
from prometheus_fastapi_instrumentator import Instrumentator

@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)
```

3. **Metrics available at**: `http://localhost:8000/metrics`

---

## 🔍 Logging Strategy

### Structured Logging

**Add to `backend/utils/logger.py`**:
```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "tool"):
            log_data["tool"] = record.tool
        return json.dumps(log_data)

# Configure logger
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("pizza_agent")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

---

## 📱 WhatsApp Monitoring

### Track Message Flow

**Add to `routes/whatsapp.py`**:
```python
import logging

webhook_logger = logging.getLogger("whatsapp_webhook")

# Log every incoming message
webhook_logger.info(
    "WhatsApp message received",
    extra={
        "from": From,
        "message_sid": MessageSid,
        "message_length": len(Body)
    }
)

# Log agent decision
webhook_logger.info(
    "Agent response",
    extra={
        "tool_used": result.get("tool"),
        "response_length": len(response_text)
    }
)
```

---

## 🎯 Custom Metrics

### Agent Tool Usage Tracking

**Create `backend/utils/metrics.py`**:
```python
from collections import Counter
from datetime import datetime, timedelta

class MetricsCollector:
    def __init__(self):
        self.tool_calls = Counter()
        self.response_times = []
        self.errors = Counter()
    
    def track_tool_call(self, tool_name):
        self.tool_calls[tool_name] += 1
    
    def track_response_time(self, duration):
        self.response_times.append(duration)
    
    def track_error(self, error_type):
        self.errors[error_type] += 1
    
    def get_stats(self):
        return {
            "tool_calls": dict(self.tool_calls),
            "avg_response_time": sum(self.response_times) / len(self.response_times) if self.response_times else 0,
            "errors": dict(self.errors)
        }

metrics = MetricsCollector()
```

**Add endpoint in `main.py`**:
```python
@app.get("/metrics/agent")
async def agent_metrics():
    return metrics.get_stats()
```

---

## 🚨 Alerting

### Slack Alerts for Critical Errors

**Add to `backend/utils/alerts.py`**:
```python
import requests
import os

def send_slack_alert(message, level="error"):
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        return
    
    color = {"error": "danger", "warning": "warning", "info": "good"}[level]
    
    payload = {
        "attachments": [{
            "color": color,
            "title": f"🍕 Pizza Agent Alert - {level.upper()}",
            "text": message,
            "footer": "Agentic Pizza System",
            "ts": int(time.time())
        }]
    }
    
    requests.post(webhook_url, json=payload)
```

**Use in error handling**:
```python
try:
    # Critical operation
    pass
except Exception as e:
    send_slack_alert(f"Critical error: {str(e)}", level="error")
    raise
```

---

## 📊 Dashboard Setup

### Grafana Dashboard JSON

**Save as `grafana-dashboard.json`**:
```json
{
  "dashboard": {
    "title": "Pizza Agent Metrics",
    "panels": [
      {
        "title": "Request Rate",
        "targets": [{"expr": "rate(http_requests_total[5m])"}]
      },
      {
        "title": "Agent Tool Usage",
        "targets": [{"expr": "agent_tool_calls_total"}]
      },
      {
        "title": "Response Time",
        "targets": [{"expr": "http_request_duration_seconds"}]
      }
    ]
  }
}
```

---

## 🔐 Security Monitoring

### Rate Limiting with Redis

**Install**:
```bash
pip install fastapi-limiter redis
```

**Add to `main.py`**:
```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis

@app.on_event("startup")
async def startup():
    redis_client = redis.from_url("redis://localhost")
    await FastAPILimiter.init(redis_client)

# Add to routes
@app.post("/chatbot", dependencies=[Depends(RateLimiter(times=5, seconds=10))])
async def chat(request: ChatRequest):
    # ... existing code
```

---

## 📝 Environment Variables

Add to `.env`:
```env
# Monitoring
SENTRY_DSN=https://...@sentry.io/...
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
REDIS_URL=redis://localhost:6379

# Metrics
PROMETHEUS_ENABLED=true
METRICS_PORT=9090
```

---

## 🧪 Health Checks

### Enhanced Health Endpoint

Update `/health` in `main.py`:
```python
@app.get("/health")
async def health_check():
    checks = {
        "database": check_database(),
        "chroma": check_chroma(),
        "llm": check_llm_connection(),
        "redis": check_redis()
    }
    
    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503
    
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if all_healthy else "degraded",
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
```

---

## 📱 Frontend Monitoring

### Add Error Boundary

**Create `components/ErrorBoundary.tsx`**:
```typescript
'use client';

import { Component, ReactNode } from 'react';
import * as Sentry from '@sentry/nextjs';

export class ErrorBoundary extends Component<
  { children: ReactNode },
  { hasError: boolean }
> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    Sentry.captureException(error, { extra: errorInfo });
  }

  render() {
    if (this.state.hasError) {
      return <h2>Something went wrong. Please refresh.</h2>;
    }
    return this.props.children;
  }
}
```

---

**Total Setup Time**: ~2 hours  
**Ongoing Maintenance**: ~30 min/week  
**ROI**: Early error detection, performance optimization, better UX
