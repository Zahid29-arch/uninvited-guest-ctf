#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DB_PATH="$DIR/platform/ctfd-data/ctfd.db"

function banner() {
    echo "=========================================================="
    echo "  🛡️  Operation Uninvited Guest — CTF Reset Manager"
    echo "=========================================================="
}

function reset_all() {
    echo "[+] Resetting entire CTF environment..."
    
    # 1. Clear solves, submissions, awards, and tracking from CTFd
    python3 - <<EOF
import sqlite3
conn = sqlite3.connect("$DB_PATH")
c = conn.cursor()
c.execute("DELETE FROM solves")
c.execute("DELETE FROM submissions")
c.execute("DELETE FROM tracking")
c.execute("DELETE FROM awards")
c.execute("DELETE FROM unlocks")
conn.commit()
conn.close()
print("    ✓ Cleared all solves, submissions, and scoring history from CTFd.")
EOF

    # 2. Restart platform containers
    echo "[+] Restarting all platform containers to clean state..."
    cd "$DIR"
    docker compose restart ctfd juice-shop exchange-portal
    
    echo ""
    echo "=========================================================="
    echo "  ✅ Entire CTF has been reset successfully!"
    echo "  - All challenge stages are now back to locked state"
    echo "  - Stage 1 is open and ready for solving"
    echo "  - Services are running and healthy"
    echo "=========================================================="
}

function reset_stage() {
    STAGE_NUM=$1
    if [[ ! "$STAGE_NUM" =~ ^[1-6]$ ]]; then
        echo "[-] Invalid stage number '$STAGE_NUM'. Must be between 1 and 6."
        exit 1
    fi

    echo "[+] Resetting Stage $STAGE_NUM (and dependent stages >= $STAGE_NUM)..."

    python3 - <<EOF
import sqlite3
conn = sqlite3.connect("$DB_PATH")
c = conn.cursor()
stage = int("$STAGE_NUM")
# Clear this stage and all subsequent stages that depend on it
for sid in range(stage, 7):
    c.execute("DELETE FROM solves WHERE challenge_id = ?", (sid,))
    c.execute("DELETE FROM submissions WHERE challenge_id = ?", (sid,))
conn.commit()
conn.close()
print(f"    ✓ Removed solves and submissions for Stage(s) {stage} through 6.")
EOF

    cd "$DIR"
    if [[ "$STAGE_NUM" -le 2 ]]; then
        echo "[+] Restarting Juice Shop container..."
        docker compose restart juice-shop
    fi
    if [[ "$STAGE_NUM" -le 6 ]]; then
        echo "[+] Restarting Exchange Portal..."
        docker compose restart exchange-portal
    fi
    echo "[+] Restarting CTFd to refresh challenge state..."
    docker compose restart ctfd

    echo ""
    echo "=========================================================="
    echo "  ✅ Stage $STAGE_NUM has been reset successfully!"
    echo "=========================================================="
}

function reset_player() {
    PLAYER_NAME=$1
    if [[ -z "$PLAYER_NAME" ]]; then
        echo "[-] Please provide a username or team name."
        exit 1
    fi

    python3 - <<EOF
import sqlite3
conn = sqlite3.connect("$DB_PATH")
c = conn.cursor()
pname = "$PLAYER_NAME"

user = c.execute("SELECT id, account_id FROM users WHERE name = ?", (pname,)).fetchone()
team = c.execute("SELECT id FROM teams WHERE name = ?", (pname,)).fetchone()

account_ids = []
if user:
    account_ids.append(user[1] if user[1] else user[0])
if team:
    account_ids.append(team[0])

if not account_ids:
    print(f"[-] No user or team found with name '{pname}'.")
else:
    for aid in set(account_ids):
        c.execute("DELETE FROM solves WHERE account_id = ?", (aid,))
        c.execute("DELETE FROM submissions WHERE account_id = ?", (aid,))
    conn.commit()
    print(f"    ✓ Cleared all progress for '{pname}'.")
conn.close()
EOF
    cd "$DIR"
    docker compose restart ctfd
}

# Command line parsing
if [[ "$1" == "all" ]]; then
    banner
    reset_all
    exit 0
elif [[ "$1" == "stage" ]]; then
    banner
    reset_stage "$2"
    exit 0
elif [[ "$1" == "player" ]]; then
    banner
    reset_player "$2"
    exit 0
elif [[ -n "$1" ]]; then
    banner
    echo "Usage:"
    echo "  ./reset.sh             (Interactive menu)"
    echo "  ./reset.sh all         (Reset entire CTF)"
    echo "  ./reset.sh stage <1-6> (Reset specific stage)"
    echo "  ./reset.sh player <name> (Reset specific player/team)"
    exit 1
fi

# Interactive menu
banner
echo "Select an option to reset:"
echo "  1) Reset Entire CTF (Solves, scores, container state)"
echo "  2) Reset Stage 1 (Find the Uninvited Guest)"
echo "  3) Reset Stage 2 (Front Door / Juice Shop)"
echo "  4) Reset Stage 3 (Locked Evidence / Crypto)"
echo "  5) Reset Stage 4 (Follow the Clicks / Forensics)"
echo "  6) Reset Stage 5 (Hidden in Plain Sight / Stego)"
echo "  7) Reset Stage 6 (Unmasking / Exchange Portal)"
echo "  8) Exit"
echo ""
read -rp "Enter choice [1-8]: " choice

case "$choice" in
    1) reset_all ;;
    2) reset_stage 1 ;;
    3) reset_stage 2 ;;
    4) reset_stage 3 ;;
    5) reset_stage 4 ;;
    6) reset_stage 5 ;;
    7) reset_stage 6 ;;
    *) echo "Exiting." ; exit 0 ;;
esac
