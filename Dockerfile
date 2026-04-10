# Build from Git repo root. Railway connects the whole repo; context must be `.` not `backend/`.
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
# Railway injects PORT at runtime (overrides this). Never leave PORT empty in the dashboard.
ENV PORT=8000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Listen on 0.0.0.0 and Railway's $PORT. Proxy headers for HTTPS / public URL in OpenAPI.
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port \"${PORT}\" --proxy-headers --forwarded-allow-ips='*'"]
