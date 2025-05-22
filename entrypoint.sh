#!/bin/sh

echo "Ожидание запуска базы данных..."

while ! python -c "import socket; s=socket.socket(); s.settimeout(1); s.connect(('db', 5432)); s.close()" 2>/dev/null; do
  echo "Ждем базу на db:5432..."
  sleep 1
done

echo "База доступна, запускаем миграции..."

alembic upgrade head

echo "Запускаем основное приложение..."

exec "$@"
