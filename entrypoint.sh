#!/bin/sh
set -e

echo "Esperando a MariaDB en $DB_HOST:$DB_PORT..."
ATTEMPTS=30
for i in $(seq 1 $ATTEMPTS); do
  python - <<'PY'
import os, socket, sys
host=os.environ.get('DB_HOST','db')
port=int(os.environ.get('DB_PORT','3306'))
s=socket.socket()
try:
    s.connect((host,port))
    s.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
PY
  if [ $? -eq 0 ]; then
    echo "Base de datos accesible."
    break
  fi
  echo "Aún esperando ($i/$ATTEMPTS)..."
  sleep 1
done

if [ "$i" = "$ATTEMPTS" ]; then
  echo "No se pudo conectar a la base de datos" >&2
  exit 1
fi

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

if [ "$LOAD_FIXTURES" = "true" ]; then
  echo "Cargando fixtures seed..."
  python manage.py loaddata fixtures/seed.json || echo "Fixtures no cargadas"
fi

echo "Iniciando Gunicorn..."
exec gunicorn CRUD.wsgi:application --bind 0.0.0.0:8000 --workers=${GUNICORN_WORKERS:-3}
