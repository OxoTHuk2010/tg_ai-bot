####BUILD
FROM python:3.12-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates tzdata build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /wheels
COPY requirements.txt .
RUN pip install -U pip wheel \
    && pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt


####RUNTIME
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 10001 appuser
WORKDIR /app

COPY --from=builder /wheels /wheels
RUN python -m pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY . .

USER appuser

CMD ["python", "main.py"]