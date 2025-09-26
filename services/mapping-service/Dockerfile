FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code + shared packages
COPY services/mapping-service ./services/mapping-service
COPY packages ./packages

EXPOSE 8000
CMD ["uvicorn", "services.mapping_service.app:app", "--host", "0.0.0.0", "--port", "8000"]
