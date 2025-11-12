#!/usr/bin/env sh

# для надежности и безопасности
# Скрипт сразу завершится, если любая команда вернёт ошибку.
# Запрещает использование необъявленных переменных.
set -eu

# каталог для логов и попытка сменить владельца
mkdir -p /app/logs && chown -R appuser:appuser /app/logs || true

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Параметры
: "${WEB_CONCURRENCY:=3}"
: "${WEB_TIMEOUT:=120}"

# запускаем из под appuser и пишем имя проекта
exec gosu appuser:appuser gunicorn person_service.asgi:application \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --workers "${WEB_CONCURRENCY}" \
  --timeout "${WEB_TIMEOUT}" \
  --forwarded-allow-ips="*" # \
  # --log-config /app/uvicorn_logging.ini  # опционально
