# Build from Git repo root. Railway connects the whole repo; context must be `.` not `backend/`.
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Behind Railway's proxy, forward X-Forwarded-* so /openapi.json and Swagger "Try it" use the public URL.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --proxy-headers --forwarded-allow-ips='*'"]
