FROM python:3.11-slim

WORKDIR /graph_api

RUN apt-get update && apt-get install -y libpq-dev gcc dos2unix curl

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN dos2unix /graph_api/entrypoint.sh && chmod +x /graph_api/entrypoint.sh

ENTRYPOINT ["/graph_api/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
