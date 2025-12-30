#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <dbname> <owner> [pg_superuser]"
  exit 1
fi

DBNAME=$1
DBOWNER=$2
PG_SUPERUSER=${3:-postgres}

echo "Creating database '$DBNAME' with owner '$DBOWNER' (superuser $PG_SUPERUSER)..."

psql -v ON_ERROR_STOP=1 -U "$PG_SUPERUSER" <<-SQL
CREATE ROLE "$DBOWNER" WITH LOGIN PASSWORD 'changeme';
CREATE DATABASE "$DBNAME" OWNER "$DBOWNER";
\connect "$DBNAME";
CREATE EXTENSION IF NOT EXISTS pg_trgm;
SQL

echo "Done. Edit password and privileges as needed."
