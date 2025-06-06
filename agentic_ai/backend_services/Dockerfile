FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip uv \
    && pip install -r requirements.txt
COPY agentic_ai /app/agentic_ai
ENV PYTHONPATH=/app/agentic_ai
EXPOSE 8000
CMD ["watchmedo", "auto-restart", "--patterns=*.py;*.env", "--recursive", "--", "python", "agentic_ai/backend_services/mcp_service.py"]
