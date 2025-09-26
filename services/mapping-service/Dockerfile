FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code only
COPY services/mapping-service/ ./services/mapping-service/

# Expose port and run
EXPOSE 8000
CMD ["uvicorn", "services.mapping-service.app:app", "--host", "0.0.0.0", "--port", "8000"]
