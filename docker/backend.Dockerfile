FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY back/ .

COPY back/init.py /app/init.py

CMD ["sh", "-c", "until pg_isready -h postgres -U postgres; do echo waiting for postgres; sleep 2; done; python init.py && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
