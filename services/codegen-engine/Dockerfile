FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code + shared packages
COPY services/codegen-engine ./services/codegen-engine
COPY packages ./packages

EXPOSE 8001
CMD ["uvicorn", "services.codegen_engine.app:app", "--host", "0.0.0.0", "--port", "8001"]
