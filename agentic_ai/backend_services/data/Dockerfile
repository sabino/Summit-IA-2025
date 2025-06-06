FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt
COPY agentic_ai/backend_services/data /app
ENV PYTHONPATH=/app
CMD ["python", "create_db.py"]
