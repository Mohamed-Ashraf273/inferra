#!/bin/bash
set -e

echo "Starting Inferra Application..."

echo "Starting FastAPI backend on port 8000..."
cd /app
python -m uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

sleep 3

echo "Starting frontend server on port 3000..."
cd /app/app/frontend
python -m http.server 3000 &
FRONTEND_PID=$!

echo "========================================="
echo "Inferra Application is running!"
echo "Backend API: http://localhost:8000"
echo "Frontend UI: http://localhost:3000"
echo "========================================="

shutdown() {
    echo "Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID
    exit 0
}

trap shutdown SIGTERM SIGINT

wait $BACKEND_PID $FRONTEND_PID
