#!/usr/bin/env python3
"""
L10 Dashboard Stats Generator

Pulls weekly client stats from Slack #client-stats threads and client metadata
from Airtable Accounts table. Writes a stats.json file for the L10 dashboard.

Runs every Monday at 9:30am Pacific before the 10am L10 meeting.

Usage:
    python3 scripts/generate_l10_stats.py
    python3 scripts/generate_l10_stats.py --week 2026-03-23  # specific week
"""

import json
import os
import re
import sys
import time
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote
from urllib.error import HTTPError

# --- Configuration ---

SLACK_CHANNEL_ID = "C0516U9417H"  # #client-stats
AIRTABLE_BASE_ID = "app0MXWD2LKazuQo1"
AIRTABLE_ACCOUNTS_TABLE = "tblzYMsrs3gSpmflP"
OUTPUT_DIR = Path(__file__).parent.parent / "l10-dashboard"
OUTPUT_FILE = OUTPUT_DIR / "stats.json"

# --- Token Loading ---

def get_slack_token():
    env_path = Path.home() / "Anissa's Repo" / "natasha-bot" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("SLACK_BOT_TOKEN="):
                return line.split("=", 1)[1].strip()
    return os.environ.get("SLACK_BOT_TOKEN", "")


def get_airtable_token():
    mcp_path = Path.home() / ".claude" / "mcp.json"
    if mcp_path.exists():
        config = json.loads(mcp_path.read_text())
        auth = config.get("mcpServers", {}).get("airtable", {}).get("headers", {}).get("Authorization", "")
        if auth.startswith("Bearer "):
            return auth[7:]
    return os.environ.get("AIRTABLE_TOKEN", "")


# --- API Helpers ---

def slack_api(method, params=None):
    token = get_slack_token()
    if not token:
        raise RuntimeError("No Slack bot token found")
    url = f"https://slack.com/api/{method}"
    if params:
        url += "?" + urlencode(params)
    req = Request(url, headers={"Authorization": f"Bearer {token}"})
    with urlopen(req) as resp:
        data = json.loads(resp.read())
    if not data.get("ok"):
        raise RuntimeError(f"Slack API error: {data.get('error', 'unknown')}")
    return data


def airtable_api(table_id, params=None):
    token = get_airtable_token()
    if not token:
        raise RuntimeError("No Airtable token found")
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{table_id}"
    if params:
        url += "?" + urlencode(params, doseq=True, quote_via=quote)
    req = Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urlopen(req) as resp:
            data = json.loads(resp.read())
    except HTTPError as e:
        body = e.read().decode() if e.fp else ""
        raise RuntimeError(f"Airtable API error {e.code}: {body}") from e
    return data


# --- Week Range ---

def get_week_range(week_date_str=None):
    if week_date_str:
        target = datetime.strptime(week_date_str, "%Y-%m-%d")
    else:
        target = datetime.now()

    days_since_monday = target.weekday()
    if days_since_monday == 0:
        monday = target
    else:
        monday = target - timedelta(days=days_since_monday)

    sunday = monday - timedelta(days=1)
    search_start = datetime(sunday.year, sunday.month, sunday.day, 0, 0, 0)
    search_end = datetime(monday.year, monday.month, monday.day, 23, 59, 59)

    return monday, search_start.timestamp(), search_end.timestamp()


# --- Slack Data ---

def fetch_weekly_messages(search_start, search_end):
    messages = []
    cursor = None
    while True:
        params = {
            "channel": SLACK_CHANNEL_ID,
            "oldest": str(search_start),
            "latest": str(search_end),
            "limit": 100,
        }
        if cursor:
            params["cursor"] = cursor
        data = slack_api("conversations.history", params)
        messages.extend(data.get("messages", []))
        cursor = data.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break
    return messages


def fetch_thread_replies(thread_ts):
    params = {
        "channel": SLACK_CHANNEL_ID,
        "ts": thread_ts,
        "limit": 100,
    }
    data = slack_api("conversations.replies", params)
    return data.get("messages", [])


# --- Parsing ---

def extract_client_name(text):
    patterns = [
        r"Client:\s*(.+?)(?:\n|$)",
        r"^\*(.+?)\s*-\s*\d+/\d+/\d+\*",
    ]
    for p in patterns:
        m = re.search(p, text, re.MULTILINE)
        if m:
            name = m.group(1).strip().rstrip("*").strip()
            name = re.sub(r"[*_~`]", "", name)
            return name
    return None


def parse_revenue(text):
    revenue = {}
    m = re.search(r"Current Month(?:\s+Revenue)?:\s*\`?\$?([\d,]+(?:\.\d+)?)\`?", text)
    if m:
        revenue["monthly"] = float(m.group(1).replace(",", ""))
    m = re.search(r"Total Revenue(?:\s+Influenced)?:\s*\`?\$?([\d,]+(?:\.\d+)?)\`?", text)
    if m:
        revenue["total"] = float(m.group(1).replace(",", ""))
    cash_patterns = [
        r"Cash Collected.*?:\s*\`?\$?([\d,]+(?:\.\d+)?)\`?",
        r"Revenue:\s*\`?\$?([\d,]+(?:\.\d+)?)\`?\s*\(\s*Target",
    ]
    cash_amounts = []
    for p in cash_patterns:
        for m in re.finditer(p, text):
            try:
                cash_amounts.append(float(m.group(1).replace(",", "")))
            except ValueError:
                pass
    if cash_amounts and "monthly" not in revenue:
        revenue["weekly_cash"] = sum(cash_amounts)
    week_rev_patterns = [
        r"\(\$?([\d,]+(?:\.\d+)?)\s*this week\)",
        r"this week.*?\$?([\d,]+(?:\.\d+)?)",
    ]
    weekly_total = 0
    for p in week_rev_patterns:
        for m in re.finditer(p, text, re.IGNORECASE):
            try:
                weekly_total += float(m.group(1).replace(",", ""))
            except ValueError:
                pass
    if weekly_total > 0:
        revenue["weekly"] = weekly_total
    return revenue


def parse_roi(text):
    m = re.search(r"ROI:\s*\`?([\d.]+)x\`?", text)
    if m:
        return float(m.group(1))
    return None


def parse_emails(text):
    emails = {}
    m = re.search(r"New Emails?\s+(?:this week|Captured).*?:\s*\`?([\d,]+)\`?", text)
    if m:
        try:
            emails["new_weekly"] = int(m.group(1).replace(",", ""))
        except ValueError:
            pass
    m = re.search(r"New Email Ratio:\s*\`?(\d+)%\`?", text)
    if m:
        emails["new_ratio"] = int(m.group(1))
    total_captured = 0
    for m in re.finditer(r"Emails Captured.*?:\s*\`?([\d,]+)\`?", text):
        try:
            total_captured += int(m.group(1).replace(",", ""))
        except ValueError:
            pass
    if total_captured > 0:
        emails["total_captured_weekly"] = total_captured
    return emails


def parse_optins(text):
    total = 0
    for m in re.finditer(r"Opt-ins:\s*\`?([\d,]+)\`?", text):
        try:
            total += int(m.group(1).replace(",", ""))
        except ValueError:
            pass
    return total if total > 0 else None


def slack_to_html(text):
    if not text:
        return ""
    text = re.sub(r"\*(.+?)\*", r"<strong>\1</strong>", text)
    text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"<(https?://[^|>]+)\|([^>]+)>", r'<a href="\1" target="_blank">\2</a>', text)
    text = re.sub(r"<(https?://[^>]+)>", r'<a href="\1" target="_blank">\1</a>', text)
    text = re.sub(r"<@[A-Z0-9]+>", "", text)
    text = re.sub(r":[a-z_]+:", "", text)
    text = text.replace("\n", "<br>")
    text = re.sub(r"•\s*", "&#8226; ", text)
    text = re.sub(r"◦\s*", "&nbsp;&nbsp;&#9702; ", text)
    text = re.sub(r"▪︎\s*", "&nbsp;&nbsp;&nbsp;&nbsp;&#9642; ", text)
    return text


# --- Airtable ---

def fetch_airtable_accounts():
    fields = [
        "Account", "Active Client Stage", "MRR", "On Track",
        "Months As Active Client",
    ]
    params = [("filterByFormula", "NOT({Active Client Stage}='')")]
    for f in fields:
        params.append(("fields[]", f))

    data = airtable_api(AIRTABLE_ACCOUNTS_TABLE, params)
    accounts = {}
    for rec in data.get("records", []):
        f = rec["fields"]
        name = f.get("Account", "")
        if name:
            months = f.get("Months As Active Client", 0)
            if isinstance(months, dict):
                months = 0
            accounts[name] = {
                "id": rec["id"],
                "stage": f.get("Active Client Stage", ""),
                "mrr": f.get("MRR", 0),
                "on_track": f.get("On Track", ""),
                "months_active": months,
            }
    return accounts


def match_client_to_account(client_name, accounts):
    client_lower = client_name.lower().strip()
    for acct_name in accounts:
        acct_lower = acct_name.lower().strip()
        if client_lower == acct_lower:
            return acct_name
        if client_lower in acct_lower or acct_lower in client_lower:
            return acct_name
        for part in client_lower.split("/"):
            part = part.strip()
            if part and (part in acct_lower or acct_lower in part):
                return acct_name
        for part in acct_lower.split("/"):
            part = part.strip()
            if part and (part in client_lower or client_lower in part):
                return acct_name
    return None


# --- Processing ---

def process_slack_week(search_start, search_end, accounts, include_html=False):
    """Process one week of Slack stats. Returns dict of client metrics."""
    messages = fetch_weekly_messages(search_start, search_end)
    stat_messages = [
        m for m in messages
        if "Weekly Stats Update" in m.get("text", "") or "Daily Stats Update" in m.get("text", "")
    ]

    clients = {}
    for msg in stat_messages:
        client_name = extract_client_name(msg.get("text", ""))
        if not client_name:
            continue

        thread_ts = msg.get("ts", "")
        replies = fetch_thread_replies(thread_ts)

        full_text = ""
        for reply in replies[1:]:
            reply_text = reply.get("text", "")
            if reply_text and len(reply_text) > 50:
                full_text += reply_text + "\n\n"
        if not full_text:
            full_text = msg.get("text", "")

        revenue = parse_revenue(full_text)
        roi = parse_roi(full_text)
        emails = parse_emails(full_text)
        total_optins = parse_optins(full_text)

        acct_name = match_client_to_account(client_name, accounts)
        acct_data = accounts.get(acct_name, {}) if acct_name else {}

        entry = {
            "name": client_name,
            "airtable_account": acct_name,
            "airtable_data": acct_data,
            "metrics": {
                "revenue": revenue,
                "roi": roi,
                "emails": emails,
                "total_optins": total_optins,
            },
            "posted_by": msg.get("user", ""),
            "posted_at": msg.get("ts", ""),
        }

        if include_html:
            entry["raw_html"] = slack_to_html(full_text)

        clients[client_name] = entry
        time.sleep(0.3)

    return clients


def build_department_summary(clients):
    total_revenue_monthly = 0
    total_revenue_weekly = 0
    total_emails_weekly = 0
    rois = []

    for c in clients.values():
        rev = c["metrics"]["revenue"]
        if rev.get("monthly"):
            total_revenue_monthly += rev["monthly"]
        if rev.get("weekly"):
            total_revenue_weekly += rev["weekly"]
        elif rev.get("weekly_cash"):
            total_revenue_weekly += rev["weekly_cash"]

        emails = c["metrics"]["emails"]
        if emails.get("total_captured_weekly"):
            total_emails_weekly += emails["total_captured_weekly"]
        elif emails.get("new_weekly"):
            total_emails_weekly += emails["new_weekly"]

        roi = c["metrics"]["roi"]
        if roi is not None:
            rois.append(roi)

    return {
        "active_clients": len(clients),
        "total_revenue_monthly": total_revenue_monthly,
        "total_revenue_weekly": total_revenue_weekly,
        "total_emails_weekly": total_emails_weekly,
        "avg_roi": round(sum(rois) / len(rois), 2) if rois else None,
    }


def extract_prev_week_metrics(prev_clients):
    """Extract just the metrics from previous week for comparison."""
    prev = {}
    for name, c in prev_clients.items():
        rev = c["metrics"]["revenue"]
        emails = c["metrics"]["emails"]
        prev[name] = {
            "revenue": rev.get("monthly") or rev.get("weekly") or rev.get("weekly_cash") or 0,
            "roi": c["metrics"]["roi"],
            "emails": emails.get("total_captured_weekly") or emails.get("new_weekly") or 0,
            "optins": c["metrics"]["total_optins"] or 0,
        }
    return prev


def process_week(week_date_str=None):
    """Main processing function."""
    monday, search_start, search_end = get_week_range(week_date_str)
    week_label = monday.strftime("%B %d, %Y")
    week_iso = monday.strftime("%Y-%m-%d")

    print(f"Generating L10 dashboard for week of {week_label}")

    # Fetch Airtable accounts
    accounts = fetch_airtable_accounts()
    print(f"Found {len(accounts)} active accounts in Airtable")

    # Process current week
    print(f"Processing current week...")
    clients = process_slack_week(search_start, search_end, accounts, include_html=True)
    print(f"Processed {len(clients)} clients for current week")

    # Process previous week for comparison
    prev_monday = monday - timedelta(days=7)
    _, prev_start, prev_end = get_week_range(prev_monday.strftime("%Y-%m-%d"))
    print(f"Processing previous week ({prev_monday.strftime('%B %d')})...")
    prev_clients = process_slack_week(prev_start, prev_end, accounts, include_html=False)
    prev_metrics = extract_prev_week_metrics(prev_clients)
    print(f"Processed {len(prev_clients)} clients for previous week")

    # Attach previous week data to each client
    for name, c in clients.items():
        c["prev_week"] = prev_metrics.get(name, {})

    # Build output
    output = {
        "generated_at": datetime.now().isoformat(),
        "week_of": week_iso,
        "week_label": week_label,
        "prev_week_of": prev_monday.strftime("%Y-%m-%d"),
        "total_clients": len(clients),
        "department_summary": build_department_summary(clients),
        "prev_department_summary": build_department_summary(prev_clients),
        "clients": clients,
        "targets": {
            "roi": 2.0,
            "weekly_revenue_per_client": 4615,
            "weekly_email_subs": 1250,
        },
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(output, indent=2, default=str))
    print(f"Wrote {OUTPUT_FILE}")
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate L10 dashboard stats")
    parser.add_argument("--week", help="Week date (YYYY-MM-DD, should be a Monday)", default=None)
    args = parser.parse_args()

    try:
        process_week(args.week)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
