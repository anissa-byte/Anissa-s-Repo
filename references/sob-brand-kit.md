# School of Bots Design System

This document outlines the complete design system for School of Bots, providing development patterns (CSS/Tailwind/HTML) for consistent implementation across all properties.

---

## Color Palette

### Primary Colors

| Name | Hex | RGB | Role |
|------|-----|-----|------|
| **Heliotrope** | `#EB55F6` | rgb(235, 85, 246) | Accent, highlights, hover backgrounds |
| **Navy** | `#04005B` | rgb(4, 0, 91) | Most headlines |
| **Ebony** | `#0D0A1B` | rgb(13, 10, 27) | Paragraph / body copy |
| **White Smoke** | `#F8F9FA` | rgb(248, 249, 250) | Page backgrounds |
| **Portage** | `#A59FF7` | rgb(165, 159, 247) | Accents, highlights, hover backgrounds |
| **Texas Rose** | `#FFBD4A` | rgb(255, 189, 74) | Buttons, CTA accents |

### Color Usage

| Color | Primary Use |
|-------|-------------|
| Navy | Headlines (most H1s, H2s) |
| Ebony | Body copy, paragraphs |
| White Smoke | Page/section backgrounds |
| Texas Rose | Primary CTA buttons, key accents |
| Heliotrope | Sparingly — hover states, highlights, gradient accents |
| Portage | Sparingly — hover states, subtle highlights, secondary accents |

### Color Proportion

**~60% White Smoke, ~30% Navy/Ebony, ~10% Texas Rose/Heliotrope/Portage**

### Accessibility

All approved color combinations meet WCAG 4.5:1 minimum contrast ratio for body text.

**Approved Combinations:**
- Navy on White Smoke (headlines)
- Ebony on White Smoke (body text)
- White Smoke on Navy (reversed sections)
- White Smoke on Ebony (reversed sections)
- Texas Rose on Navy (button label on dark bg)
- Texas Rose on Ebony (button label on dark bg)
- Portage on Ebony (accent text on dark bg)

**Use with caution (decorative/large text only):**
- Heliotrope on White Smoke (low contrast — large text or non-text elements only)
- Portage on White Smoke (low contrast — large text or non-text elements only)

---

## Typography

Font files are stored in Drive:
**[Font Downloads](https://drive.google.com/drive/u/0/folders/1SizrBL_xI_Tsv8WKEbZTX4QSU4lFz0dB)**

Font application reference (see page 4):
**[Brand PDF — Font Applications](https://drive.google.com/file/d/1i89TQwpDsojqpFfxmN61nsVdLjTTa2Hk/view?usp=sharing)**

> **Note:** Update CSS font-family values below once font names are confirmed from the Drive folder. Replace `[PRIMARY-FONT]` and `[SECONDARY-FONT]` with actual names.

```css
--sob-font-heading: '[PRIMARY-FONT]', system-ui, sans-serif;
--sob-font-body: '[PRIMARY-FONT]', system-ui, sans-serif;
--sob-font-display: '[SECONDARY-FONT]', Georgia, serif;
```

### Font Size Scale

```css
--sob-text-hero: clamp(3rem, 10vw, 8rem);
--sob-text-7xl: 4.5rem;
--sob-text-6xl: 3.75rem;
--sob-text-5xl: 3rem;
--sob-text-4xl: 2.25rem;
--sob-text-3xl: 1.875rem;
--sob-text-2xl: 1.5rem;
--sob-text-xl: 1.25rem;
--sob-text-base: 1rem;
--sob-text-sm: 0.875rem;
--sob-text-xs: 0.75rem;
--sob-text-2xs: 0.625rem;
```

---

## Logo System

Logo files are stored in Drive:
**[Logo Files](https://drive.google.com/drive/u/2/folders/1-vlDYMrRrtuOaq0WbIp2zP8ss4OYO-Md)**

> Download and place files in `assets/logos/` for local reference.

### Logo Variant Usage

| Variant | Use Case |
|---------|----------|
| Symbol Only | Tight spaces — social avatars, app icons, watermarks, favicons |
| Logotype Only | Marketing materials, signage, broader applications |
| Combination Mark | High-visibility moments — campaign headers, co-branding, hero sections |

### Logo Color Versions

| Version | Use On |
|---------|--------|
| Full color | White Smoke or light backgrounds |
| White | Navy, Ebony, or dark photo backgrounds |
| Navy | White Smoke backgrounds only |

### Logo Guidelines

- **Clear Space:** Always maintain clear space equal to the height of the logo mark on all sides
- **Minimum Size:** Never reproduce the combination mark smaller than 120px wide
- **Never:** Distort, rotate at angles, recolor outside approved versions, place on low-contrast backgrounds, or add drop shadows to the logo

---

## Spacing System

Based on 4px increments:

```css
--sob-space-0: 0;
--sob-space-1: 0.25rem;     /* 4px */
--sob-space-2: 0.5rem;      /* 8px */
--sob-space-3: 0.75rem;     /* 12px */
--sob-space-4: 1rem;        /* 16px */
--sob-space-5: 1.25rem;     /* 20px */
--sob-space-6: 1.5rem;      /* 24px */
--sob-space-8: 2rem;        /* 32px */
--sob-space-10: 2.5rem;     /* 40px */
--sob-space-12: 3rem;       /* 48px */
--sob-space-16: 4rem;       /* 64px */
--sob-space-20: 5rem;       /* 80px */
--sob-space-24: 6rem;       /* 96px */
--sob-space-32: 8rem;       /* 128px */
```

### Shorthand Aliases

```css
--sob-space-xs: var(--sob-space-1);   /* 4px */
--sob-space-sm: var(--sob-space-2);   /* 8px */
--sob-space-md: var(--sob-space-4);   /* 16px */
--sob-space-lg: var(--sob-space-6);   /* 24px */
--sob-space-xl: var(--sob-space-8);   /* 32px */
--sob-space-2xl: var(--sob-space-12); /* 48px */
--sob-space-3xl: var(--sob-space-16); /* 64px */
--sob-space-4xl: var(--sob-space-24); /* 96px */
```

---

## Borders

```css
--sob-border-width: 1px;
--sob-border-color: rgba(4, 0, 91, 0.15);   /* Navy at 15% opacity */
--sob-border: 1px solid rgba(4, 0, 91, 0.15);

--sob-radius: 4px;                 /* Default - subtle rounding */
--sob-radius-sm: 2px;              /* Badges, small elements */
--sob-radius-md: 8px;              /* Cards, larger elements */
--sob-radius-lg: 12px;             /* Prominent elements */
--sob-radius-full: 9999px;         /* Pills, circular */
```

### Dividers

```css
.sob-divider {
  border: none;
  border-top: 1px solid rgba(4, 0, 91, 0.12);
  margin: var(--sob-space-lg) 0;
}

.sob-divider--strong {
  border-top-color: rgba(4, 0, 91, 0.25);
}

.sob-divider--accent {
  border-top-color: var(--sob-texas-rose);
  border-top-width: 2px;
}
```

---

## Shadows

Subtle, modern shadows:

```css
--sob-shadow-sm: 0 1px 2px 0 rgba(13, 10, 27, 0.05);
--sob-shadow: 0 1px 3px 0 rgba(13, 10, 27, 0.1), 0 1px 2px -1px rgba(13, 10, 27, 0.1);
--sob-shadow-md: 0 4px 6px -1px rgba(13, 10, 27, 0.1), 0 2px 4px -2px rgba(13, 10, 27, 0.1);
--sob-shadow-lg: 0 10px 15px -3px rgba(13, 10, 27, 0.1), 0 4px 6px -4px rgba(13, 10, 27, 0.1);
--sob-shadow-xl: 0 20px 25px -5px rgba(13, 10, 27, 0.1), 0 8px 10px -6px rgba(13, 10, 27, 0.1);

/* Heliotrope glow for special emphasis */
--sob-shadow-heliotrope: 0 4px 14px 0 rgba(235, 85, 246, 0.25);
--sob-shadow-heliotrope-lg: 0 10px 25px 0 rgba(235, 85, 246, 0.3);

/* Texas Rose glow for CTA emphasis */
--sob-shadow-cta: 0 4px 14px 0 rgba(255, 189, 74, 0.35);
```

---

## Effects & Transforms

### Transitions

```css
--sob-transition-fast: 150ms ease;
--sob-transition-base: 200ms ease;
--sob-transition-slow: 300ms ease;
--sob-transition-slower: 500ms ease;

--sob-transition-colors: color 200ms ease, background-color 200ms ease, border-color 200ms ease;
--sob-transition-transform: transform 200ms ease;
--sob-transition-shadow: box-shadow 200ms ease;
--sob-transition-all: all 200ms ease;
```

### Hover Effects

```css
/* Lift on hover */
.sob-hover-lift {
  transition: transform 200ms ease, box-shadow 200ms ease;
}

.sob-hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: var(--sob-shadow-md);
}

/* Scale on hover */
.sob-hover-scale {
  transition: transform 300ms ease;
}

.sob-hover-scale:hover {
  transform: scale(1.02);
}

/* Brighten on hover (for images) */
.sob-hover-brighten {
  transition: filter 300ms ease;
}

.sob-hover-brighten:hover {
  filter: brightness(1.05);
}
```

### Opacity Levels

```css
--sob-opacity-disabled: 0.5;
--sob-opacity-muted: 0.6;
--sob-opacity-subtle: 0.8;
```

---

## Components

### Buttons

#### Primary Button (Texas Rose)

```css
.sob-button-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--sob-space-2);

  background: var(--sob-texas-rose);
  color: var(--sob-ebony);

  font-family: var(--sob-font-heading);
  font-size: var(--sob-text-sm);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;

  padding: var(--sob-space-3) var(--sob-space-6);
  border: none;
  border-radius: var(--sob-radius);

  cursor: pointer;
  transition: var(--sob-transition-colors), var(--sob-transition-shadow);
}

.sob-button-primary:hover {
  background: var(--sob-portage);
  color: var(--sob-ebony);
  box-shadow: var(--sob-shadow-cta);
}

.sob-button-primary:focus-visible {
  outline: 2px solid var(--sob-portage);
  outline-offset: 2px;
}

.sob-button-primary:disabled {
  opacity: var(--sob-opacity-disabled);
  cursor: not-allowed;
}
```

**HTML:**
```html
<button class="sob-button-primary">
  Get Started
</button>
```

#### Secondary Button (Outline)

```css
.sob-button-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--sob-space-2);

  background: transparent;
  color: var(--sob-navy);
  border: 2px solid var(--sob-navy);

  font-family: var(--sob-font-heading);
  font-size: var(--sob-text-sm);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;

  padding: var(--sob-space-3) var(--sob-space-6);
  border-radius: var(--sob-radius);

  cursor: pointer;
  transition: var(--sob-transition-colors);
}

.sob-button-secondary:hover {
  background: var(--sob-navy);
  color: var(--sob-white-smoke);
}

.sob-button-secondary:focus-visible {
  outline: 2px solid var(--sob-portage);
  outline-offset: 2px;
}
```

#### Ghost Button (Dark Backgrounds)

```css
.sob-button-ghost {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--sob-space-2);

  background: transparent;
  color: var(--sob-white-smoke);
  border: 2px solid var(--sob-white-smoke);

  font-family: var(--sob-font-heading);
  font-size: var(--sob-text-sm);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;

  padding: var(--sob-space-3) var(--sob-space-6);
  border-radius: var(--sob-radius);

  cursor: pointer;
  transition: var(--sob-transition-colors);
}

.sob-button-ghost:hover {
  background: var(--sob-heliotrope);
  border-color: var(--sob-heliotrope);
  color: var(--sob-ebony);
}
```

---

## Layout Patterns

### Container

```css
.sob-container {
  width: 100%;
  max-width: var(--sob-container-xl);
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--sob-space-md);
  padding-right: var(--sob-space-md);
}

/* Container Widths */
--sob-container-sm: 640px;
--sob-container-md: 768px;
--sob-container-lg: 1024px;
--sob-container-xl: 1280px;
--sob-container-2xl: 1536px;
```

### Section Spacing

```css
.sob-section {
  padding-top: var(--sob-space-3xl);
  padding-bottom: var(--sob-space-3xl);
}

@media screen and (min-width: 768px) {
  .sob-section {
    padding-top: var(--sob-space-4xl);
    padding-bottom: var(--sob-space-4xl);
  }
}

.sob-section--sm {
  padding-top: var(--sob-space-2xl);
  padding-bottom: var(--sob-space-2xl);
}
```

### Grid System

```css
.sob-grid {
  display: grid;
  gap: var(--sob-space-lg);
}

/* 2-Column Grid */
.sob-grid--2 {
  grid-template-columns: 1fr;
}

@media screen and (min-width: 768px) {
  .sob-grid--2 {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 3-Column Grid */
.sob-grid--3 {
  grid-template-columns: 1fr;
}

@media screen and (min-width: 768px) {
  .sob-grid--3 {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media screen and (min-width: 1024px) {
  .sob-grid--3 {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* 4-Column Grid */
.sob-grid--4 {
  grid-template-columns: repeat(2, 1fr);
}

@media screen and (min-width: 768px) {
  .sob-grid--4 {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

### Flexbox Utilities

```css
.sob-flex {
  display: flex;
}

.sob-flex--center {
  align-items: center;
  justify-content: center;
}

.sob-flex--between {
  align-items: center;
  justify-content: space-between;
}

.sob-flex--col {
  flex-direction: column;
}

.sob-gap-sm { gap: var(--sob-space-sm); }
.sob-gap-md { gap: var(--sob-space-md); }
.sob-gap-lg { gap: var(--sob-space-lg); }
.sob-gap-xl { gap: var(--sob-space-xl); }
```

### Section Structure Pattern

```html
<section class="sob-section sob-section--[variant]" id="section-name">
  <div class="sob-container">
    <header class="sob-section__header">
      <h2 class="sob-heading">Section Title</h2>
    </header>
    <div class="sob-section__content">
      <!-- Content components -->
    </div>
  </div>
</section>

<style>
  /* 1. Structure & Layout */
  /* 2. Typography */
  /* 3. Components */
  /* 4. States */
  /* 5. Media Queries */
</style>
```

---

## Responsive Breakpoints

```css
/* Mobile first approach */
--sob-breakpoint-sm: 640px;
--sob-breakpoint-md: 768px;
--sob-breakpoint-lg: 1024px;
--sob-breakpoint-xl: 1280px;
--sob-breakpoint-2xl: 1536px;
```

**Usage:**
- Base styles: Mobile (320px+)
- `sm:` prefix: Small tablets (640px+)
- `md:` prefix: Tablets (768px+)
- `lg:` prefix: Desktop (1024px+)
- `xl:` prefix: Large desktop (1280px+)

```css
/* Example: Mobile-first responsive pattern */
.sob-hero__title {
  font-size: var(--sob-text-4xl);
}

@media screen and (min-width: 768px) {
  .sob-hero__title {
    font-size: var(--sob-text-6xl);
  }
}

@media screen and (min-width: 1024px) {
  .sob-hero__title {
    font-size: var(--sob-text-7xl);
  }
}
```

### Visibility Utilities

```css
.sob-hide-mobile {
  display: none;
}

@media screen and (min-width: 768px) {
  .sob-hide-mobile {
    display: block;
  }
}

.sob-hide-desktop {
  display: block;
}

@media screen and (min-width: 768px) {
  .sob-hide-desktop {
    display: none;
  }
}
```

---

## Accessibility

### Focus States

```css
:focus-visible {
  outline: 2px solid var(--sob-portage);
  outline-offset: 2px;
}

/* Remove default focus for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}
```

### Minimum Touch Targets

All interactive elements should be at least 44x44px on mobile devices.

```css
.sob-touch-target {
  min-width: 44px;
  min-height: 44px;
}
```

### Screen Reader Utilities

```css
.sob-sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

### Color Contrast

All approved color combinations meet WCAG 4.5:1 minimum contrast ratio for body text.

**Approved Combinations:**
- Navy on White Smoke
- Ebony on White Smoke
- White Smoke on Navy
- White Smoke on Ebony
- Texas Rose on Navy
- Texas Rose on Ebony

**Not approved for body text (decorative/large text only):**
- Heliotrope on White Smoke
- Portage on White Smoke
- Texas Rose on White Smoke

---

## Usage Guidelines

### Do's

- Use ~60/30/10 color proportion (White Smoke backgrounds / Navy + Ebony / Texas Rose + accents)
- Use Navy for most headlines
- Use Ebony for body copy and paragraphs
- Use Texas Rose for primary CTAs and key accents
- Use Heliotrope and Portage sparingly — hover states, gradients, highlights only
- Keep White Smoke as the default background
- Maintain adequate whitespace between sections
- Use subtle shadows and rounded corners
- Ensure focus states are always visible (Portage outline)

### Don'ts

- Don't use Heliotrope or Portage as dominant colors — they're accents only
- Don't overuse Texas Rose beyond CTAs and key accents
- Don't place Heliotrope or Portage text on White Smoke backgrounds (contrast failure for small text)
- Don't use harsh or brutalist design elements
- Don't crowd elements — let the layout breathe
- Don't distort, recolor, or add effects to the logo

---

## Tailwind CSS Configuration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        sob: {
          heliotrope: '#EB55F6',
          navy: '#04005B',
          ebony: '#0D0A1B',
          'white-smoke': '#F8F9FA',
          portage: '#A59FF7',
          'texas-rose': '#FFBD4A',
        }
      },
      fontFamily: {
        // Update with actual font names from Drive
        'sob-heading': ['[PRIMARY-FONT]', 'system-ui', 'sans-serif'],
        'sob-display': ['[SECONDARY-FONT]', 'Georgia', 'serif'],
      },
      borderRadius: {
        'sob': '4px',
        'sob-md': '8px',
        'sob-lg': '12px',
      },
      boxShadow: {
        'sob': '0 1px 3px 0 rgba(13, 10, 27, 0.1), 0 1px 2px -1px rgba(13, 10, 27, 0.1)',
        'sob-md': '0 4px 6px -1px rgba(13, 10, 27, 0.1), 0 2px 4px -2px rgba(13, 10, 27, 0.1)',
        'sob-lg': '0 10px 15px -3px rgba(13, 10, 27, 0.1), 0 4px 6px -4px rgba(13, 10, 27, 0.1)',
        'sob-heliotrope': '0 4px 14px 0 rgba(235, 85, 246, 0.25)',
        'sob-cta': '0 4px 14px 0 rgba(255, 189, 74, 0.35)',
      }
    }
  }
}
```

**Example Tailwind Usage:**

```html
<!-- Primary Button -->
<button class="bg-sob-texas-rose hover:bg-sob-portage text-sob-ebony font-bold text-sm uppercase tracking-wider px-6 py-3 rounded-sob transition-colors">
  Get Started
</button>

<!-- Card -->
<article class="bg-sob-white-smoke rounded-sob-md p-6 shadow-sob hover:shadow-sob-md transition-shadow">
  <h3 class="font-sob-heading font-bold text-xl uppercase tracking-tight text-sob-navy mb-2">
    Card Title
  </h3>
  <p class="text-sob-ebony">
    Card description goes here.
  </p>
</article>

<!-- Dark Section -->
<section class="bg-sob-navy text-sob-white-smoke">
  <h2 class="text-sob-texas-rose font-bold">Headline on Dark</h2>
  <p class="text-sob-white-smoke opacity-80">Body copy on dark background.</p>
</section>
```

---

## Complete CSS Variables Reference

Copy this entire block as your base stylesheet:

```css
/* School of Bots Design System v1.0.0 */

:root {
  /* ==================== COLORS ==================== */

  --sob-heliotrope: #EB55F6;
  --sob-navy: #04005B;
  --sob-ebony: #0D0A1B;
  --sob-white-smoke: #F8F9FA;
  --sob-portage: #A59FF7;
  --sob-texas-rose: #FFBD4A;

  /* ==================== TYPOGRAPHY ==================== */

  /* Update with actual font names from Drive */
  --sob-font-heading: '[PRIMARY-FONT]', system-ui, sans-serif;
  --sob-font-body: '[PRIMARY-FONT]', system-ui, sans-serif;
  --sob-font-display: '[SECONDARY-FONT]', Georgia, serif;

  /* Font Sizes */
  --sob-text-hero: clamp(3rem, 10vw, 8rem);
  --sob-text-7xl: 4.5rem;
  --sob-text-6xl: 3.75rem;
  --sob-text-5xl: 3rem;
  --sob-text-4xl: 2.25rem;
  --sob-text-3xl: 1.875rem;
  --sob-text-2xl: 1.5rem;
  --sob-text-xl: 1.25rem;
  --sob-text-base: 1rem;
  --sob-text-sm: 0.875rem;
  --sob-text-xs: 0.75rem;
  --sob-text-2xs: 0.625rem;

  /* Font Weights */
  --sob-font-normal: 400;
  --sob-font-medium: 500;
  --sob-font-bold: 700;

  /* Line Heights */
  --sob-leading-none: 1;
  --sob-leading-tight: 1.1;
  --sob-leading-snug: 1.25;
  --sob-leading-normal: 1.5;
  --sob-leading-relaxed: 1.625;
  --sob-leading-loose: 2;

  /* Letter Spacing */
  --sob-tracking-tighter: -0.03em;
  --sob-tracking-tight: -0.02em;
  --sob-tracking-normal: -0.01em;
  --sob-tracking-wide: 0.025em;
  --sob-tracking-wider: 0.05em;
  --sob-tracking-widest: 0.1em;

  /* ==================== SPACING ==================== */

  --sob-space-0: 0;
  --sob-space-1: 0.25rem;
  --sob-space-2: 0.5rem;
  --sob-space-3: 0.75rem;
  --sob-space-4: 1rem;
  --sob-space-5: 1.25rem;
  --sob-space-6: 1.5rem;
  --sob-space-8: 2rem;
  --sob-space-10: 2.5rem;
  --sob-space-12: 3rem;
  --sob-space-16: 4rem;
  --sob-space-20: 5rem;
  --sob-space-24: 6rem;
  --sob-space-32: 8rem;

  /* Shorthand */
  --sob-space-xs: var(--sob-space-1);
  --sob-space-sm: var(--sob-space-2);
  --sob-space-md: var(--sob-space-4);
  --sob-space-lg: var(--sob-space-6);
  --sob-space-xl: var(--sob-space-8);
  --sob-space-2xl: var(--sob-space-12);
  --sob-space-3xl: var(--sob-space-16);
  --sob-space-4xl: var(--sob-space-24);

  /* ==================== BORDERS ==================== */

  --sob-border-width: 1px;
  --sob-border-color: rgba(4, 0, 91, 0.15);
  --sob-border: 1px solid rgba(4, 0, 91, 0.15);

  --sob-radius: 4px;
  --sob-radius-sm: 2px;
  --sob-radius-md: 8px;
  --sob-radius-lg: 12px;
  --sob-radius-full: 9999px;

  /* ==================== SHADOWS ==================== */

  --sob-shadow-sm: 0 1px 2px 0 rgba(13, 10, 27, 0.05);
  --sob-shadow: 0 1px 3px 0 rgba(13, 10, 27, 0.1), 0 1px 2px -1px rgba(13, 10, 27, 0.1);
  --sob-shadow-md: 0 4px 6px -1px rgba(13, 10, 27, 0.1), 0 2px 4px -2px rgba(13, 10, 27, 0.1);
  --sob-shadow-lg: 0 10px 15px -3px rgba(13, 10, 27, 0.1), 0 4px 6px -4px rgba(13, 10, 27, 0.1);
  --sob-shadow-xl: 0 20px 25px -5px rgba(13, 10, 27, 0.1), 0 8px 10px -6px rgba(13, 10, 27, 0.1);
  --sob-shadow-heliotrope: 0 4px 14px 0 rgba(235, 85, 246, 0.25);
  --sob-shadow-heliotrope-lg: 0 10px 25px 0 rgba(235, 85, 246, 0.3);
  --sob-shadow-cta: 0 4px 14px 0 rgba(255, 189, 74, 0.35);

  /* ==================== TRANSITIONS ==================== */

  --sob-transition-fast: 150ms ease;
  --sob-transition-base: 200ms ease;
  --sob-transition-slow: 300ms ease;
  --sob-transition-slower: 500ms ease;

  /* ==================== CONTAINERS ==================== */

  --sob-container-sm: 640px;
  --sob-container-md: 768px;
  --sob-container-lg: 1024px;
  --sob-container-xl: 1280px;
  --sob-container-2xl: 1536px;

  /* ==================== BREAKPOINTS ==================== */

  --sob-breakpoint-sm: 640px;
  --sob-breakpoint-md: 768px;
  --sob-breakpoint-lg: 1024px;
  --sob-breakpoint-xl: 1280px;
  --sob-breakpoint-2xl: 1536px;

  /* ==================== OPACITY ==================== */

  --sob-opacity-disabled: 0.5;
  --sob-opacity-muted: 0.6;
  --sob-opacity-subtle: 0.8;
}

/* Selection Highlight */
::selection {
  background-color: var(--sob-heliotrope);
  color: var(--sob-ebony);
}
```

---

## Maintenance

When adding new components or sections:

1. **Reference this design system first** — Check existing patterns before creating new ones
2. **Use existing tokens** — Colors, typography, spacing from CSS variables only
3. **Follow naming convention** — `sob-` prefix with BEM-inspired naming
4. **Mobile-first responsive** — Base styles for mobile, `@media` for desktop
5. **Organize CSS** — Structure → Typography → Components → States → Media
6. **Test accessibility** — Focus states, contrast ratios, touch targets (min 44x44px)
7. **Document new patterns** — Update this file when adding novel patterns

---

**Design System Version:** 1.0.0
**Last Updated:** 2026-03-05
**Font Reference:** [Drive — Font Downloads](https://drive.google.com/drive/u/0/folders/1SizrBL_xI_Tsv8WKEbZTX4QSU4lFz0dB)
**Logo Reference:** [Drive — Logo Files](https://drive.google.com/drive/u/2/folders/1-vlDYMrRrtuOaq0WbIp2zP8ss4OYO-Md)
**Font Applications (Page 4):** [Brand PDF](https://drive.google.com/file/d/1i89TQwpDsojqpFfxmN61nsVdLjTTa2Hk/view?usp=sharing)
