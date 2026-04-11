FROM python:3.11

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# $PORT is set by Railway at runtime (e.g. 8080). Bind all interfaces.
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port \"${PORT}\""]