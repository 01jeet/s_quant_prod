# #!/bin/bash

# set -e

# SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# COMPOSE_FILE="$SCRIPT_DIR/Docker/docker-compose.yml"
# # ROOT_ENV="$(cd "$SCRIPT_DIR/../.." && pwd)/.env.dev"
# ROOT_ENV="$SCRIPT_DIR/.env.dev"

# echo "SCRIPT_DIR location: $SCRIPT_DIR"
# echo "docker compose location: $COMPOSE_FILE"
# echo "docker env for infra location: $ROOT_ENV"

# echo "🚀 Starting Docker ..."
# # echo ""


# docker compose \
#   --env-file "$ROOT_ENV" \
#   -f "$COMPOSE_FILE" \
#   up -d --wait

#!/bin/bash

# We use -e to stop on error, but we will handle directory creation carefully
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/Docker/docker-compose.yml"
ROOT_ENV="$SCRIPT_DIR/.env.dev"
CONFIG_FILE_PATH="$SCRIPT_DIR/Docker/centrifugo_config/centrifugo_config.json"
PG_ADMIN_CONFIG_PATH="$SCRIPT_DIR/Docker/pgadmin_config/servers.json"

echo "-------------------------------------------------------"
echo "SCRIPT_DIR: $SCRIPT_DIR"
echo "COMPOSE_FILE: $COMPOSE_FILE"
echo "ENV_FILE: $ROOT_ENV"
echo "-------------------------------------------------------"

# ------------------------------------------------------------------------------
# STEP 1: Load Environment Variables Robustly
# ------------------------------------------------------------------------------
echo "⚙️ Loading environment variables..."

# This loop reads the .env file line by line.
# It removes Windows \r, ignores comments, and handles spaces around '='
while IFS= read -r line || [ -n "$line" ]; do
  # Remove carriage return and trailing whitespace
  line=$(echo "$line" | tr -d '\r' | xargs)
  
  # Skip empty lines and comments
  [[ -z "$line" || "$line" == \#* ]] && continue
  
  # Split by '=' and export. This handles "VAR = VAL" by trimming spaces.
  key=$(echo "$line" | cut -d '=' -f 1 | xargs)
  val=$(echo "$line" | cut -d '=' -f 2- | xargs)
  
  export "$key"="$val"
done < "$ROOT_ENV"

# ------------------------------------------------------------------------------
# STEP 2_a: Generate Centrifugo JSON (Fresh Setup)
# ------------------------------------------------------------------------------
echo "⚙️ Preparing Centrifugo config..."

# Get the directory name from the full path
CONFIG_DIR="$(dirname "$CONFIG_FILE_PATH")"

# 1. Create directory if it doesn't exist
if [ ! -d "$CONFIG_DIR" ]; then
    echo "📂 Directory $CONFIG_DIR not found. Creating it now..."
    mkdir -p "$CONFIG_DIR"
    # Check if mkdir actually worked
    if [ ! -d "$CONFIG_DIR" ]; then
        echo "❌ ERROR: Failed to create directory $CONFIG_DIR. Check folder permissions."
        exit 1
    fi
fi

# 2. Remove the old file to ensure it's a "fresh" copy
if [ -f "$CONFIG_FILE_PATH" ]; then
    rm -f "$CONFIG_FILE_PATH"
fi

# 3. Write the fresh JSON file
# We use a heredoc. Variables are injected from the loop above.
cat <<EOF > "$CONFIG_FILE_PATH"
{
  "engine": {
    "type": "redis",
    "redis": {
      "address": "valkey:6379",
      "password": "${VALKEY_PASSWORD}"
    }
  },
  "client": {
    "token": {
      "hmac_secret_key": "${CENTRIFUGO_TOKEN_HMAC_SECRET}"
    },
    "allowed_origins": [
      "*"
    ]
  },
  "http_api": {
    "key": "${CENTRIFUGO_API_KEY}"
  },
  "admin": {
    "password": "${CENTRIFUGO_ADMIN_PASSWORD}",
    "secret": "${CENTRIFUGO_ADMIN_SECRET}",
    "enabled": true
  }
}
EOF

if [ -f "$CONFIG_FILE_PATH" ]; then
    echo "✅ Fresh config successfully generated at: $CONFIG_FILE_PATH"
else
    echo "❌ ERROR: Failed to write the config file."
    exit 1
fi


# ------------------------------------------------------------------------------
# STEP 2_b: Generate Centrifugo JSON (Fresh Setup)
# ------------------------------------------------------------------------------

echo "⚙️ Preparing pg_admin server config..."

# Get the directory name from the full path
CONFIG_DIR_PGADMIN="$(dirname "$PG_ADMIN_CONFIG_PATH")"

# 1. Create directory if it doesn't exist
if [ ! -d "$CONFIG_DIR_PGADMIN" ]; then
    echo "📂 Directory $CONFIG_DIR_PGADMIN not found. Creating it now..."
    mkdir -p "$CONFIG_DIR_PGADMIN"
    # Check if mkdir actually worked
    if [ ! -d "$CONFIG_DIR_PGADMIN" ]; then
        echo "❌ ERROR: Failed to create directory $CONFIG_DIR_PGADMIN. Check folder permissions."
        exit 1
    fi
fi

# 2. Remove the old file to ensure it's a "fresh" copy
if [ -f "$PG_ADMIN_CONFIG_PATH" ]; then
    rm -f "$PG_ADMIN_CONFIG_PATH"
fi

# 3. Write the fresh JSON file
# We use a heredoc. Variables are injected from the loop above.
cat <<EOF > "$PG_ADMIN_CONFIG_PATH"
{
    "Servers": {
        "1": {
            "Name": "Production Postgres",
            "Group": "Servers",
            "Host":  "${PGADMIN_SERVER_HOST}",
            "Port": "${INFRA_POSTGRES_PORT}",
            "Username": "${INFRA_POSTGRES_USER}",
            "DB":"${INFRA_POSTGRES_DB}",
            "PassWord": "${INFRA_POSTGRES_PASSWORD}",
            "SSLMode": "prefer"
        }
    }
}
EOF

if [ -f "$PG_ADMIN_CONFIG_PATH" ]; then
    echo "✅ Fresh config successfully generated at: $PG_ADMIN_CONFIG_PATH"
else
    echo "❌ ERROR: Failed to write the config file."
    exit 1
fi
# ------------------------------------------------------------------------------
# STEP 3: Start Docker
# ------------------------------------------------------------------------------
echo "🚀 Starting Docker ..."

docker compose \
  --env-file "$ROOT_ENV" \
  -f "$COMPOSE_FILE" \
  up -d --wait

echo "✨ All systems started successfully!"



# #!/bin/bash
# set -e
# #Start system
# echo "🚀 Starting system..."

# echo ""
# bash Docker/infra/start_infra_docker.sh
# echo "✔ Infra Docker up and running"
# echo ""

# echo ""
# bash Docker/temporal/start_temporal_docker.sh
# echo "✔ Temporal Docker up and running"
# echo ""