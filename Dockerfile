FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/crawler

# Default: run the example spider and write output.json to /app/output.json
CMD ["sh", "-c", "scrapy crawl example -o /app/output.json"]

