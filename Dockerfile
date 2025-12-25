FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN groupadd -r appuser && useradd -r -g appuser -d /app appuser

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
