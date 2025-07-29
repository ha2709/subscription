FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Optional: install curl for wait-for-it or debugging
RUN apt-get update && apt-get install -y curl && apt-get clean

# Environment setup
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV FLASK_APP=main:app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000
CMD ["python", "main.py"]
