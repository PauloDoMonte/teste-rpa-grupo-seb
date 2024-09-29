FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src
COPY test/ ./test

RUN useradd -m appuser
USER appuser

CMD ["python", "src/main.py"]