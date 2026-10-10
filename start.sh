#!/usr/bin/env bash
set -e

echo "=============================================="
echo " Starting Uninvited Guest CTF Environment"
echo "=============================================="

# Fix permissions on all platform and stage assets for non-root containers (CTFd & Juice Shop)
chmod -R 777 platform stages 2>/dev/null || true

# Start containers via Docker Compose
docker compose up -d --build

echo ""
echo "=============================================="
echo " CTF Services Started Successfully!"
echo " - CTFd Platform:       http://localhost:8000"
echo " - OWASP Juice Shop:    http://localhost:3000"
echo " - The Exchange Portal: http://localhost:8086"
echo "=============================================="
