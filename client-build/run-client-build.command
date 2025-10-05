#!/bin/bash
set -Eeuo pipefail
cd "$(dirname "$0")"

echo "=== Poetic Layer Client Build ==="

# Prefer python3
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "❌ Python not found. Please install Python 3.11+ (Homebrew: brew install python) and rerun."
  exit 1
fi

# Ensure pip exists
$PY -m ensurepip --upgrade >/dev/null 2>&1 || true

# Create venv if missing
if [ ! -d "venv" ]; then
  echo "Creating virtual environment…"
  $PY -m venv venv
fi

source venv/bin/activate

echo "Upgrading pip…"
python -m pip install --upgrade pip

echo "Installing backend requirements…"
pip install -r requirements.txt

# Ensure Python can import the local "packages" package
export PYTHONPATH="$PWD"

echo "Starting Mapping Service on http://127.0.0.1:8000 …"
# If app.py does not start uvicorn by itself, use the line below instead.
# python -m uvicorn mapping-service.app:app --host 127.0.0.1 --port 8000
( python mapping-service/app.py ) >/tmp/mapping-service.log 2>&1 &

sleep 2
open "frontend/build/index.html" >/dev/null 2>&1 || true

echo "All set. Close this window to end."
