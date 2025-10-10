# services/mapping-service/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared packages
COPY packages ./packages

# Copy mapping-service source code
COPY services/mapping_service ./services/mapping_service

# Expose port and run
EXPOSE 8000
CMD ["uvicorn", "services.mapping_service.app:app", "--host", "0.0.0.0", "--port", "8000"]
