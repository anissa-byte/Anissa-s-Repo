---
name: sob-webpage-generator
description: >
  Generates a branded, self-contained HTML web page from raw pasted content.
  Use this skill any time the user wants to turn content into a shareable or 
  embeddable web page — client-facing guides, internal policy docs, onboarding 
  pages, quick-reference sheets, SOPs, or any structured communication. Trigger 
  whenever the user says things like "make this into a page", "create a web doc", 
  "turn this into something shareable", "build a client-facing guide", "make this 
  look professional", or "put this in a page." Always use this skill for any HTML 
  output that should match SOB's brand.
---

# SOB Branded Web Page Generator

## Purpose
Convert raw pasted content into a polished, on-brand HTML page. The audience is
almost always busy CEOs or executive decision-makers. Every output must prioritize:
visual clarity, brevity, authority, and forward momentum. These are informational 
pages — no CTAs, no sales language, no calls to action.

---

## Brand System

### Color Palette
- **Background:** `#0A0A0A` (near-black) — always dark
- **Primary accent:** `#FFBD4A` (SOB yellow-orange)
- **Text:** `#FFFFFF` (primary), `#AAAAAA` (secondary/supporting)
- **Card backgrounds:** `#141414` or `#1A1A1A`
- **Borders:** `#FFBD4A` or `#2A2A2A` (subtle)

### Typography
- Font stack: `'Inter', system-ui, -apple-system, sans-serif` (load Inter from Google Fonts)
- Headlines: Bold, uppercase or title-case, generous tracking
- Body: 16–18px, line-height 1.6
- Stat callouts: 48–72px, orange, bold — these are hero elements
- Labels / eyebrows: 11–12px uppercase, letter-spacing 0.1em, `#FFBD4A`

### Logo Treatment
Use the text logo in the top-left of every page:
```html
<span class="logo">SCHOOL OF <span style="color:#FFBD4A">BOTS</span></span>
```
No image, no external asset — text only.

### Visual Language
- Pull out any numbers, outcomes, or stats and make them large orange callouts
- Use icon-driven lists (Unicode emoji or simple SVG icons — no external libraries)
- Orange divider lines between major sections
- Cards/tiles for grouped info: dark card background + subtle orange left-border — use a **2-column grid** (2x2 for 4 items, 2x3 for 6, etc.) so each card has room to breathe. Never put 4 cards in a single row.
- Numbered visual steps for sequential content
- Minimize prose — convert paragraphs to scannable bullets or visual blocks
- No walls of text under any circumstances

---

## Voice & Tone
- **Authority without arrogance:** We've done this before. We know what works.
- **Low friction:** Confident, clear, no hedging. "Here's what to do" not "you might want to consider..."
- **Results-first:** Lead with outcomes, support with process
- **Warm but direct:** Conversational but never casual. Never cold or corporate.
- **No filler:** Remove "just," "simply," "basically," "very," "really"
- **Short sentences:** Natasha's pattern — punchy, outcome-first, "we've got it" energy
- **No CTAs:** These pages inform. They do not sell. End on information, not action.

---

## Page Types

### 1. Client-Facing Guide
*When: Sharing process, strategy, or education with a client.*

Structure:
1. Header — page title + one-line purpose statement
2. Key concepts — visual cards or icon list
3. Process steps — numbered visual sequence (if sequential)
4. Summary or "what this means for you" block (plain language, no CTA)

### 2. Internal Policy / SOP
*When: Documenting team process or decision framework.*

Structure:
1. Title + one-line scope statement
2. Rules or criteria — scannable bullet list
3. Decision logic — table or simple flowchart (CSS/ASCII)
4. Edge cases or examples — card format

### 3. Quick Reference Sheet
*When: Condensing heavy content into a CEO-ready summary.*

Structure:
1. Stats or outcomes hero — large orange numbers front and center
2. 3–5 core concepts — tiles or cards
3. One "so what" callout box — bold, brief, plain language

### 4. Welcome / Onboarding Page
*When: Introducing a client to SOB, a service, or a new phase of work.*

Structure:
1. Warm header — client name, what this page is
2. What to expect — timeline or phases as visual steps
3. Your team — names and roles
4. Reference info — links, contacts, relevant docs (no CTA)

---

## Content Transformation Rules

| If content contains... | Transform it into... |
|---|---|
| A long explanatory paragraph | 3–5 bullet points + a bold lead sentence |
| A numbered list of 5+ items | Icon grid or two-column card layout |
| A specific number or stat | Large orange callout, pulled out of body text |
| A sequential process | Numbered visual steps with brief labels |
| A decision or rule | Bold rule statement + supporting detail beneath |
| A quote from Natasha or a client | Styled blockquote with orange left border |
| Dense process description | Summary table or flowchart |

**Default:** When in doubt, compress. Less is always more.

---

## Output Requirements

1. **Single self-contained HTML file** — all CSS in `<style>` tag, no external dependencies except Google Fonts
2. **Mobile-responsive** — flexbox/grid, tested mentally at 375px and 1200px
3. **Dark background always** — `#0A0A0A`, white text, orange accents
4. **No lorem ipsum** — every word comes from the provided content
5. **No CTAs** — informational only; pages end on information, not prompts to act
6. **Logo text treatment** at top of every page (see Logo Treatment above)
7. **Visual-first rendering** — if something can be a stat, icon list, or card instead of a sentence, make it that

---

## Step-by-Step Execution

1. Read the pasted content in full
2. Identify the page type from the four options above
3. Extract and flag: key outcomes, stats, steps, rules, people/roles, any quotes
4. Map extracted content to the appropriate page type structure
5. Write compressed, on-brand copy — rewrite paragraphs as bullets, pull out stats
6. Build the full HTML with inline styles (no class-based external CSS)
7. Save to `./[descriptive-slug].html` in the current working directory
8. Present the file to the user

---

## HTML Shell Reference

Use this as your base. Expand sections as needed.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[PAGE TITLE]</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: #0A0A0A;
      color: #FFFFFF;
      font-family: 'Inter', system-ui, sans-serif;
      font-size: 17px;
      line-height: 1.65;
      padding: 0;
    }
    .container { max-width: 860px; margin: 0 auto; padding: 48px 24px; }
    .logo { font-size: 13px; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; }
    .eyebrow { font-size: 11px; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; color: #FFBD4A; margin-bottom: 12px; }
    h1 { font-size: clamp(32px, 5vw, 52px); font-weight: 900; line-height: 1.1; margin-bottom: 16px; }
    h2 { font-size: clamp(22px, 3vw, 32px); font-weight: 800; margin-bottom: 12px; }
    h3 { font-size: 18px; font-weight: 700; margin-bottom: 8px; }
    p { color: #CCCCCC; margin-bottom: 16px; }
    .divider { border: none; border-top: 1px solid #FFBD4A; margin: 48px 0; opacity: 0.4; }
    .stat { font-size: clamp(48px, 8vw, 72px); font-weight: 900; color: #FFBD4A; line-height: 1; }
    .card {
      background: #141414;
      border: 1px solid #2A2A2A;
      border-left: 3px solid #FFBD4A;
      border-radius: 8px;
      padding: 24px;
      margin-bottom: 16px;
    }
    .grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
    .step { display: flex; gap: 16px; align-items: flex-start; margin-bottom: 24px; }
    .step-num {
      background: #FFBD4A;
      color: #000;
      font-weight: 900;
      font-size: 14px;
      width: 32px; height: 32px;
      border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0;
    }
    blockquote {
      border-left: 3px solid #FFBD4A;
      padding: 16px 20px;
      background: #141414;
      border-radius: 0 8px 8px 0;
      font-style: italic;
      color: #CCCCCC;
    }
    ul { padding-left: 0; list-style: none; }
    ul li { padding: 8px 0; padding-left: 20px; position: relative; color: #CCCCCC; }
    ul li::before { content: "→"; position: absolute; left: 0; color: #FFBD4A; font-weight: 700; }
    @media (max-width: 600px) { .grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <div class="container">
    <!-- Logo -->
    <div style="margin-bottom: 48px;">
      <span class="logo">SCHOOL OF <span style="color:#FFBD4A">BOTS</span></span>
    </div>

    <!-- Page content goes here -->

  </div>
</body>
</html>
```
