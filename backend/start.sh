#!/bin/bash

# Exit on error
set -e

echo "Initializing Database..."
# Run the script to ensure Super Admin exists and database is populated
python3 set_super_admin.py

echo "Starting Gunicorn Server..."
# Use gunicorn with uvicorn workers for production performance
# Workers = 2-4 per core is typical. We'll start with 2 for the free/starter tier to save RAM.
exec gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
