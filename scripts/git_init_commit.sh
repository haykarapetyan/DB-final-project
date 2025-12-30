#!/usr/bin/env bash
set -euo pipefail

if [ ! -d .git ]; then
  git init
  git add .
  git commit -m "Initial scaffold: FastAPI app, models, Alembic migrations, scripts"
  echo "Repository initialized and initial commit created."
else
  echo "Git repository already initialized."
fi
