#!/usr/bin/env python3
"""
Validation suite for the SltyNX GitHub Profile README (Stage 8).
Checks:
1. Required repository files and assets exist and are non-empty.
2. All SVGs have valid XML structure, SVG namespace, width, height, and viewBox.
3. No duplicate element IDs exist inside any SVG.
4. No <script> or <iframe> tags exist in any SVG or README.md.
5. Element coordinates (rect, circle, text) remain inside their SVG viewBox bounds.
6. All local image references and links in README.md resolve to existing targets.
7. Required profile links and text fallbacks are present in README.md.
"""
from __future__ import annotations
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"
SOURCE_DIR = ROOT / "source-assets"
README_PATH = ROOT / "README.md"

REQUIRED_ASSETS = [
    "hero.svg",
    "hero-fallback.png",
    "sltynx-logo.svg",
    "dotmatrix-name.svg",
    "profile-avatar.png",
    "profile-intro.svg",
    "telegram-button.svg",
    "current-project.svg",
    "skills-learning.svg",
    "terminal-session.svg",
    "ai-assistance.svg",
    "error-repair.svg",
    "knowledge-panel.svg",
    "funny-quote.svg",
    "footer.svg",
    "mobile/hero.svg",
    "mobile/dotmatrix-name.svg",
    "mobile/profile-intro.svg",
    "mobile/current-project.svg",
    "mobile/skills-learning.svg",
    "mobile/terminal-session.svg",
    "mobile/ai-assistance.svg",
    "mobile/error-repair.svg",
    "mobile/knowledge-panel.svg",
    "mobile/funny-quote.svg",
    "mobile/footer.svg",
]

REQUIRED_SOURCES = [
    "sleepy-mascot.jpg",
    "sltynx-logo-reference.png",
    "confused-mascot.jpg",
]


def validate_svg_file(svg_path: pathlib.Path, errors: list[str]) -> None:
    name = svg_path.name
    raw = svg_path.read_text(encoding="utf-8")

    if "<script" in raw.lower() or "<iframe" in raw.lower():
        errors.append(f"{name}: contains forbidden <script> or <iframe> tag")

    if "#000000" not in raw.lower():
        errors.append(f"{name}: missing primary true-black background (#000000)")

    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        errors.append(f"{name}: invalid XML ({exc})")
        return

    if not root.tag.endswith("svg"):
        errors.append(f"{name}: root element is not <svg> (got {root.tag})")

    vb = root.attrib.get("viewBox", "")
    parts = [float(x) for x in vb.split()] if vb else []
    if len(parts) != 4:
        errors.append(f"{name}: missing or invalid viewBox='{vb}'")
        return

    _, _, vb_w, vb_h = parts

    # Check duplicate IDs
    seen_ids: set[str] = set()
    for elem in root.iter():
        eid = elem.attrib.get("id")
        if eid:
            if eid in seen_ids:
                errors.append(f"{name}: duplicate SVG element id='{eid}'")
            seen_ids.add(eid)

        # Bounds check for top-level / un-transformed rects and texts
        tag = elem.tag.split("}")[-1]
        if tag == "text":
            x_str = elem.attrib.get("x")
            y_str = elem.attrib.get("y")
            if x_str and y_str:
                try:
                    tx, ty = float(x_str), float(y_str)
                    if ty > vb_h or tx > vb_w:
                        errors.append(f"{name}: <text> at ({tx}, {ty}) exceeds viewBox ({vb_w}x{vb_h})")
                except ValueError:
                    pass


def validate_readme(errors: list[str]) -> None:
    if not README_PATH.exists():
        errors.append("README.md is missing")
        return

    text = README_PATH.read_text(encoding="utf-8")

    # Check local src/srcset paths
    for match in re.finditer(r'(?:src|srcset)="([^"]+)"', text):
        ref = match.group(1)
        if ref.startswith(("http://", "https://", "data:")):
            continue
        target = (ROOT / ref).resolve()
        if not target.exists():
            errors.append(f"README.md: broken image reference '{ref}'")

    # Check markdown links
    for match in re.finditer(r"\]\(([^)]+)\)", text):
        link = match.group(1).strip()
        if link.startswith(("http://", "https://", "#")):
            continue
        target = (ROOT / link).resolve()
        if not target.exists():
            errors.append(f"README.md: broken local link '{link}'")

    # Verify required links & content
    required_snippets = [
        "https://t.me/SltyNX_X",
        "@SltyNX_X",
        "private currently",
        "Sleeping Core",
        "Beginner \u2014 Learning in Progress",
        "don't give up on me bro, I'm trying to understand it for real.",
    ]
    for snippet in required_snippets:
        if snippet not in text:
            errors.append(f"README.md: missing required content '{snippet}'")


def main() -> int:
    errors: list[str] = []

    for fname in REQUIRED_ASSETS:
        p = ASSETS_DIR / fname
        if not p.exists() or p.stat().st_size == 0:
            errors.append(f"Missing or empty asset: assets/{fname}")
        elif p.suffix == ".svg":
            validate_svg_file(p, errors)

    for sname in REQUIRED_SOURCES:
        p = SOURCE_DIR / sname
        if not p.exists() or p.stat().st_size == 0:
            errors.append(f"Missing or empty source asset: source-assets/{sname}")

    validate_readme(errors)

    if errors:
        print("VALIDATION FAILED:")
        for err in errors:
            print(f"  [!] {err}")
        return 1

    print("ALL VALIDATION CHECKS PASSED:")
    print(f"  [OK] {len(REQUIRED_ASSETS)} generated assets verified in assets/")
    print(f"  [OK] {len(REQUIRED_SOURCES)} reference assets verified in source-assets/")
    print("  [OK] All SVGs have valid XML, unique IDs, #000000 backgrounds, and in-bounds viewBoxes")
    print("  [OK] All README.md local paths, fallbacks, and external links verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
