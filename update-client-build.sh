#!/bin/bash
set -e

echo "=== Building Frontend ==="
cd frontend
npm install
npm run build
cd ..

echo "=== Preparing Client Build Folder ==="
CLIENT_BUILD_DIR="client-build"

# Clear previous build
rm -rf $CLIENT_BUILD_DIR
mkdir -p $CLIENT_BUILD_DIR/frontend
mkdir -p $CLIENT_BUILD_DIR/mapping-service

# Copy frontend build
cp -r frontend/build/* $CLIENT_BUILD_DIR/frontend/

# Copy mapping service
cp -r services/mapping-service/* $CLIENT_BUILD_DIR/mapping-service/

# Write requirements.txt if not present
pip freeze > $CLIENT_BUILD_DIR/mapping-service/requirements.txt || echo "Could not write requirements.txt, ensure pip is installed."

echo "=== Writing run-client-build.sh ==="

cat > $CLIENT_BUILD_DIR/run-client-build.sh <<'EOF'
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
EOF

chmod +x $CLIENT_BUILD_DIR/run-client-build.sh

echo "=== Client Build Updated Successfully ==="
echo "You can now run ./client-build/run-client-build.sh to start the app."
