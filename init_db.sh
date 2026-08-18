#!/bin/sh

# Loads db initialization
# User in https://github.com/identicum/sherpa-iam/

set -eu

export PGHOST="${PGHOST:-db}"
export PGPORT="${PGPORT:-5432}"
export PGUSER="${POSTGRES_USER:-postgres}"
export PGPASSWORD="${POSTGRES_PASSWORD:-identicum}"

echo "Loading hr_0.sql and hr_data.sql into ${PGHOST}:${PGPORT} as ${PGUSER}..."
psql -v ON_ERROR_STOP=1 -f /db/hr_0.sql
psql -v ON_ERROR_STOP=1 -f /db/hr_data.sql
echo "Done."
