FROM python:3.11-slim

WORKDIR /app/services/mapping-service

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install fastapi uvicorn

COPY services/mapping-service /app/services/mapping-service

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
