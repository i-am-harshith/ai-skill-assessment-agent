#!/bin/zsh

set -euo pipefail

export PATH="/opt/homebrew/bin:$PATH"

PROJECT_ROOT="/Users/harshithkumarmv/Desktop/ai-skill-assessment-agent"
BACKEND_DIR="$PROJECT_ROOT/backend"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

backend_running() {
  lsof -iTCP:8000 -sTCP:LISTEN >/dev/null 2>&1
}

frontend_running() {
  lsof -iTCP:5173 -sTCP:LISTEN >/dev/null 2>&1
}

wait_for_url() {
  local name="$1"
  local url="$2"
  local attempts=45

  for _ in $(seq 1 "$attempts"); do
    if curl -fsS "$url" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done

  echo "$name did not become ready in time."
  return 1
}

start_backend() {
  osascript >/dev/null <<OSA
tell application "Terminal"
  activate
  do script "export PATH=/opt/homebrew/bin:\$PATH; cd $BACKEND_DIR; source .venv/bin/activate; uvicorn app.main:app --reload"
end tell
OSA
}

start_frontend() {
  osascript >/dev/null <<OSA
tell application "Terminal"
  activate
  do script "export PATH=/opt/homebrew/bin:\$PATH; cd $FRONTEND_DIR; npm run dev"
end tell
OSA
}

echo "Checking demo services..."

if [[ ! -d "$BACKEND_DIR/.venv" ]]; then
  echo "Backend virtual environment not found at $BACKEND_DIR/.venv"
  exit 1
fi

if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
  echo "Frontend dependencies are missing at $FRONTEND_DIR/node_modules"
  exit 1
fi

if backend_running; then
  echo "Backend is already running on port 8000."
else
  echo "Starting backend..."
  start_backend
fi

if frontend_running; then
  echo "Frontend is already running on port 5173."
else
  echo "Starting frontend..."
  start_frontend
fi

echo "Waiting for backend..."
wait_for_url "Backend" "http://127.0.0.1:8000/api/health"

echo "Waiting for frontend..."
wait_for_url "Frontend" "http://127.0.0.1:5173"

echo "Opening browser..."
open "http://localhost:5173"

echo "Demo app is ready."
