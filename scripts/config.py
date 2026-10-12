#!/usr/bin/env python3
"""
Centralized configuration, design tokens, brand geometry, and content
for the SltyNX GitHub Profile README.
"""
from __future__ import annotations
import base64
import pathlib

ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent
SOURCE_ASSETS_DIR = ROOT_DIR / "source-assets"
ASSETS_DIR = ROOT_DIR / "assets"

# ---------------------------------------------------------------------------
# 1. Profile Identity & Verified Sources (Section 2 & 7 & 8 & 9)
# ---------------------------------------------------------------------------
USER = "SltyNX"
DISPLAY_NAME = "SLYTNX"
BIO = "Sleeping Core"

GITHUB_URL = "https://github.com/SltyNX"
PROFILE_REPO_URL = "https://github.com/SltyNX/SltyNX"
PROJECT_NAME = "Gnosis Keyboard"
PROJECT_REPO_NAME = "private currently"
PROJECT_URL = "private currently"
PROJECT_STATUS = "In Progress"
PROJECT_DESCRIPTION = (
    "A custom Android keyboard focused on control, customization, "
    "and a better typing experience."
)

TELEGRAM_USERNAME = "@SltyNX_X"
TELEGRAM_URL = "https://t.me/SltyNX_X"
TELEGRAM_CTA = "Message me on Telegram"

INTRO_QUOTE = (
    "Just a guy who sleeps a lot, codes a little, and dreams of building something cool."
)
DEV_STATUS_TEXT = (
    "Currently a noob developer. Learning as I go, breaking things occasionally, "
    "and trying to understand how everything works."
)

# ---------------------------------------------------------------------------
# 2. Visual Design System — Pure Black Minimalist Terminal (Section 4)
# ---------------------------------------------------------------------------
BG_PRIMARY = "#000000"      # True black primary canvas
BG_SECONDARY = "#080808"    # Supporting near-black surface
BG_ELEVATED = "#0D0D0D"     # Terminal headers / inner cards / keycaps
BG_DOT_IDLE = "#141414"     # Unlit dot-matrix grid cells

TEXT_PRIMARY = "#F2F2F2"    # Crisp off-white primary text & active dots
TEXT_SECONDARY = "#A6A6A6"  # Muted grey descriptions & secondary labels
TEXT_MUTED = "#6E6E6E"      # Subtle terminal metadata, timestamps, comments
TEXT_DIM = "#383838"        # Low-contrast structural accents

BORDER = "#303030"          # Thin 1px structural card & badge borders
BORDER_SUBTLE = "#1E1E1E"   # Inner panel separators

ACCENT_GLOW = "#D8D8D8"     # Restrained monochrome white/grey highlight
TERM_SUCCESS = "#4ADE80"    # Subdued green — strictly for semantic terminal success
TERM_ERROR = "#F87171"      # Subdued red — strictly for semantic terminal errors
TERM_WARN = "#FBBF24"       # Subdued amber — strictly for construction warning sign

FONT_MONO = (
    "'JetBrains Mono', 'Fira Code', 'Cascadia Code', 'SFMono-Regular', "
    "Consolas, 'Liberation Mono', Menlo, 'Courier New', monospace"
)
FONT_SANS = (
    "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Roboto, "
    "Helvetica, Arial, sans-serif"
)

SVG_NS = 'xmlns="http://www.w3.org/2000/svg"'

# ---------------------------------------------------------------------------
# 3. Hero & Footer Copy (Section 5 & 16)
# ---------------------------------------------------------------------------
HERO_TAGLINE = "sleep > code > repeat"
HERO_STATUS = "status: sleeping..."
HERO_CLOCK = "03:14 AM"

FOOTER_WORDMARK = "SLYTNX"
FOOTER_TAGLINE = "sleep \u2022 code \u2022 create"
FOOTER_THANKS = "Thanks for visiting!"
FOOTER_STATUS = "Still loading..."

# ---------------------------------------------------------------------------
# 4. Beginner Skills & Learning Inventory (Section 10)
# ---------------------------------------------------------------------------
SKILLS_HEADING = "Skills / Tools"
SKILLS_LABEL = "Beginner \u2014 Learning in Progress"
SKILLS_MESSAGE = "Not skilled yet, but I'm building it step by step."

# Honest beginner learning inventory without fabricated percentages
LEARNING_ITEMS = [
    ("Android Exploration", "Exploring inputviews & keyboard layouts", "exploring"),
    ("Kotlin & Java Basics", "Reading docs & experimenting step by step", "learning"),
    ("Python Scripting", "Small scripts, configs & SVG generation", "learning"),
    ("Git & GitHub", "Commits, repositories & version control basics", "using"),
    ("JSON & Configs", "Keyboard data files & structured layouts", "using"),
    ("Markdown & SVG", "Building clean documentation & visual assets", "exploring"),
    ("Trial & Error Debugging", "Breaking things, reading errors & fixing them", "always"),
    ("AI-Assisted Learning", "Asking for hints when stuck & understanding why", "using"),
]

# ---------------------------------------------------------------------------
# 5. Terminal Session — Running Out of Ideas (Section 11)
# ---------------------------------------------------------------------------
TERMINAL_SCENE_A_LINES = [
    ("cmd", "$ start-project"),
    ("out", "> opening the editor..."),
    ("out", "> thinking of an idea..."),
    ("err", "> no ideas found."),
    ("out", "> searching for motivation..."),
]
MASCOT_THOUGHT_BUBBLE = "...what now?"

AI_SERVICES = [
    ("Claude \u2014 Sonnet", "hint-node // 01"),
    ("Gemini", "hint-node // 02"),
    ("ChatGPT", "hint-node // 03"),
]

AI_POPUPS = [
    "asking for a hint...",
    "idea detected?",
    "trying again...",
]

TERMINAL_SCENE_D_LINES = [
    ("ok", "> hint received"),
    ("out", "> trying to understand..."),
    ("out", "> implementing solution..."),
]

# ---------------------------------------------------------------------------
# 6. Error Animation — The AI Construction Truck (Section 12)
# ---------------------------------------------------------------------------
ERROR_REPAIR_LINES = [
    ("err", "! error: something went wrong"),
    ("out", "> diagnosis: developer confusion"),
    ("out", "> requesting assistance..."),
    ("out", "> applying fix..."),
    ("ok", "\u2713 build successful (in this simulation)"),
]

# ---------------------------------------------------------------------------
# 7. Knowledge Base Section (Section 13)
# ---------------------------------------------------------------------------
KNOWLEDGE_TITLE = "Knowledge Base"
KNOWLEDGE_SUBTITLE = "Notes, experiments, and things I'm learning."
KNOWLEDGE_DIRS = [
    ("learning-notes/", "notes on Android input, Python & Git basics", "./knowledge-base/learning-notes"),
    ("experiments/", "small layout tests & terminal SVG sandboxes", "./knowledge-base/experiments"),
    ("project-references/", "Gnosis Keyboard data structures & references", "./knowledge-base/project-references"),
    ("ideas/", "future tools to build after catching up on sleep", "./knowledge-base/ideas"),
]
KNOWLEDGE_EXTRACTION_LINES = [
    "> opening study-notes.zip...",
    "> extracting knowledge...",
    "> still learning...",
]

# ---------------------------------------------------------------------------
# 8. Funny Quote — Trying to Understand (Section 14)
# ---------------------------------------------------------------------------
FUNNY_QUOTE_TITLE = "Trying to Understand"
FUNNY_QUOTE_TEXT = (
    '"When I say Ehh, ehhh, ehhhh... like for three time, '
    'don\'t give up on me bro, I\'m trying to understand it for real."'
)
FUNNY_QUOTE_CAPTION = "// internal monologue while reading documentation at 3 AM"

# ---------------------------------------------------------------------------
# 9. Discrete Square Dot-Matrix Bitmaps (11 rows x 9 cols per letter)
#    Captures the geometric SLYTNX typography from Asset B in discrete dots
# ---------------------------------------------------------------------------
DOT_LETTERS: dict[str, list[str]] = {
    "S": [
        " .#####. ",
        "#########",
        "###...###",
        "###......",
        ".#####...",
        "..######.",
        ".....####",
        "###...###",
        "###...###",
        "#########",
        " .#####. ",
    ],
    "L": [
        "##.......",
        "##.......",
        "##.......",
        "##.......",
        "##.......",
        "##.......",
        "##.......",
        "#########",
        "#########",
        "#########",
        "#########",
    ],
    "Y": [
        "#########",
        "#########",
        ".#######.",
        "..#####..",
        "...###...",
        "....#....",
        "....#....",
        "....#....",
        "....#....",
        "....#....",
        "....#....",
    ],
    "T": [
        "#########",
        "#########",
        "#########",
        "#########",
        "....#....",
        "....#....",
        "....#....",
        "....#....",
        "....#....",
        "....#....",
        "....#....",
    ],
    "N": [
        "#.......#",
        "##......#",
        "###.....#",
        "####....#",
        "#####...#",
        "######..#",
        "#######.#",
        "#########",
        "#########",
        "#########",
        "#########",
    ],
    "X": [
        "#########",
        ".#.....#.",
        "..#...#..",
        "...#.#...",
        "....#....",
        "....#....",
        "....#....",
        "...#.#...",
        "..#...#..",
        ".#.....#.",
        "#########",
    ],
}

# Discrete dot-matrix representation of the stacked triple-triangle emblem (13 rows x 17 cols)
DOT_EMBLEM: list[str] = [
    "........#........",
    ".......#.#.......",
    "......#...#......",
    ".....#..#..#.....",
    "....#..#.#..#....",
    "...#..#...#..#...",
    "..#############..",
    "...#.#.###.#.#...",
    "..#.#########.#..",
    ".###############.",
    "..#############..",
    ".###############.",
    "#################",
]


def render_brand_emblem_svg(cx: float, top_y: float, scale: float = 1.0, stroke_col: str = TEXT_PRIMARY, fill_col: str = TEXT_PRIMARY) -> str:
    """
    Renders the exact clean vector SltyNX triple-triangle emblem from Asset B:
    - Two upper wireframe triangles shifted vertically
    - One solid filled lower triangle overlapping them
    """
    # Base geometry at scale=1.0: total width = 76, total height = 84
    hw = 38.0 * scale
    sw = max(1.4, 2.0 * scale)

    # Top wireframe triangle: apex at top_y, base at top_y + 56*scale
    t1_apex_y = top_y
    t1_base_y = top_y + 56.0 * scale

    # Middle wireframe triangle: apex at top_y + 13*scale, base at top_y + 69*scale
    t2_apex_y = top_y + 13.0 * scale
    t2_base_y = top_y + 69.0 * scale

    # Bottom solid triangle: apex at top_y + 26*scale, base at top_y + 82*scale
    t3_apex_y = top_y + 26.0 * scale
    t3_base_y = top_y + 82.0 * scale

    return (
        f'<g class="sltynx-emblem">'
        f'<polygon points="{cx:.1f},{t1_apex_y:.1f} {cx - hw:.1f},{t1_base_y:.1f} {cx + hw:.1f},{t1_base_y:.1f}" '
        f'fill="none" stroke="{stroke_col}" stroke-width="{sw:.2f}" stroke-linejoin="miter" stroke-miterlimit="10"/>'
        f'<polygon points="{cx:.1f},{t2_apex_y:.1f} {cx - hw:.1f},{t2_base_y:.1f} {cx + hw:.1f},{t2_base_y:.1f}" '
        f'fill="none" stroke="{stroke_col}" stroke-width="{sw:.2f}" stroke-linejoin="miter" stroke-miterlimit="10"/>'
        f'<polygon points="{cx:.1f},{t3_apex_y:.1f} {cx - hw:.1f},{t3_base_y:.1f} {cx + hw:.1f},{t3_base_y:.1f}" '
        f'fill="{fill_col}"/>'
        f'</g>'
    )


def render_geometric_wordmark_svg(start_x: float, top_y: float, scale: float = 1.0, col: str = TEXT_PRIMARY) -> str:
    """
    Renders the exact geometric SLYTNX vector wordmark from Asset B:
    - S: Bold geometric S
    - L: Thin left vertical stem + thick solid horizontal bottom block
    - Y: Solid inverted triangle top bowl + thin center vertical stem
    - T: Thick solid horizontal top block + thin center vertical stem
    - N: Solid lower-left right triangle + thin right vertical stem
    - X: Hollow hourglass (two stroked triangles meeting at center)
    Total width at scale=1.0 is ~488px, height is 76px.
    """
    h = 76.0 * scale
    w = 62.0 * scale
    gap = 23.0 * scale
    thin = max(2.2, 3.6 * scale)
    thick = 21.0 * scale

    parts: list[str] = []

    # 1. Letter S (x = start_x)
    sx = start_x
    # Clean geometric S built with a bold stroked spine inside [sx, sx+w] x [top_y, top_y+h]
    s_sw = 15.0 * scale
    parts.append(
        f'<path d="M {sx + w - 6*scale:.1f} {top_y + 21*scale:.1f} '
        f'C {sx + w - 6*scale:.1f} {top_y + 4*scale:.1f}, {sx + 7*scale:.1f} {top_y + 4*scale:.1f}, {sx + 7*scale:.1f} {top_y + 20*scale:.1f} '
        f'C {sx + 7*scale:.1f} {top_y + 35*scale:.1f}, {sx + w - 5*scale:.1f} {top_y + 37*scale:.1f}, {sx + w - 5*scale:.1f} {top_y + 55*scale:.1f} '
        f'C {sx + w - 5*scale:.1f} {top_y + h - 4*scale:.1f}, {sx + 6*scale:.1f} {top_y + h - 4*scale:.1f}, {sx + 6*scale:.1f} {top_y + h - 22*scale:.1f}" '
        f'fill="none" stroke="{col}" stroke-width="{s_sw:.2f}" stroke-linecap="butt"/>'
    )

    # 2. Letter L (thin vertical left stem + thick bottom bar)
    lx = start_x + (w + gap) * 1
    parts.append(
        f'<rect x="{lx:.1f}" y="{top_y:.1f}" width="{thin:.2f}" height="{h:.1f}" fill="{col}"/>'
        f'<rect x="{lx:.1f}" y="{top_y + h - thick:.1f}" width="{w:.1f}" height="{thick:.1f}" fill="{col}"/>'
    )

    # 3. Letter Y (solid inverted triangle top + thin vertical bottom stem)
    yx = start_x + (w + gap) * 2
    y_mid = top_y + 45.0 * scale
    y_cx = yx + w / 2.0
    parts.append(
        f'<polygon points="{yx:.1f},{top_y:.1f} {yx + w:.1f},{top_y:.1f} {y_cx:.1f},{y_mid:.1f}" fill="{col}"/>'
        f'<rect x="{y_cx - thin/2:.2f}" y="{y_mid - 2*scale:.1f}" width="{thin:.2f}" height="{h - 43.0*scale:.1f}" fill="{col}"/>'
    )

    # 4. Letter T (thick top bar + thin center vertical stem)
    tx = start_x + (w + gap) * 3
    t_cx = tx + w / 2.0
    parts.append(
        f'<rect x="{tx:.1f}" y="{top_y:.1f}" width="{w:.1f}" height="{thick:.1f}" fill="{col}"/>'
        f'<rect x="{t_cx - thin/2:.2f}" y="{top_y:.1f}" width="{thin:.2f}" height="{h:.1f}" fill="{col}"/>'
    )

    # 5. Letter N (solid lower-left right triangle + thin right vertical stem)
    nx = start_x + (w + gap) * 4
    parts.append(
        f'<polygon points="{nx:.1f},{top_y:.1f} {nx:.1f},{top_y + h:.1f} {nx + w:.1f},{top_y + h:.1f}" fill="{col}"/>'
        f'<rect x="{nx + w - thin:.2f}" y="{top_y:.1f}" width="{thin:.2f}" height="{h:.1f}" fill="{col}"/>'
    )

    # 6. Letter X (hollow hourglass: two stroked triangles meeting at center)
    xx = start_x + (w + gap) * 5
    x_cx = xx + w / 2.0
    x_cy = top_y + h / 2.0
    pad = thin / 2.0
    parts.append(
        f'<polygon points="{xx + pad:.1f},{top_y + pad:.1f} {xx + w - pad:.1f},{top_y + pad:.1f} {x_cx:.1f},{x_cy:.1f}" '
        f'fill="none" stroke="{col}" stroke-width="{thin:.2f}" stroke-linejoin="miter"/>'
        f'<polygon points="{x_cx:.1f},{x_cy:.1f} {xx + pad:.1f},{top_y + h - pad:.1f} {xx + w - pad:.1f},{top_y + h - pad:.1f}" '
        f'fill="none" stroke="{col}" stroke-width="{thin:.2f}" stroke-linejoin="miter"/>'
    )

    return '<g class="sltynx-wordmark">' + "".join(parts) + "</g>"


def get_asset_base64(filename: str) -> str:
    """Reads an image file from source-assets/ and returns its base64 string."""
    path = SOURCE_ASSETS_DIR / filename
    if not path.exists():
        return ""
    return base64.b64encode(path.read_bytes()).decode("ascii")


def combine_into_single_terminal(sections: list[str], w: int, header_title: str, header_right: str = "") -> str:
    """
    Combines multiple section SVGs (Skills / Tools, Development Log & Story,
    Simulated Error & Repair, Knowledge Base, Trying to Understand) one after another
    into a single continuous terminal SVG with isolated CSS/IDs and no inner double-borders.
    """
    import re

    top_bar_h = 36
    y_offset = top_bar_h
    all_defs: list[str] = []
    all_styles: list[str] = []
    section_groups: list[str] = []

    for idx, raw_svg in enumerate(sections):
        prefix = f"u{idx}_"
        vb_match = re.search(r'viewBox="0 0 (\d+) (\d+)"', raw_svg)
        if not vb_match:
            continue
        sec_w = int(vb_match.group(1))
        sec_h = int(vb_match.group(2))

        # 1. Namespace IDs and url(#...)
        s = re.sub(r'\bid="([^"]+)"', rf'id="{prefix}\1"', raw_svg)
        s = re.sub(r'url\(#([^)]+)\)', rf'url(#{prefix}\1)', s)

        # 2. Namespace @keyframes and animation names
        kf_names = set(re.findall(r'@keyframes\s+([A-Za-z0-9_-]+)', s))
        for kfn in sorted(kf_names, key=len, reverse=True):
            s = re.sub(rf'\b{re.escape(kfn)}\b', f"{prefix}{kfn}", s)

        # 3. Namespace CSS classes inside <style> and class="..." (except mono/sans)
        style_match = re.search(r'<style>(.*?)</style>', s, re.S)
        if style_match:
            style_content = style_match.group(1)
            cls_names = set(re.findall(r'\.([A-Za-z_][A-Za-z0-9_-]*)', style_content)) - {"mono", "sans"}
            for cn in sorted(cls_names, key=len, reverse=True):
                style_content = re.sub(rf'\.{re.escape(cn)}\b', f".{prefix}{cn}", style_content)
                s = re.sub(
                    r'\bclass="([^"]*)"',
                    lambda m, c=cn, p=prefix: f'class="{re.sub(rf"(?<![A-Za-z0-9_-]){re.escape(c)}(?![A-Za-z0-9_-])", p + c, m.group(1))}"',
                    s,
                )
            style_content = re.sub(r'\.mono\s*\{[^}]*\}', '', style_content)
            style_content = re.sub(r'\.sans\s*\{[^}]*\}', '', style_content)
            all_styles.append(style_content.strip())

        for dm in re.finditer(r'<defs>(.*?)</defs>', s, flags=re.S):
            if dm.group(1).strip():
                all_defs.append(dm.group(1).strip())

        # 4. Extract inner content between <svg ...> and </svg>
        inner_start = s.find(">") + 1
        inner_end = s.rfind("</svg>")
        inner = s[inner_start:inner_end]
        inner = re.sub(r'<title>.*?</title>', '', inner, flags=re.S)
        inner = re.sub(r'<defs>.*?</defs>', '', inner, flags=re.S)
        inner = re.sub(r'<style>.*?</style>', '', inner, flags=re.S)

        # 5. Strip outer rounded border rects so sections stack seamlessly inside the single terminal
        inner = re.sub(
            rf'<rect x="0" y="0" width="{sec_w}" height="{sec_h}" rx="\d+" fill="{BG_PRIMARY}"/>',
            f'<rect x="0" y="0" width="{sec_w}" height="{sec_h}" fill="{BG_PRIMARY}"/>',
            inner,
        )
        inner = re.sub(
            rf'<rect x="1" y="1" width="{sec_w - 2}" height="{sec_h - 2}"[^>]*/>',
            f'<line x1="1" y1="0" x2="{sec_w - 1}" y2="0" stroke="{BORDER}" stroke-width="1.2"/>',
            inner,
        )
        # Make section header strip flush (rx="0") inside the unified terminal
        inner = re.sub(
            r'(<rect x="1\.5" y="1\.5" width="\d+" height="\d+") rx="\d+"',
            r'\1 rx="0"',
            inner,
        )

        section_groups.append(
            f'  <g transform="translate(0, {y_offset})">\n'
            f'{inner.strip()}\n'
            f'  </g>'
        )
        y_offset += sec_h

    total_h = y_offset
    right_tag = (
        f'<text x="{w - 20}" y="23" text-anchor="end" class="mono" font-size="11.5" fill="{TEXT_MUTED}">{header_right}</text>'
        if header_right
        else ""
    )

    return f'''<svg {SVG_NS} viewBox="0 0 {w} {total_h}" width="{w}" height="{total_h}" role="img" aria-label="SltyNX Unified Terminal — Skills, Development Log, Simulated Error and Repair, Knowledge Base, and Trying to Understand">
  <title>SltyNX — Unified Terminal Session</title>
  <defs>
    {chr(10).join(all_defs)}
  </defs>
  <style>
    .mono {{ font-family: {FONT_MONO}; }}
    .sans {{ font-family: {FONT_SANS}; }}
    {chr(10).join(all_styles)}
  </style>

  <!-- Single Master Terminal Background -->
  <rect x="0" y="0" width="{w}" height="{total_h}" rx="8" fill="{BG_PRIMARY}"/>

  <!-- Master Terminal Titlebar -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="{top_bar_h - 2}" rx="6" fill="{BG_SECONDARY}"/>
  <line x1="1" y1="{top_bar_h}" x2="{w - 1}" y2="{top_bar_h}" stroke="{BORDER}" stroke-width="1"/>
  <circle cx="20" cy="18.5" r="4.2" fill="{TEXT_DIM}"/>
  <circle cx="34" cy="18.5" r="4.2" fill="{TEXT_DIM}"/>
  <circle cx="48" cy="18.5" r="4.2" fill="{TEXT_DIM}"/>
  <text x="66" y="23" class="mono" font-size="12.5" font-weight="700" fill="{TEXT_PRIMARY}">{header_title}</text>
  {right_tag}

  <!-- Seamless Stacked Terminal Sections -->
{chr(10).join(section_groups)}

  <!-- Single Master Outer Terminal Border -->
  <rect x="1" y="1" width="{w - 2}" height="{total_h - 2}" rx="7" fill="none" stroke="{BORDER}" stroke-width="1.2"/>
</svg>
'''

