#!/bin/sh

password="$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c "${1:-16}")"
secret="$(< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c "${1:-16}")"

cat << EOF > .env
POSTGRES_USER=oreilly
POSTGRES_PASSWORD=${password}
FLASK_ENV=Production
SECRET_KEY=${secret}
EOF

cat << EOF > k8s-secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: oreilly-app-secrets
type: Opaque
data:
  POSTGRES_USER: $(printf "oreilly" | base64)
  POSTGRES_PASSWORD: $(printf "%s" "${password}" | base64)
  FLASK_ENV: $(printf "Production" | base64)
  SECRET_KEY: $(printf "%s" "${secret}" | base64)
EOF