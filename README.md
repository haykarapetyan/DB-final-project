# Simple REST API for University Sessions

This project implements a small FastAPI application with PostgreSQL (SQLAlchemy) and Alembic migrations. It models Groups, Subjects and Sessions (see ER diagram provided by the instructor).

Quick setup (assumes PostgreSQL is available):

```bash
# create a virtualenv and install
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# create DB using the script (edit names/owner as needed)
bash scripts/init_db.sh mydb myuser

# run alembic migrations
alembic upgrade head

# start the app
uvicorn app.main:app --reload
```

See `scripts/populate_via_api.py` for a script that fills the DB through the REST API.

Notes:
- The `scripts/init_db.sh` creates a PostgreSQL database and owner (requires sudo or appropriate privileges).
- Two example Alembic migrations are included: initial tables and adding JSON field + GIN+pg_trgm index.