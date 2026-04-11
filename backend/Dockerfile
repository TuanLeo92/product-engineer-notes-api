FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=1
# Local default only; on Railway, PORT is injected at runtime (often 8080, not 8000).
ENV PORT=8000

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

# Port expansion happens in entrypoint.sh (shell), not in JSON exec argv.
ENTRYPOINT ["/app/entrypoint.sh"]