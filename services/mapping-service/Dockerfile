FROM python:3.11-slim
WORKDIR /app

# Copy top-level requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared packages
COPY packages ./packages

# Copy service code
COPY services/mapping-service ./services/mapping-service

# Expose FastAPI port
EXPOSE 8000

CMD ["uvicorn", "services.mapping_service.app:app", "--host", "0.0.0.0", "--port", "8000"]
