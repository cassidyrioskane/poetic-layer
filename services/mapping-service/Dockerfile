FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY packages ./packages
COPY services/mapping-service ./services/mapping-service
EXPOSE 8000
CMD ["uvicorn", "services.mapping_service.app:app", "--host", "0.0.0.0", "--port", "8000"]
