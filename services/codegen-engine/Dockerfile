FROM python:3.11-slim

WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code + shared packages
COPY packages ./packages
COPY services/codegen-engine ./services/codegen-engine

# Expose port and run
EXPOSE 8000
CMD ["uvicorn", "services.codegen-engine.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
