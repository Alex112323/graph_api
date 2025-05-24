FROM python:3.11-slim

WORKDIR /graph_api

RUN apt-get update && apt-get install -y libpq-dev gcc dos2unix curl

# Копируем requirements.txt из config/
COPY config/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной проект
COPY . .

RUN dos2unix /graph_api/scripts/entrypoint.sh && chmod +x /graph_api/scripts/entrypoint.sh

ENTRYPOINT ["/graph_api/scripts/entrypoint.sh"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
