FROM python:3.11-slim

WORKDIR /app

# --- System dependencies (needed for Pillow image handling) ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev \
 && rm -rf /var/lib/apt/lists/*

# --- Copy requirements and install Python deps ---
COPY requirements.txt .
# Add fallback install for Pillow in case requirements.txt doesn’t list it
RUN pip install --no-cache-dir -r requirements.txt Pillow

# --- Copy shared packages and service code ---
COPY packages ./packages
COPY services/mapping_service ./services/mapping_service

EXPOSE 8000

# --- Start the mapping service ---
CMD ["uvicorn", "services.mapping_service.app:app", "--host", "0.0.0.0", "--port", "8000"]
