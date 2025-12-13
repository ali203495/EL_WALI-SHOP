#!/bin/bash

# Kill running servers on port 8000 and 3000 to clear state
fuser -k 8000/tcp
fuser -k 3000/tcp

# Start Backend
echo "Starting Backend..."
cd backend
# Use the absolute path to venv python to be safe
./venv/bin/uvicorn main:app --reload --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend started with PID $BACKEND_PID"
cd ..

# Start Frontend
echo "Starting Frontend..."
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend started with PID $FRONTEND_PID"
cd ..

echo "Servers are starting..."
echo "Backend logs: tail -f backend.log"
echo "Frontend logs: tail -f frontend.log"
