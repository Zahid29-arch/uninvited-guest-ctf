#!/usr/bin/env bash
# ==============================================================================
# Script: verify_network_isolation.sh
# Member 1: Deployment & Platform Architecture (IT24103264)
# Description: Verifies network segmentation, port bindings, and security controls.
# ==============================================================================
set -euo pipefail

echo "=========================================================="
echo "  🔍 Security Controls & Network Isolation Audit"
echo "  👤 Architecture & Deployment: IT24103264 (Member 1)"
echo "=========================================================="

echo "[*] Auditing exposed listening ports..."
for port in 8000 3000 8086; do
    if netstat -tuln 2>/dev/null | grep -q ":${port} " || ss -tuln 2>/dev/null | grep -q ":${port} "; then
        echo "  [+] Port ${port} is active and properly listening."
    else
        echo "  [-] Warning: Port ${port} is not listening."
    fi
done

echo "[*] Checking Docker bridge isolation (uninvited_net)..."
if docker network inspect uninvited_net >/dev/null 2>&1; then
    SUBNET=$(docker network inspect uninvited_net -f '{{(index .IPAM.Config 0).Subnet}}')
    echo "  [+] Network uninvited_net confirmed with subnet: ${SUBNET}"
else
    echo "  [-] Network uninvited_net not found."
fi

echo "[*] Audit complete."
