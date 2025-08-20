FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt && pip install psycopg2-binary
CMD ["python", "master_orchestrator.py"]
