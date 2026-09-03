#!/bin/bash
set -e

# When Railway mounts a persistent volume (e.g., at /data), it starts empty.
# If SQLITE_DB_PATH points to that volume, we must seed it with our existing data
# so we don't lose the 1,447 conversations and 1,017 analyses.
if [ -n "$SQLITE_DB_PATH" ] && [ "$SQLITE_DB_PATH" != "data/myntra_copilot.db" ]; then
    if [ ! -f "$SQLITE_DB_PATH" ]; then
        echo "Seeding existing database to volume at $SQLITE_DB_PATH..."
        cp data/myntra_copilot.db "$SQLITE_DB_PATH"
        echo "Database seeded successfully."
    else
        echo "Database already exists in volume at $SQLITE_DB_PATH."
    fi
fi

# Start FastAPI using uvicorn, binding to 0.0.0.0 and the dynamically assigned $PORT
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
