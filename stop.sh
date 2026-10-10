#!/usr/bin/env bash
# ==============================================================================
# Script: stop.sh
# Member 1: Deployment & Platform Architecture (IT24103264)
# Description: Graceful shutdown and resource teardown engine.
# ==============================================================================
set -euo pipefail

echo "=========================================================="
echo "  🛑 Stopping Operation Uninvited Guest CTF Services..."
echo "  👤 Architecture & Deployment: IT24103264 (Member 1)"
echo "=========================================================="

docker compose down

echo "[+] All containers safely stopped and network resources released."
