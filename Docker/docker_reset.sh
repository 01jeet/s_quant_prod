#!/bin/bash

set -e

# Use the same path logic as your init script to ensure consistency
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/Docker/docker-compose.yml"
ROOT_ENV="$SCRIPT_DIR/.env.dev"

echo "-------------------------------------------------------"
echo "🛑 Shutting down and cleaning up environment..."
echo "COMPOSE_FILE: $COMPOSE_FILE"
echo "ENV_FILE: $ROOT_ENV"
echo "-------------------------------------------------------"

# docker compose down:
# - Stops and removes containers
# - Removes networks created by the compose file
# -v (or --volumes): Removes all named volumes declared in the volumes section
# (Note: We do NOT use --rmi, so your images stay downloaded on your disk)

docker compose \
  --env-file "$ROOT_ENV" \
  -f "$COMPOSE_FILE" \
  down -v #--rmi all 

# docker compose \
#   --env-file "$ROOT_ENV" \
#   -f "$COMPOSE_FILE" \
#   down -v --rmi all 

echo ""
echo "✅ Containers and Volumes removed. Images were preserved."
echo "✨ Environment is now clean."
