#!/bin/sh
set -e

echo "Waiting for database to be available..."

python - <<'PY'
import os, time, sys
import psycopg2

host = os.environ.get("DATABASE_HOST", "db")
port = os.environ.get("DATABASE_PORT", "5432")
dbname = os.environ.get("POSTGRES_DB")
user = os.environ.get("POSTGRES_USER")
pwd = os.environ.get("POSTGRES_PASSWORD")

for i in range(60):
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=pwd, host=host, port=port)
        conn.close()
        print("Database reachable")
        sys.exit(0)
    except Exception as e:
        print(f"Waiting for db ({i+1}/60): {e}")
        time.sleep(1)
print("Timed out waiting for database", file=sys.stderr)
sys.exit(1)
PY

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Django Server..."
exec python manage.py runserver 0.0.0.0:8000