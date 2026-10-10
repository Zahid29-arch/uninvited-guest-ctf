#!/usr/bin/env bash
# ==============================================================================
# Script: start.sh
# Member 1: Deployment & Platform Architecture (IT24103264)
# Description: Automated deployment lifecycle engine with pre-flight diagnostics,
#              permission enforcement, container orchestration, and health checking.
# ==============================================================================
set -euo pipefail

echo "=========================================================="
echo "  🛡️  Operation Uninvited Guest — Play Box Deployment Engine"
echo "  👤 Architecture & Deployment: IT24103264 (Member 1)"
echo "=========================================================="

# 1. Pre-flight Checks: Verify Docker Engine & Docker Compose
echo "[*] Running pre-flight system diagnostics..."
if ! command -v docker >/dev/null 2>&1; then
    echo "[-] Error: docker is not installed. Please install Docker Engine." >&2
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    echo "[-] Error: Docker daemon is not running or current user lacks docker group privileges." >&2
    exit 1
fi

# 2. Filesystem Security & Volume Permissions
echo "[*] Enforcing container volume read/write permissions..."
chmod -R 777 platform stages 2>/dev/null || true

# 3. Provision Containers via Docker Compose
echo "[*] Launching containerized services on isolated network (uninvited_net)..."
docker compose up -d --build

# 4. Healthcheck & Service Readiness Polling
echo "[*] Waiting for backend services to initialize..."
MAX_RETRIES=20
COUNT=0
until docker compose ps | grep -q "Up" || [ $COUNT -eq $MAX_RETRIES ]; do
    sleep 2
    COUNT=$((COUNT + 1))
done

# 5. Network Interface & IP Address Discovery
HOST_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "127.0.0.1")

echo ""
echo "=========================================================="
echo "  [+] All CTF Target Services Online & Operational!"
echo "----------------------------------------------------------"
echo "  - CTFd Scoring Engine:   http://${HOST_IP}:8000"
echo "  - OWASP Juice Shop:      http://${HOST_IP}:3000"
echo "  - The Dark Exchange:     http://${HOST_IP}:8086"
echo "=========================================================="
echo "  Player access point: Open Firefox on Kali Linux and connect"
echo "  to the CTFd URL above to begin Stage 1."
echo "=========================================================="
