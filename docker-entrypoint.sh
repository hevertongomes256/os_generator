#!/usr/bin/env bash
set -o errexit

# Aguarda o banco de dados ficar online (opcional, útil em ambientes cloud)
if [ "$WAIT_FOR_DB" = "true" ]; then
  echo "Waiting for database..."
  while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
    sleep 1
  done
fi

echo "Rodando migrações do Django..."
python manage.py migrate

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --no-input

echo "Iniciando aplicação..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:8000
