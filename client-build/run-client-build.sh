#!/bin/bash
echo "=== Starting Client Build ==="

# Install backend dependencies if missing
if ! command -v pip &> /dev/null; then
    echo 'Installing pip...'
    python3 -m ensurepip --upgrade
fi
python3 -m pip install --upgrade pip
python3 -m pip install -r client-build/mapping-service/requirements.txt

# Install 'serve' if missing
if ! command -v serve &> /dev/null; then
    echo 'Installing serve...'
    npm install -g serve
fi

# Start mapping service in background
python3 client-build/mapping-service/app.py &

# Find an available port for frontend
PORT=3000
while lsof -i:$PORT &>/dev/null; do
    PORT=$((PORT+1))
done

echo "Starting frontend on http://localhost:$PORT"
serve -s client-build/frontend -l $PORT
