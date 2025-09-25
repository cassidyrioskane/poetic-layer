FROM python:3.11-slim

WORKDIR /app

# Install dependencies from top-level requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared packages
COPY packages ./packages

# Copy mapping-service source code
COPY services/mapping-service ./services/mapping-service

# Expose FastAPI port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "services.mapping_service.app:app", "--host", "0.0.0.0", "--port", "8000"]
