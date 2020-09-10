#!/bin/sh

cat << EOF > .env
POSTGRES_USER=oreilly
POSTGRES_PASSWORD=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c "${1:-16}")
FLASK_ENV=Production
SECRET_KEY=$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c "${1:-16}")
EOF