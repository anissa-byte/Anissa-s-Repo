#!/bin/bash
# Refresh L10 Dashboard Stats
# Runs every Monday at 9:30am Pacific before the 10am L10 meeting.
#
# What it does:
#   1. Pulls latest stats from Slack #client-stats
#   2. Pulls client metadata from Airtable Accounts
#   3. Generates stats.json for the dashboard
#   4. Commits and pushes so the live dashboard updates
#
# Usage:
#   ./scripts/refresh_l10_dashboard.sh
#   ./scripts/refresh_l10_dashboard.sh 2026-03-23  # specific week

set -e

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_DIR"

WEEK_ARG=""
if [ -n "$1" ]; then
    WEEK_ARG="--week $1"
fi

echo "$(date): Starting L10 dashboard refresh..."

# Generate stats
python3 scripts/generate_l10_stats.py $WEEK_ARG

# Check if stats.json changed
if git diff --quiet l10-dashboard/stats.json 2>/dev/null; then
    echo "$(date): No changes to stats.json"
else
    echo "$(date): Stats updated, committing..."
    git add l10-dashboard/stats.json
    git commit -m "Auto-update L10 dashboard stats — $(date '+%Y-%m-%d')"
    git push origin main
    echo "$(date): Pushed to origin/main"
fi

echo "$(date): L10 dashboard refresh complete"
