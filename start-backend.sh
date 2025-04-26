#!/bin/bash
echo "🛡️ Killing any old uvicorn processes..."
killall uvicorn || true
echo "🚀 Starting backend fresh on port 8002..."
uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
echo "🚀 Backend started on port 8002"