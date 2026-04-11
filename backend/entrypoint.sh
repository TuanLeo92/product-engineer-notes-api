#!/usr/bin/env sh
set -e
# Railway injects PORT at runtime. Always expand in shell — some runners invoke
# uvicorn without a shell and would pass the literal "$PORT" to --port.
PORT="${PORT:-8000}"
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT}"
