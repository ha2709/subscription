FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Optional: install curl for wait-for-it or debugging
RUN apt-get update && apt-get install -y curl && apt-get clean

# Load .env if python-dotenv is used
ENV PYTHONUNBUFFERED=1

EXPOSE 5000
CMD ["python", "main.py"]
