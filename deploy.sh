#!/usr/bin/env bash
set -euo pipefail

IMAGE="${1:?IMAGE tag is required}"
APP_DIR="${2:?APP_DIR tag is required}"
SERVICE_NAME="person-service" # менять это значение

COMPOSE_FILE="$APP_DIR/docker-compose.prod.yml"
LOGS_VOLUME="${SERVICE_NAME}-logs"
LOGS_DIR="/var/log/${SERVICE_NAME}"

# === Проверка/создание каталога ===
if [ ! -d "$LOGS_DIR" ]; then
  echo "Папка $LOGS_DIR не существует, создаю..."
  sudo mkdir -p "$LOGS_DIR"
else
  echo "Папка $LOGS_DIR уже существует."
fi

echo "=== 1. Проверяем / создаём том ${LOGS_VOLUME} ==="
if ! docker volume inspect "${LOGS_VOLUME}" >/dev/null 2>&1; then
  docker volume create \
    --driver local \
    --opt type=none \
    --opt o=bind \
    --opt device="$LOGS_DIR" \
    "$LOGS_VOLUME"
  echo "Создан том ${LOGS_VOLUME}"
else
  echo "Том ${LOGS_VOLUME} уже существует"
fi


echo "Starting deployment of $IMAGE"

cd "$APP_DIR"

echo "Stopping and removing old containers..."
docker compose -f "$COMPOSE_FILE" down || true

echo "Cleaning up dangling images..."
docker image prune -af || true

echo "Pulling new image..."
docker pull "$IMAGE"

echo "Starting containers..."

export IMAGE="$IMAGE"
docker compose -f "$COMPOSE_FILE" up -d --remove-orphans

echo "Cleaning up old images (keeping the latest 2)..."
# Удалим все, кроме двух последних по времени
docker images "${IMAGE%:*}" --format "{{.Repository}}:{{.Tag}}" | tail -n +3 | xargs -r docker rmi || true

echo "$IMAGE" > "$APP_DIR/.current_image"
