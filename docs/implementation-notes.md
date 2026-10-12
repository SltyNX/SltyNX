# SltyNX Profile README — Implementation Notes

## Overview

This repository powers the GitHub Profile README for **[SltyNX](https://github.com/SltyNX)** (`Sleeping Core`).
All visual panels are deterministically generated as standalone, GitHub-compatible SVGs using standard-library Python 3.12 scripts in `scripts/`.

## Repository Structure

```text
SltyNX/
├── README.md
├── assets/
│   ├── hero.svg
│   ├── hero-fallback.png
│   ├── sltynx-logo.svg
│   ├── dotmatrix-name.svg
│   ├── profile-avatar.png
│   ├── telegram-button.svg
│   ├── current-project.svg
│   ├── skills-learning.svg
│   ├── terminal-session.svg
│   ├── ai-assistance.svg
│   ├── error-repair.svg
│   ├── knowledge-panel.svg
│   ├── funny-quote.svg
│   └── footer.svg
├── source-assets/
│   ├── sleepy-mascot.jpg
│   ├── sltynx-logo-reference.png
│   └── confused-mascot.jpg
├── knowledge-base/
│   ├── learning-notes/README.md
│   ├── experiments/README.md
│   ├── project-references/README.md
│   └── ideas/README.md
├── scripts/
│   ├── config.py
│   ├── generate.py
│   ├── generate_hero.py
│   ├── generate_dotmatrix.py
│   ├── generate_terminal.py
│   └── validate_assets.py
├── .github/
│   └── workflows/
│       └── validate-profile.yml
└── docs/
    └── implementation-notes.md
```

## Regenerating & Validating Assets

No external third-party Python packages are required to build or validate the SVGs:

```bash
python3 scripts/generate.py
python3 scripts/validate_assets.py
```

## Animation & Fallback Architecture

1. **GitHub Compatibility**: Because GitHub strips `<script>` tags and external network requests inside `<img>` SVGs, all animations use pure CSS `@keyframes` inside self-contained `<svg>` files, with reference mascot artwork (`sleepy-mascot.jpg` and `confused-mascot.jpg`) embedded as base64 data URIs.
2. **Reduced-Motion & Static Fallbacks**:
   - Every animated SVG includes a `@media (prefers-reduced-motion: reduce)` rule that freezes the animation at its completed, readable state.
   - `README.md` uses `<picture>` elements with `<source media="(prefers-reduced-motion: reduce)">` pointing to `./assets/hero-fallback.png` and `./assets/sltynx-logo.svg`.
   - All critical copy, links, and terminal logs are available directly in accessible Markdown text and `<details>` transcripts.
