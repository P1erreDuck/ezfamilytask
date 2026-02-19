FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY back/ .

COPY docker/wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

CMD ["/wait-for-postgres.sh", "postgres", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]