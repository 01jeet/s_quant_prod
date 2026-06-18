#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/Docker/docker-compose.yml"
# ROOT_ENV="$(cd "$SCRIPT_DIR/../.." && pwd)/.env.dev"
ROOT_ENV="$SCRIPT_DIR/.env.dev"

echo "SCRIPT_DIR location: $SCRIPT_DIR"
echo "docker compose location: $COMPOSE_FILE"
echo "docker env for infra location: $ROOT_ENV"

echo "🚀 Starting Docker ..."
# echo ""


docker compose \
  --env-file "$ROOT_ENV" \
  -f "$COMPOSE_FILE" \
  stop 