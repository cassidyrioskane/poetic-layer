FROM python:3.11-slim

# System libs for Pillow (JPEG/PNG)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo-dev zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the top-level requirements into the image (build context is repo root on Render)
COPY requirements.txt /app/requirements.txt

# Install Python deps. We also explicitly install Pillow/numpy in case your
# top-level requirements.txt doesn’t include them (no harm if they’re already present).
RUN pip install --no-cache-dir -r /app/requirements.txt \
 && pip install --no-cache-dir Pillow numpy

# Copy shared packages and the mapping service code
COPY packages /app/packages
COPY services/mapping_service /app/services/mapping_service

# Make repo code importable as a package
ENV PYTHONPATH=/app

EXPOSE 8000
CMD ["uvicorn", "services.mapping_service.app:app", "--host", "0.0.0.0", "--port", "8000"]
