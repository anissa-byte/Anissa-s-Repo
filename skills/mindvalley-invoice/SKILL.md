---
name: mindvalley-invoice
description: >
  Generates the Mindvalley invoice PDF for the current billing cycle,
  creates a Gmail draft to finance@mindvalley.com with the PDF attached,
  and sends a Slack DM reminder. Trigger every 28 days on billing reminder day.
---

# Mindvalley Invoice Skill

## When to use this skill
Run this skill whenever Anissa says anything like:
- "Run the Mindvalley invoice"
- "Generate the Mindvalley invoice"
- "It's invoice day"
- "Create the Mindvalley draft"

---

## What this skill does
1. Calculates the correct invoice number, issue date, and due date for the current cycle
2. Generates a pixel-perfect PDF invoice matching the SOB invoice template
3. Creates a Gmail draft to `finance@mindvalley.com` with the PDF attached
4. Sends Anissa a Slack DM: "Your Mindvalley invoice draft is ready — go check Gmail drafts."

---

## Billing cycle reference

| Field | Value |
|---|---|
| Anchor invoice | GYDHNDN3-0004 |
| Anchor due date | March 2, 2026 |
| Cycle length | 28 days |
| Lead time | 12 days (invoice issued 12 days before due date) |
| Client | Mindvalley Inc — finance@mindvalley.com |
| Amount | US$13,000.00 |
| Line item | DM Funnel System |

---

## Step-by-step instructions for Claude

### Step 1 — Generate the PDF

Run the following Python script using bash_tool. It auto-calculates all dates and the invoice number from today's date.

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from datetime import date, timedelta
import math

ANCHOR_DUE    = date(2026, 3, 2)
ANCHOR_NUM    = 4
CYCLE_DAYS    = 28
LEAD_DAYS     = 12
INVOICE_PREFIX = "GYDHNDN3-"

def get_cycle_for_date(today: date):
    delta = (today - ANCHOR_DUE).days
    cycles_elapsed = math.ceil(delta / CYCLE_DAYS) if delta > 0 else 0
    cycle_num = ANCHOR_NUM + cycles_elapsed
    due_date  = ANCHOR_DUE + timedelta(days=cycles_elapsed * CYCLE_DAYS)
    if today > due_date:
        cycles_elapsed += 1
        cycle_num += 1
        due_date = ANCHOR_DUE + timedelta(days=cycles_elapsed * CYCLE_DAYS)
    issue_date = due_date - timedelta(days=LEAD_DAYS)
    invoice_number = f"{INVOICE_PREFIX}{cycle_num:04d}"
    return invoice_number, issue_date, due_date

def draw_invoice(output_path, invoice_number, issue_date, due_date):
    W, H = letter
    c = canvas.Canvas(output_path, pagesize=letter)
    NAVY = colors.HexColor("#1B1F3B")
    GOLD = colors.HexColor("#F5A623")

    # Header bar
    c.setFillColor(NAVY)
    c.rect(0, H - 80, W, 80, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, H - 48, "SCHOOL")
    c.setFont("Helvetica", 11)
    c.drawString(40, H - 62, "OF BOTS")
    c.setFillColor(GOLD)
    c.rect(W - 70, H - 65, 38, 38, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 7)
    c.drawString(W - 63, H - 44, "SCHOOL")
    c.setFont("Helvetica", 6)
    c.drawString(W - 60, H - 53, "OF BOTS")

    # Invoice title
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(40, H - 120, "Invoice")

    # Meta
    labels = ["Invoice number", "Date of issue", "Date due"]
    values = [invoice_number, issue_date.strftime("%B %-d, %Y"), due_date.strftime("%B %-d, %Y")]
    y = H - 145
    for lbl, val in zip(labels, values):
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(40, y, lbl)
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.black)
        c.drawString(155, y, val)
        y -= 16

    # From
    y = H - 145
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(NAVY)
    c.drawString(280, y, "School of Bots")
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.black)
    for line in ["+1 949-899-6343", "support@schoolofbots.co"]:
        y -= 14
        c.drawString(280, y, line)

    # Bill to
    y_bill = H - 145
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(NAVY)
    c.drawString(420, y_bill, "Bill to")
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.black)
    for line in ["Mindvalley Inc", "407 California Avenue", "Suite #2",
                 "Palo Alto, California 94306", "United States", "finance@mindvalley.com"]:
        y_bill -= 14
        c.drawString(420, y_bill, line)

    # Amount due banner
    banner_y = H - 295
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(NAVY)
    c.drawString(40, banner_y, f"US$13,000.00 due {due_date.strftime('%B %-d, %Y')}")
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#1155CC"))
    c.drawString(40, banner_y - 18, "Pay online")

    # Table
    table_y = banner_y - 55
    col_headers = ["Description", "Qty", "Unit price", "Amount"]
    col_data    = ["DM Funnel System", "1", "US$13,000.00", "US$13,000.00"]
    col_widths  = [280, 50, 100, 100]
    table_w     = sum(col_widths)
    c.setFillColor(colors.HexColor("#F2F2F2"))
    c.rect(40, table_y - 2, table_w, 18, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#555555"))
    c.setFont("Helvetica", 8)
    x = 40
    for i, h in enumerate(col_headers):
        if i == 0:
            c.drawString(x + 4, table_y + 4, h)
        else:
            c.drawRightString(x + col_widths[i] - 4, table_y + 4, h)
        x += col_widths[i]
    c.setStrokeColor(colors.HexColor("#DDDDDD"))
    c.setLineWidth(0.5)
    c.line(40, table_y - 2, 40 + table_w, table_y - 2)
    row_y = table_y - 22
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)
    x = 40
    for i, val in enumerate(col_data):
        if i == 0:
            c.drawString(x + 4, row_y, val)
        else:
            c.drawRightString(x + col_widths[i] - 4, row_y, val)
        x += col_widths[i]
    c.line(40, row_y - 8, 40 + table_w, row_y - 8)
    right_x = 40 + table_w - 4
    totals_y = row_y - 22
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.black)
    for label, val in [("Subtotal", "US$13,000.00"), ("Total", "US$13,000.00")]:
        c.drawRightString(right_x - 110, totals_y, label)
        c.drawRightString(right_x, totals_y, val)
        totals_y -= 14
    c.setLineWidth(0.5)
    c.line(40 + table_w - 210, totals_y - 4, 40 + table_w, totals_y - 4)
    totals_y -= 18
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(right_x - 110, totals_y, "Amount due")
    c.drawRightString(right_x, totals_y, "US$13,000.00")

    # Bank transfer
    bank_y = totals_y - 55
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(NAVY)
    c.drawString(40, bank_y, "Pay US$13,000.00 with a bank transfer")
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.black)
    c.drawString(40, bank_y - 14, "Bank transfers can take up to two business days. To pay via bank transfer,")
    c.drawString(40, bank_y - 26, "transfer funds using the following bank information.")
    detail_y = bank_y - 46
    for lbl, val in [("Bank name", "Wells Fargo"), ("Routing number", "121000248"),
                     ("Account number", "40630281440097299"), ("SWIFT code", "WFBIUS6SXXX"),
                     ("Reference", invoice_number)]:
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(NAVY)
        c.drawString(40, detail_y, lbl)
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.black)
        c.drawString(155, detail_y, val)
        detail_y -= 14

    # Footer
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.line(40, 45, W - 40, 45)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#888888"))
    c.drawRightString(W - 40, 32, "Page 1 of 1")
    c.save()

today = date.today()
invoice_number, issue_date, due_date = get_cycle_for_date(today)
safe_num = invoice_number.replace("/", "-")
output_path = f"/tmp/Invoice-{safe_num}.pdf"
draw_invoice(output_path, invoice_number, issue_date, due_date)
print(f"PDF_PATH={output_path}")
print(f"INVOICE_NUMBER={invoice_number}")
print(f"DUE_DATE={due_date.strftime('%B %-d, %Y')}")
```

Capture the output values: `PDF_PATH`, `INVOICE_NUMBER`, `DUE_DATE`.

---

### Step 2 — Create the Gmail draft

Use the Gmail MCP tool (`Gmail:gmail_create_draft`) to create the draft.

**To:** finance@mindvalley.com  
**Subject:** Invoice {INVOICE_NUMBER} — School of Bots DM Funnel System  
**Body template:**

```
Hi [Mindvalley Finance Team],

Please find attached invoice {INVOICE_NUMBER} for DM Funnel System services.

Invoice details:
• Invoice number: {INVOICE_NUMBER}
• Amount due: US$13,000.00
• Due date: {DUE_DATE}

Payment can be made via bank transfer using the details on the invoice, or online via the link included.

Please don't hesitate to reach out if you have any questions.

Best,
School of Bots
support@schoolofbots.co
+1 949-899-6343
```

Attach the PDF file at `PDF_PATH` to the draft.

---

### Step 3 — Send Slack DM to Anissa

Use the Slack MCP tool (`Slack:slack_send_message`) to send a DM to Anissa.

**Channel/recipient:** Anissa's Slack handle  
**Message:**
```
🧾 Your Mindvalley invoice draft is ready — go check your Gmail drafts.

Invoice {INVOICE_NUMBER} | Due {DUE_DATE} | $13,000.00
```

---

### Step 4 — Confirm to Anissa

After all three steps, confirm in the chat:
> "Done. Invoice {INVOICE_NUMBER} (due {DUE_DATE}) has been generated, drafted in Gmail, and I sent you a Slack reminder. Just review and hit send when ready."

---

## Important constants (never change without instruction)

| Field | Value |
|---|---|
| Client name | Mindvalley Inc |
| Bill to address | 407 California Avenue, Suite #2, Palo Alto, CA 94306 |
| Finance email | finance@mindvalley.com |
| Amount | US$13,000.00 (fixed, do not change) |
| Line item description | DM Funnel System |
| Bank | Wells Fargo |
| Routing | 121000248 |
| Account | 40630281440097299 |
| SWIFT | WFBIUS6SXXX |
| SOB phone | +1 949-899-6343 |
| SOB support email | support@schoolofbots.co |

---

## Error handling

- If PDF generation fails: Surface the Python error to Anissa immediately, do not attempt to continue.
- If Gmail draft creation fails: Still send the Slack notification but flag that the Gmail draft failed and include the invoice number so Anissa can manually create it.
- If Slack fails: Confirm in Claude chat that the PDF and draft were created successfully.
