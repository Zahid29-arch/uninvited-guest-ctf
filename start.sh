#!/usr/bin/env bash
set -e

echo "=============================================="
echo " Starting Uninvited Guest CTF Environment"
echo "=============================================="

# Fix permissions on CTFd database directory for Docker non-root user (UID 1001)
if [ -d "platform/ctfd-data" ]; then
    chmod -R 777 platform/ctfd-data 2>/dev/null || true
fi

# Start containers via Docker Compose
docker compose up -d --build

echo ""
echo "=============================================="
echo " CTF Services Started Successfully!"
echo " - CTFd Platform:       http://localhost:8000"
echo " - OWASP Juice Shop:    http://localhost:3000"
echo " - The Exchange Portal: http://localhost:8086"
echo "=============================================="
