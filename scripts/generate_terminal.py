#!/usr/bin/env python3
"""
Generates the profile content, terminal storytelling, error-repair construction truck,
knowledge base, and funny quote SVGs — all optimized with a 640px responsive viewBox
and high-legibility typography (14px-24px) for crystal-clear mobile and desktop views:
- assets/profile-intro.svg
- assets/current-project.svg
- assets/skills-learning.svg
- assets/terminal-session.svg
- assets/ai-assistance.svg
- assets/error-repair.svg
- assets/knowledge-panel.svg
- assets/funny-quote.svg
"""
from __future__ import annotations
from html import escape
import pathlib

import config as C


def build_profile_intro() -> str:
    """
    Builds assets/profile-intro.svg (640x254) — Animated Terminal for Profile Introduction:
    Types out at large 15.5px-16.5px monospace:
      $ cat profile_intro.txt
      > Just a guy who sleeps a lot, codes a little,
        and dreams of building something cool.
      > Currently a noob developer. Learning as I go,
        breaking things occasionally, and trying to
        understand how everything works.
    """
    w, h = 640, 254

    intro_lines = [
        ("cmd", "$ cat profile_intro.txt", 68, 3, 12),
        ("pri", "> Just a guy who sleeps a lot, codes a little,", 104, 15, 30),
        ("pri", "  and dreams of building something cool.", 130, 30, 44),
        ("sec", "> Currently a noob developer. Learning as I go,", 166, 48, 63),
        ("sec", "  breaking things occasionally, and trying to", 192, 63, 77),
        ("sec", "  understand how everything works.", 218, 77, 88),
    ]

    clips: list[str] = []
    texts: list[str] = []
    css_rules: list[str] = []

    for idx, (kind, txt, y, t0, t1) in enumerate(intro_lines):
        col = C.TEXT_PRIMARY if kind in ("cmd", "pri") else C.TEXT_SECONDARY
        fsize = "16.5" if kind == "cmd" else "15.5"
        fweight = ' font-weight="700"' if kind == "cmd" else ""
        clips.append(
            f'<clipPath id="piClip{idx}">'
            f'<rect x="20" y="{y - 20}" width="600" height="28" class="piline{idx}"/>'
            f'</clipPath>'
        )
        texts.append(
            f'<text x="24" y="{y}" clip-path="url(#piClip{idx})" class="mono" font-size="{fsize}"{fweight} fill="{col}" xml:space="preserve">{escape(txt)}</text>'
        )
        css_rules.append(
            f".piline{idx} {{ animation: piType{idx} 12s steps(45, end) infinite; }}\n"
            f"    @keyframes piType{idx} {{\n"
            f"      0%, {t0}% {{ width: 0px; }}\n"
            f"      {t1}%, 94% {{ width: 600px; }}\n"
            f"      98%, 100% {{ width: 0px; }}\n"
            f"    }}"
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Profile Introduction Terminal: Just a guy who sleeps a lot, codes a little, and dreams of building something cool. Currently a noob developer. Learning as I go, breaking things occasionally, and trying to understand how everything works.">
  <title>Profile Introduction — SltyNX (Sleeping Core)</title>
  <defs>
    {"".join(clips)}
  </defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    {chr(10).join(css_rules)}
    .pi-cur {{ animation: piBlink 1s steps(2, start) infinite; }}
    @keyframes piBlink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .piline0, .piline1, .piline2, .piline3, .piline4, .piline5 {{ animation: none !important; width: 600px !important; }}
      .pi-cur {{ animation: none !important; opacity: 1 !important; }}
    }}
  </style>

  <!-- Outer Terminal Card Frame -->
  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Top Terminal Header Strip -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="36" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="38" x2="{w - 1}" y2="38" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="22" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <circle cx="38" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <circle cx="54" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <text x="74" y="24" class="mono" font-size="13.5" fill="{C.TEXT_SECONDARY}">sltynx@sleeping-core: ~/profile</text>
  <text x="{w - 20}" y="24" text-anchor="end" class="mono" font-size="13" fill="{C.TEXT_MUTED}">bio: Sleeping Core</text>

  <!-- Animated Terminal Typing Lines -->
  {"".join(texts)}

  <!-- Bottom Prompt & Blinking Cursor -->
  <text x="24" y="242" class="mono" font-size="15.5" fill="{C.TEXT_MUTED}">$ </text>
  <rect x="44" y="228" width="9" height="16" fill="{C.TEXT_PRIMARY}" class="pi-cur"/>
</svg>
'''


def build_current_project() -> str:
    """
    Builds assets/current-project.svg (640x316) — Section 9:
    Stacked mobile-friendly card with large 24px title, 16px description,
    status bar, and full-scale pixel-art Gnosis Keyboard illustration below.
    """
    w, h = 640, 316

    keys_svg: list[str] = []
    row1 = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]
    row2 = ["A", "S", "D", "F", "G", "H", "J", "K", "L"]
    row3 = ["Z", "X", "C", "V", "B", "N", "M"]

    highlight_keys = {"G": "0.2s", "N": "0.9s", "O": "1.6s", "S": "2.3s", "I": "3.0s"}

    # Centered keyboard frame at x=140..500 (width=360), y=194..302 (height=108)
    kb_x = 156
    kb_y = 204
    for idx, k in enumerate(row1):
        kx = kb_x + idx * 33
        ky = kb_y
        cls = ' class="key-press"' if k in highlight_keys else ""
        st = f' style="animation-delay:{highlight_keys[k]}"' if k in highlight_keys else ""
        keys_svg.append(
            f'<g{cls}{st}><rect x="{kx}" y="{ky}" width="29" height="21" rx="3.5" fill="{C.BG_ELEVATED}" stroke="{C.BORDER}" stroke-width="1.1"/>'
            f'<text x="{kx + 14.5}" y="{ky + 15}" text-anchor="middle" class="mono" font-size="11.5" font-weight="600" fill="{C.TEXT_SECONDARY}">{k}</text></g>'
        )
    for idx, k in enumerate(row2):
        kx = kb_x + 16 + idx * 33
        ky = kb_y + 25
        cls = ' class="key-press"' if k in highlight_keys else ""
        st = f' style="animation-delay:{highlight_keys[k]}"' if k in highlight_keys else ""
        keys_svg.append(
            f'<g{cls}{st}><rect x="{kx}" y="{ky}" width="29" height="21" rx="3.5" fill="{C.BG_ELEVATED}" stroke="{C.BORDER}" stroke-width="1.1"/>'
            f'<text x="{kx + 14.5}" y="{ky + 15}" text-anchor="middle" class="mono" font-size="11.5" font-weight="600" fill="{C.TEXT_SECONDARY}">{k}</text></g>'
        )
    for idx, k in enumerate(row3):
        kx = kb_x + 49 + idx * 33
        ky = kb_y + 50
        cls = ' class="key-press"' if k in highlight_keys else ""
        st = f' style="animation-delay:{highlight_keys[k]}"' if k in highlight_keys else ""
        keys_svg.append(
            f'<g{cls}{st}><rect x="{kx}" y="{ky}" width="29" height="21" rx="3.5" fill="{C.BG_ELEVATED}" stroke="{C.BORDER}" stroke-width="1.1"/>'
            f'<text x="{kx + 14.5}" y="{ky + 15}" text-anchor="middle" class="mono" font-size="11.5" font-weight="600" fill="{C.TEXT_SECONDARY}">{k}</text></g>'
        )
    keys_svg.append(
        f'<rect x="{kb_x}" y="{kb_y + 50}" width="44" height="21" rx="3.5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.1"/>'
        f'<text x="{kb_x + 22}" y="{kb_y + 64}" text-anchor="middle" class="mono" font-size="10" fill="{C.TEXT_MUTED}">SHIFT</text>'
        f'<rect x="{kb_x + 282}" y="{kb_y + 50}" width="44" height="21" rx="3.5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.1"/>'
        f'<text x="{kb_x + 304}" y="{kb_y + 64}" text-anchor="middle" class="mono" font-size="10" fill="{C.TEXT_MUTED}">DEL</text>'
        f'<rect x="{kb_x}" y="{kb_y + 75}" width="54" height="20" rx="3.5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.1"/>'
        f'<text x="{kb_x + 27}" y="{kb_y + 89}" text-anchor="middle" class="mono" font-size="10" fill="{C.TEXT_MUTED}">?123</text>'
        f'<rect x="{kb_x + 60}" y="{kb_y + 75}" width="196" height="20" rx="3.5" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_MUTED}" stroke-width="1.1"/>'
        f'<text x="{kb_x + 158}" y="{kb_y + 89}" text-anchor="middle" class="mono" font-size="10.5" font-weight="700" fill="{C.TEXT_PRIMARY}" letter-spacing="2.5">GNOSIS</text>'
        f'<rect x="{kb_x + 262}" y="{kb_y + 75}" width="64" height="20" rx="3.5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.1"/>'
        f'<text x="{kb_x + 294}" y="{kb_y + 89}" text-anchor="middle" class="mono" font-size="10" fill="{C.TEXT_SECONDARY}">ENTER</text>'
    )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Current Project: Gnosis Keyboard (In Progress)">
  <title>Current Projects — {escape(C.PROJECT_NAME)} ({escape(C.PROJECT_STATUS)})</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    .key-press rect {{ animation: keyTap 4s ease-in-out infinite; }}
    .key-press text {{ animation: keyText 4s ease-in-out infinite; }}
    @keyframes keyTap {{
      0%, 80%, 100% {{ fill: {C.BG_ELEVATED}; stroke: {C.BORDER}; }}
      10%, 25% {{ fill: {C.TEXT_PRIMARY}; stroke: {C.TEXT_PRIMARY}; }}
    }}
    @keyframes keyText {{
      0%, 80%, 100% {{ fill: {C.TEXT_SECONDARY}; }}
      10%, 25% {{ fill: {C.BG_PRIMARY}; font-weight: 700; }}
    }}
    .pulse-dot {{ animation: pDot 2.4s ease-in-out infinite; }}
    @keyframes pDot {{ 0%, 100% {{ opacity: 0.35; }} 50% {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .key-press rect, .key-press text, .pulse-dot {{ animation: none !important; }}
    }}
  </style>

  <!-- Card Background & Border -->
  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Section Header Strip -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="36" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="38" x2="{w - 1}" y2="38" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="20" y="25" class="mono" font-size="14.5" font-weight="700" fill="{C.TEXT_PRIMARY}">// Current Projects</text>
  <text x="{w - 20}" y="25" text-anchor="end" class="mono" font-size="13.5" fill="{C.TEXT_MUTED}">repo: {escape(C.PROJECT_REPO_NAME)}</text>

  <!-- Project Title & Status Badge -->
  <text x="22" y="74" class="sans" font-size="24" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(C.PROJECT_NAME)}</text>

  <rect x="226" y="53" width="128" height="28" rx="5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.1"/>
  <circle cx="242" cy="67" r="4" fill="{C.TEXT_PRIMARY}" class="pulse-dot"/>
  <text x="255" y="72" class="mono" font-size="13.5" font-weight="600" fill="{C.TEXT_PRIMARY}">{escape(C.PROJECT_STATUS)}</text>

  <!-- Description -->
  <text x="22" y="106" class="sans" font-size="16" fill="{C.TEXT_SECONDARY}">A custom Android keyboard focused on control, customization,</text>
  <text x="22" y="129" class="sans" font-size="16" fill="{C.TEXT_SECONDARY}">and a better typing experience.</text>

  <!-- Non-percentage Honest Development Status Bar -->
  <rect x="20" y="144" width="600" height="34" rx="5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.1"/>
  <text x="34" y="166" class="mono" font-size="14" fill="{C.TEXT_SECONDARY}">stage: active development</text>
  <text x="272" y="166" class="mono" font-size="14" fill="{C.TEXT_MUTED}">|</text>
  <text x="292" y="166" class="mono" font-size="14" font-weight="600" fill="{C.TEXT_PRIMARY}">repo: {escape(C.PROJECT_REPO_NAME)}</text>

  <!-- Centered Pixel-Art Keyboard Illustration -->
  <rect x="142" y="192" width="356" height="112" rx="7" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>
  {"".join(keys_svg)}
</svg>
'''


def build_skills_learning() -> str:
    """
    Builds assets/skills-learning.svg (640x436) — Section 10:
    Communicates honestly that SltyNX is a beginner currently learning step by step.
    Uses a spacious 2-column x 4-row grid (292px wide x 72px tall cards) inside a 640px
    viewBox with 13px-16px fonts and per-card clipPaths for mobile & desktop clarity.
    """
    w, h = 640, 436
    badges: list[str] = []
    clips: list[str] = []

    col_w = 292
    row_h = 72
    gap_x = 16
    gap_y = 12
    start_x = 20
    start_y = 92

    for idx, (title, desc, tag) in enumerate(C.LEARNING_ITEMS):
        r = idx // 2
        c = idx % 2
        bx = start_x + c * (col_w + gap_x)
        by = start_y + r * (row_h + gap_y)
        clips.append(
            f'<clipPath id="skCardClip{idx}">'
            f'<rect x="2" y="2" width="{col_w - 4}" height="{row_h - 4}" rx="5"/>'
            f'</clipPath>'
        )
        badges.append(
            f'<g transform="translate({bx}, {by})">'
            f'<rect x="0" y="0" width="{col_w}" height="{row_h}" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>'
            f'<g clip-path="url(#skCardClip{idx})">'
            f'<text x="14" y="27" class="mono" font-size="14" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(title)}</text>'
            f'<rect x="{col_w - 86}" y="9" width="76" height="22" rx="4" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1"/>'
            f'<text x="{col_w - 48}" y="24" text-anchor="middle" class="mono" font-size="11.5" fill="{C.TEXT_SECONDARY}">{escape(tag)}</text>'
            f'<text x="14" y="53" class="sans" font-size="13" fill="{C.TEXT_SECONDARY}">{escape(desc)}</text>'
            f'</g>'
            f'</g>'
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Skills and Tools — Beginner, Learning in Progress">
  <title>{escape(C.SKILLS_HEADING)} — {escape(C.SKILLS_LABEL)}</title>
  <defs>
    {"".join(clips)}
  </defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
  </style>

  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Top Header Strip -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="38" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="40" x2="{w - 1}" y2="40" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="20" y="26" class="mono" font-size="15" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(C.SKILLS_HEADING)}</text>

  <!-- Beginner — Learning in Progress Badge -->
  <rect x="346" y="7" width="276" height="26" rx="4" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1.1"/>
  <text x="484" y="25" text-anchor="middle" class="mono" font-size="13" font-weight="600" fill="{C.TEXT_PRIMARY}">{escape(C.SKILLS_LABEL)}</text>

  <!-- Honest Core Message -->
  <text x="20" y="70" class="sans" font-size="15.5" font-weight="600" fill="{C.TEXT_SECONDARY}">&#8220;{escape(C.SKILLS_MESSAGE)}&#8221;</text>

  <!-- 8 Outlined Learning Inventory Cards (2 cols x 4 rows) -->
  {"".join(badges)}
</svg>
'''


def build_terminal_session() -> str:
    """
    Builds assets/terminal-session.svg (640x420) — Section 11, Scenes A & B:
    Stacked vertical layout for high mobile visibility:
    Top (Scene A): Animated terminal typing at 16.5px monospace.
    Bottom (Scene B): Sleepy mascot sitting in front of laptop with '...what now?' thought bubble.
    """
    w, h = 640, 420

    clips: list[str] = []
    texts: list[str] = []

    line_timings = [
        (4, 14),   # $ start-project
        (18, 28),  # > opening the editor...
        (33, 44),  # > thinking of an idea...
        (49, 58),  # > no ideas found.
        (63, 75),  # > searching for motivation...
    ]

    for idx, ((kind, txt), (_t_start, _t_end)) in enumerate(zip(C.TERMINAL_SCENE_A_LINES, line_timings)):
        y = 74 + idx * 30
        col = C.TEXT_PRIMARY if kind == "cmd" else (C.TERM_ERROR if kind == "err" else C.TEXT_SECONDARY)
        fweight = ' font-weight="700"' if kind == "cmd" else ""
        clips.append(
            f'<clipPath id="tsClip{idx}">'
            f'<rect x="20" y="{y - 20}" width="580" height="28" class="tline{idx}"/>'
            f'</clipPath>'
        )
        texts.append(
            f'<text x="26" y="{y}" clip-path="url(#tsClip{idx})" class="mono" font-size="16"{fweight} fill="{col}">{escape(txt)}</text>'
        )

    line_css: list[str] = []
    for idx, (t_start, t_end) in enumerate(line_timings):
        line_css.append(
            f".tline{idx} {{ animation: typeL{idx} 12s steps(36, end) infinite; }}\n"
            f"    @keyframes typeL{idx} {{\n"
            f"      0%, {t_start}% {{ width: 0px; }}\n"
            f"      {t_end}%, 92% {{ width: 580px; }}\n"
            f"      96%, 100% {{ width: 0px; }}\n"
            f"    }}"
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Terminal Session — Starting Work and Running Out of Ideas (Scenes A and B)">
  <title>Terminal Session — Starting Work &amp; Running Out of Ideas (Scenes A &amp; B)</title>
  <defs>
    {"".join(clips)}
  </defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    {chr(10).join(line_css)}

    .thought-bubble {{ animation: bubbleShow 12s ease-in-out infinite; }}
    @keyframes bubbleShow {{
      0%, 54% {{ opacity: 0; transform: translateY(4px); }}
      60%, 92% {{ opacity: 1; transform: translateY(0px); }}
      96%, 100% {{ opacity: 0; transform: translateY(4px); }}
    }}

    .mascot-nod {{ animation: headNod 4s ease-in-out infinite; }}
    @keyframes headNod {{
      0%, 100% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(2.2px); }}
    }}

    .cur {{ animation: cBlink 1s steps(2, start) infinite; }}
    @keyframes cBlink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}

    @media (prefers-reduced-motion: reduce) {{
      .tline0, .tline1, .tline2, .tline3, .tline4 {{ animation: none !important; width: 580px !important; }}
      .thought-bubble {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
      .mascot-nod, .cur {{ animation: none !important; }}
    }}
  </style>

  <!-- Outer Frame -->
  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Top Terminal Header -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="36" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="38" x2="{w - 1}" y2="38" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="22" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <circle cx="38" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <circle cx="54" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <text x="74" y="24" class="mono" font-size="13.5" fill="{C.TEXT_SECONDARY}">sltynx@desk: ~/projects (scene 01 // running out of ideas)</text>

  <!-- =================================================================== -->
  <!-- SCENE A (TOP): Terminal Typing Sequence                             -->
  <!-- =================================================================== -->
  {"".join(texts)}

  <!-- Blinking Terminal Cursor -->
  <text x="26" y="220" class="mono" font-size="16" fill="{C.TEXT_MUTED}">$ </text>
  <rect x="46" y="206" width="9" height="16" fill="{C.TEXT_PRIMARY}" class="cur"/>

  <!-- Horizontal Divider -->
  <line x1="20" y1="234" x2="620" y2="234" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- =================================================================== -->
  <!-- SCENE B (BOTTOM): Sleepy Mascot at Laptop + "...what now?" Bubble   -->
  <!-- =================================================================== -->
  <rect x="20" y="246" width="600" height="156" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Desk Surface -->
  <line x1="40" y1="368" x2="596" y2="368" stroke="{C.BORDER}" stroke-width="1.5"/>

  <!-- Coffee Mug on Desk -->
  <rect x="148" y="346" width="20" height="22" rx="2.5" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_MUTED}" stroke-width="1.3"/>
  <path d="M 168 351 C 174 351, 174 363, 168 363" fill="none" stroke="{C.TEXT_MUTED}" stroke-width="1.3"/>

  <!-- Sleepy Mascot Sitting Behind Laptop -->
  <g class="mascot-nod">
    <rect x="278" y="326" width="48" height="42" rx="8" fill="#222222" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
    <circle cx="302" cy="296" r="27" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
    <path d="M 275 296 C 275 262, 329 262, 329 296 C 323 282, 312 286, 304 292 L 298 282 L 290 292 L 282 284 Z" fill="#1A1A1A" stroke="{C.TEXT_MUTED}" stroke-width="1.1"/>
    <line x1="290" y1="300" x2="298" y2="300" stroke="{C.BG_PRIMARY}" stroke-width="2.4" stroke-linecap="round"/>
    <line x1="306" y1="300" x2="314" y2="300" stroke="{C.BG_PRIMARY}" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M 322 290 Q 325 296 322 298 Q 319 296 322 290 Z" fill="{C.TEXT_SECONDARY}"/>
  </g>

  <!-- Laptop on Desk -->
  <polygon points="242,330 296,330 304,366 250,366" fill="#141414" stroke="{C.TEXT_SECONDARY}" stroke-width="1.3"/>
  <polygon points="273,344 269,351 277,351" fill="{C.TEXT_PRIMARY}"/>
  <rect x="246" y="364" width="76" height="4" rx="1.5" fill="{C.TEXT_SECONDARY}"/>

  <!-- Thought Bubble: "...what now?" -->
  <g class="thought-bubble">
    <circle cx="338" cy="278" r="3.5" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_SECONDARY}" stroke-width="1.1"/>
    <circle cx="352" cy="268" r="5" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_SECONDARY}" stroke-width="1.1"/>
    <rect x="364" y="252" width="166" height="40" rx="6" fill="{C.BG_PRIMARY}" stroke="{C.TEXT_SECONDARY}" stroke-width="1.3"/>
    <text x="447" y="277" text-anchor="middle" class="mono" font-size="15.5" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(C.MASCOT_THOUGHT_BUBBLE)}</text>
  </g>

  <text x="320" y="391" text-anchor="middle" class="mono" font-size="13" fill="{C.TEXT_MUTED}">status: staring at blank editor</text>
</svg>
'''


def build_ai_assistance() -> str:
    """
    Builds assets/ai-assistance.svg (640x436) — Section 11, Scenes C & D:
    Stacked mobile-first layout:
    Top (Scene C): 3 wide AI Reference cards (192px each) + notification popups.
    Middle (Scene D): Terminal output (> hint received, > trying to understand..., > implementing solution...).
    Bottom (Scene D): Focused mascot at laptop reading docs.
    """
    w, h = 640, 436

    service_cards: list[str] = []
    ai_clips: list[str] = []
    popups_svg: list[str] = []

    for idx, (name, sub) in enumerate(C.AI_SERVICES):
        sx = 20 + idx * 204
        sy = 50
        ai_clips.append(
            f'<clipPath id="aiCardClip{idx}"><rect x="{sx + 2}" y="{sy + 2}" width="188" height="54" rx="5"/></clipPath>'
            f'<clipPath id="aiPopClip{idx}"><rect x="{sx + 2}" y="118" width="188" height="28" rx="4"/></clipPath>'
        )
        if idx == 0:
            icon = f'<path d="M {sx+22} {sy+20} V {sy+38} M {sx+13} {sy+29} H {sx+31} M {sx+15} {sy+22} L {sx+29} {sy+36} M {sx+29} {sy+22} L {sx+15} {sy+36}" stroke="{C.TEXT_PRIMARY}" stroke-width="1.7"/>'
        elif idx == 1:
            icon = f'<polygon points="{sx+22},{sy+18} {sx+25.5},{sy+26} {sx+33.5},{sy+29} {sx+25.5},{sy+32} {sx+22},{sy+40} {sx+18.5},{sy+32} {sx+10.5},{sy+29} {sx+18.5},{sy+26}" fill="none" stroke="{C.TEXT_PRIMARY}" stroke-width="1.5"/>'
        else:
            icon = f'<polygon points="{sx+22},{sy+19} {sx+31},{sy+24} {sx+31},{sy+34} {sx+22},{sy+39} {sx+13},{sy+34} {sx+13},{sy+24}" fill="none" stroke="{C.TEXT_PRIMARY}" stroke-width="1.5"/>'

        service_cards.append(
            f'<g class="ai-node n{idx}">'
            f'<rect x="{sx}" y="{sy}" width="192" height="58" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>'
            f'<g clip-path="url(#aiCardClip{idx})">'
            f'{icon}'
            f'<text x="{sx + 40}" y="{sy + 25}" class="sans" font-size="14.5" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(name)}</text>'
            f'<text x="{sx + 40}" y="{sy + 44}" class="mono" font-size="11.5" fill="{C.TEXT_MUTED}">{escape(sub)}</text>'
            f'</g>'
            f'</g>'
        )

    for idx, ptext in enumerate(C.AI_POPUPS):
        px = 20 + idx * 204
        py = 116
        popups_svg.append(
            f'<g class="popup pop{idx}">'
            f'<rect x="{px}" y="{py}" width="192" height="32" rx="5" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_SECONDARY}" stroke-width="1.1" stroke-dasharray="3 2"/>'
            f'<g clip-path="url(#aiPopClip{idx})">'
            f'<rect x="{px + 12}" y="{py + 13}" width="6" height="6" fill="{C.TEXT_PRIMARY}"/>'
            f'<text x="{px + 24}" y="{py + 21}" class="mono" font-size="12.5" font-weight="600" fill="{C.TEXT_PRIMARY}">{escape(ptext)}</text>'
            f'</g>'
            f'</g>'
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Asking AI for Help and Implementing Solution (Scenes C and D)">
  <title>Terminal Session — Asking AI for Help &amp; Implementing Solution (Scenes C &amp; D)</title>
  <defs>
    {"".join(ai_clips)}
  </defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}

    .pop0 {{ animation: popSeq0 12s ease-in-out infinite; }}
    .pop1 {{ animation: popSeq1 12s ease-in-out infinite; }}
    .pop2 {{ animation: popSeq2 12s ease-in-out infinite; }}
    @keyframes popSeq0 {{
      0%, 5% {{ opacity: 0; transform: translateY(-4px); }}
      10%, 34% {{ opacity: 1; transform: translateY(0px); }}
      40%, 100% {{ opacity: 0.28; transform: translateY(0px); }}
    }}
    @keyframes popSeq1 {{
      0%, 22% {{ opacity: 0; transform: translateY(-4px); }}
      28%, 54% {{ opacity: 1; transform: translateY(0px); }}
      60%, 100% {{ opacity: 0.28; transform: translateY(0px); }}
    }}
    @keyframes popSeq2 {{
      0%, 40% {{ opacity: 0; transform: translateY(-4px); }}
      46%, 76% {{ opacity: 1; transform: translateY(0px); }}
      82%, 100% {{ opacity: 0.28; transform: translateY(0px); }}
    }}

    .resp0 {{ animation: rLine0 12s steps(24, end) infinite; }}
    .resp1 {{ animation: rLine1 12s steps(24, end) infinite; }}
    .resp2 {{ animation: rLine2 12s steps(24, end) infinite; }}
    @keyframes rLine0 {{ 0%, 48% {{ opacity: 0; }} 52%, 94% {{ opacity: 1; }} 98%, 100% {{ opacity: 0; }} }}
    @keyframes rLine1 {{ 0%, 60% {{ opacity: 0; }} 64%, 94% {{ opacity: 1; }} 98%, 100% {{ opacity: 0; }} }}
    @keyframes rLine2 {{ 0%, 72% {{ opacity: 0; }} 76%, 94% {{ opacity: 1; }} 98%, 100% {{ opacity: 0; }} }}

    .focus-badge {{ animation: rLine1 12s ease-in-out infinite; }}

    @media (prefers-reduced-motion: reduce) {{
      .pop0, .pop1, .pop2, .resp0, .resp1, .resp2, .focus-badge {{ animation: none !important; opacity: 1 !important; }}
    }}
  </style>

  <!-- Outer Frame -->
  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Top Terminal Header -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="36" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="38" x2="{w - 1}" y2="38" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="22" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <circle cx="38" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <circle cx="54" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <text x="74" y="24" class="mono" font-size="13.5" fill="{C.TEXT_SECONDARY}">sltynx@desk: ~/projects (scene 02 // asking AI for a hint)</text>

  <!-- SCENE C (TOP): Three AI Reference Nodes & Popups -->
  {"".join(service_cards)}
  {"".join(popups_svg)}

  <!-- SCENE D (MIDDLE): Terminal Assistance Output -->
  <rect x="20" y="160" width="600" height="106" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>
  <text x="36" y="189" class="mono resp0" font-size="16" font-weight="600" fill="{C.TERM_SUCCESS}">&gt; hint received</text>
  <text x="36" y="218" class="mono resp1" font-size="16" fill="{C.TEXT_PRIMARY}">&gt; trying to understand...</text>
  <text x="36" y="247" class="mono resp2" font-size="16" fill="{C.TEXT_SECONDARY}">&gt; implementing solution...</text>

  <!-- SCENE D (BOTTOM): Mascot Focusing & Typing at Laptop -->
  <rect x="20" y="278" width="600" height="140" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>
  <line x1="40" y1="386" x2="600" y2="386" stroke="{C.BORDER}" stroke-width="1.5"/>

  <g transform="translate(230, 326)">
    <rect x="-24" y="22" width="48" height="38" rx="8" fill="#242424" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
    <circle cx="0" cy="-6" r="25" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
    <path d="M -25 -6 C -25 -38, 25 -38, 25 -6 C 19 -20, 9 -16, 2 -10 L -4 -20 L -12 -10 L -19 -18 Z" fill="#1A1A1A" stroke="{C.TEXT_MUTED}" stroke-width="1.1"/>
    <line x1="-12" y1="-6" x2="-4" y2="-4" stroke="{C.BG_PRIMARY}" stroke-width="2" stroke-linecap="round"/>
    <line x1="4" y1="-4" x2="12" y2="-6" stroke="{C.BG_PRIMARY}" stroke-width="2" stroke-linecap="round"/>
    <circle cx="-8" cy="-1" r="2.2" fill="{C.BG_PRIMARY}"/>
    <circle cx="8" cy="-1" r="2.2" fill="{C.BG_PRIMARY}"/>
    <g class="focus-badge" stroke="{C.TEXT_PRIMARY}" stroke-width="1.5" stroke-linecap="round">
      <line x1="-36" y1="-20" x2="-30" y2="-16"/>
      <line x1="-38" y1="-10" x2="-31" y2="-9"/>
      <line x1="36" y1="-20" x2="30" y2="-16"/>
      <line x1="38" y1="-10" x2="31" y2="-9"/>
    </g>
  </g>

  <polygon points="166,350 220,350 228,384 174,384" fill="#161616" stroke="{C.TEXT_PRIMARY}" stroke-width="1.3"/>
  <rect x="170" y="382" width="76" height="4" rx="1.5" fill="{C.TEXT_SECONDARY}"/>

  <!-- Status Badge Next to Focused Mascot -->
  <rect x="304" y="314" width="268" height="36" rx="5" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1.2" class="focus-badge"/>
  <text x="438" y="337" text-anchor="middle" class="mono focus-badge" font-size="14" font-weight="600" fill="{C.TEXT_PRIMARY}">focus: reading the docs...</text>

  <text x="320" y="407" text-anchor="middle" class="mono" font-size="13" fill="{C.TEXT_MUTED}">status: actually making sense now</text>
</svg>
'''


def build_error_repair() -> str:
    """
    Builds assets/error-repair.svg (640x436) — Section 12:
    Error Animation — The AI Construction Truck.
    Stacked layout for high mobile visibility:
    Top: Simulated terminal error output + repair progress bar at 16px monospace.
    Bottom: Full-width dedicated repair track with puzzled mascot, ERR_01/FIXED module,
            miniature worker with animated wrench, and the [AI ASSIST] Construction Truck.
    """
    w, h = 640, 436

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Simulated Error Animation — The AI Construction Truck">
  <title>Error Animation — The AI Construction Truck (Simulated)</title>
  <defs>
    <clipPath id="truckLaneClip">
      <rect x="20" y="246" width="600" height="174" rx="6"/>
    </clipPath>
  </defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}

    .err-line {{ animation: showErr 14s linear infinite; }}
    @keyframes showErr {{
      0%, 4% {{ opacity: 0; }}
      6%, 92% {{ opacity: 1; }}
      97%, 100% {{ opacity: 0; }}
    }}

    .req-line {{ animation: showReq 14s linear infinite; }}
    @keyframes showReq {{
      0%, 16% {{ opacity: 0; }}
      20%, 92% {{ opacity: 1; }}
      97%, 100% {{ opacity: 0; }}
    }}

    .fix-line {{ animation: showFix 14s linear infinite; }}
    @keyframes showFix {{
      0%, 46% {{ opacity: 0; }}
      50%, 92% {{ opacity: 1; }}
      97%, 100% {{ opacity: 0; }}
    }}

    .ok-line {{ animation: showOk 14s linear infinite; }}
    @keyframes showOk {{
      0%, 68% {{ opacity: 0; }}
      72%, 92% {{ opacity: 1; }}
      97%, 100% {{ opacity: 0; }}
    }}

    .prog-fill {{ animation: progBar 14s ease-in-out infinite; }}
    @keyframes progBar {{
      0%, 46% {{ width: 0px; fill: {C.TEXT_MUTED}; }}
      68% {{ width: 320px; fill: {C.TEXT_PRIMARY}; }}
      72%, 92% {{ width: 320px; fill: {C.TERM_SUCCESS}; }}
      97%, 100% {{ width: 0px; }}
    }}

    .truck-rig {{ animation: truckDrive 14s ease-in-out infinite; }}
    @keyframes truckDrive {{
      0%, 20% {{ transform: translateX(320px); opacity: 0; }}
      24% {{ opacity: 1; }}
      36%, 74% {{ transform: translateX(0px); opacity: 1; }}
      88% {{ transform: translateX(-340px); opacity: 1; }}
      92%, 100% {{ transform: translateX(-360px); opacity: 0; }}
    }}

    .worker-fix {{ animation: workerAct 14s linear infinite; }}
    @keyframes workerAct {{
      0%, 36% {{ opacity: 0; }}
      40%, 68% {{ opacity: 1; }}
      72%, 100% {{ opacity: 0; }}
    }}

    .wrench-turn {{ animation: wrenchRot 0.8s ease-in-out infinite; transform-origin: 282px 352px; }}
    @keyframes wrenchRot {{
      0%, 100% {{ transform: rotate(-18deg); }}
      50% {{ transform: rotate(22deg); }}
    }}

    .warn-badge {{ animation: warnState 14s linear infinite; }}
    @keyframes warnState {{
      0%, 5% {{ opacity: 0; }}
      8%, 68% {{ opacity: 1; }}
      72%, 100% {{ opacity: 0; }}
    }}

    .fixed-badge {{ animation: showOk 14s linear infinite; }}

    @media (prefers-reduced-motion: reduce) {{
      .err-line, .req-line, .fix-line, .ok-line, .fixed-badge {{ animation: none !important; opacity: 1 !important; }}
      .warn-badge {{ display: none !important; }}
      .prog-fill {{ animation: none !important; width: 320px !important; fill: {C.TERM_SUCCESS} !important; }}
      .truck-rig {{ animation: none !important; transform: translateX(0px) !important; opacity: 1 !important; }}
      .worker-fix {{ animation: none !important; opacity: 1 !important; }}
      .wrench-turn {{ animation: none !important; }}
    }}
  </style>

  <!-- Outer Frame -->
  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Top Terminal Header -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="36" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="38" x2="{w - 1}" y2="38" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="22" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <circle cx="38" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <circle cx="54" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <text x="74" y="24" class="mono" font-size="13.5" fill="{C.TEXT_SECONDARY}">sltynx@desk: ~/debug-sim (error &amp; repair)</text>
  <text x="{w - 20}" y="24" text-anchor="end" class="mono" font-size="12.5" fill="{C.TEXT_MUTED}">[simulated]</text>

  <!-- TOP SECTION: Simulated Terminal Output & Progress Bar -->
  <text x="26" y="68" class="mono err-line" font-size="16" font-weight="700" fill="{C.TERM_ERROR}">! error: something went wrong</text>
  <text x="26" y="98" class="mono err-line" font-size="15.5" fill="{C.TEXT_SECONDARY}">&gt; diagnosis: developer confusion</text>
  <text x="26" y="128" class="mono req-line" font-size="15.5" fill="{C.TEXT_SECONDARY}">&gt; requesting assistance...</text>
  <text x="26" y="158" class="mono fix-line" font-size="15.5" fill="{C.TEXT_PRIMARY}">&gt; applying fix...</text>

  <g class="fix-line">
    <rect x="26" y="172" width="320" height="14" rx="4" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.1"/>
    <rect x="26" y="172" width="320" height="14" rx="4" fill="{C.TERM_SUCCESS}" class="prog-fill"/>
    <text x="358" y="184" class="mono" font-size="13" fill="{C.TEXT_MUTED}">repair_job</text>
  </g>

  <text x="26" y="216" class="mono ok-line" font-size="16" font-weight="700" fill="{C.TERM_SUCCESS}">&#10003; build successful (in this simulation)</text>

  <!-- Horizontal Separator -->
  <line x1="20" y1="234" x2="620" y2="234" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- BOTTOM SECTION: Puzzled Mascot + Pixel AI Construction Truck -->
  <rect x="20" y="246" width="600" height="174" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>

  <g clip-path="url(#truckLaneClip)">
    <!-- Puzzled Mascot Avatar on Left of Track -->
    <g transform="translate(92, 316)">
      <circle cx="0" cy="0" r="24" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
      <path d="M -24 0 C -24 -30, 24 -30, 24 0 C 17 -12, 5 -10, -2 -4 L -9 -14 L -16 -4 Z" fill="#1A1A1A"/>
      <line x1="-11" y1="2" x2="-4" y2="2" stroke="{C.BG_PRIMARY}" stroke-width="2.2"/>
      <line x1="4" y1="2" x2="11" y2="2" stroke="{C.BG_PRIMARY}" stroke-width="2.2"/>
      <text x="28" y="-8" class="mono warn-badge" font-size="16" font-weight="700" fill="{C.TEXT_SECONDARY}">?</text>
    </g>

    <!-- Error / Build Module Box on Work Track -->
    <g class="warn-badge">
      <rect x="196" y="302" width="76" height="48" rx="5" fill="#140C0C" stroke="{C.TERM_ERROR}" stroke-width="1.4"/>
      <polygon points="234,310 222,330 246,330" fill="none" stroke="{C.TERM_WARN}" stroke-width="1.5"/>
      <text x="234" y="328" text-anchor="middle" class="mono" font-size="11" font-weight="700" fill="{C.TERM_WARN}">!</text>
      <text x="234" y="344" text-anchor="middle" class="mono" font-size="10.5" font-weight="600" fill="{C.TERM_ERROR}">ERR_01</text>
    </g>

    <!-- Fixed Module State -->
    <g class="fixed-badge">
      <rect x="196" y="302" width="76" height="48" rx="5" fill="#0B140E" stroke="{C.TERM_SUCCESS}" stroke-width="1.4"/>
      <text x="234" y="327" text-anchor="middle" class="mono" font-size="15" font-weight="700" fill="{C.TERM_SUCCESS}">&#10003;</text>
      <text x="234" y="343" text-anchor="middle" class="mono" font-size="10.5" font-weight="700" fill="{C.TERM_SUCCESS}">FIXED</text>
    </g>

    <!-- Miniature Pixel Worker + Toolbox + Wrench -->
    <g class="worker-fix">
      <rect x="302" y="358" width="20" height="14" rx="1.5" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_SECONDARY}" stroke-width="1.1"/>
      <line x1="306" y1="358" x2="318" y2="358" stroke="{C.TEXT_PRIMARY}" stroke-width="2"/>
      <rect x="280" y="350" width="14" height="20" rx="2" fill="#2A2A2A" stroke="{C.TEXT_SECONDARY}" stroke-width="1.1"/>
      <circle cx="287" cy="342" r="7" fill="#E5E5E5"/>
      <path d="M 278 341 C 278 333, 296 333, 296 341 Z" fill="{C.TERM_WARN}"/>
      <g class="wrench-turn">
        <line x1="282" y1="352" x2="268" y2="334" stroke="{C.TEXT_PRIMARY}" stroke-width="2.4" stroke-linecap="round"/>
        <circle cx="267" cy="333" r="3.5" fill="none" stroke="{C.TEXT_PRIMARY}" stroke-width="1.6"/>
      </g>
      <text x="270" y="326" class="mono" font-size="12" fill="{C.TERM_WARN}">*</text>
      <text x="286" y="324" class="mono" font-size="11" fill="{C.TEXT_PRIMARY}">+</text>
    </g>

    <!-- Pixel-Art AI Construction Truck on Dedicated Track -->
    <g class="truck-rig">
      <rect x="376" y="302" width="136" height="36" rx="4" fill="{C.BG_PRIMARY}" stroke="{C.TERM_WARN}" stroke-width="1.4"/>
      <text x="444" y="325" text-anchor="middle" class="mono" font-size="13.5" font-weight="700" fill="{C.TEXT_PRIMARY}">[ AI ASSIST ]</text>

      <rect x="368" y="338" width="146" height="26" rx="2.5" fill="#1C1C1C" stroke="{C.TEXT_SECONDARY}" stroke-width="1.3"/>
      <line x1="378" y1="344" x2="384" y2="358" stroke="{C.TERM_WARN}" stroke-width="2.2"/>
      <line x1="392" y1="344" x2="398" y2="358" stroke="{C.TERM_WARN}" stroke-width="2.2"/>
      <line x1="406" y1="344" x2="412" y2="358" stroke="{C.TERM_WARN}" stroke-width="2.2"/>

      <polygon points="332,340 346,318 368,318 368,364 332,364" fill="#262626" stroke="{C.TEXT_PRIMARY}" stroke-width="1.3"/>
      <polygon points="338,338 348,322 364,322 364,338" fill="#090909" stroke="{C.BORDER}" stroke-width="1"/>
      <rect x="351" y="311" width="9" height="6" rx="1.5" fill="{C.TERM_WARN}"/>

      <circle cx="352" cy="366" r="10" fill="#0A0A0A" stroke="{C.TEXT_SECONDARY}" stroke-width="2.2"/>
      <circle cx="352" cy="366" r="3.5" fill="{C.TEXT_PRIMARY}"/>
      <circle cx="410" cy="366" r="10" fill="#0A0A0A" stroke="{C.TEXT_SECONDARY}" stroke-width="2.2"/>
      <circle cx="410" cy="366" r="3.5" fill="{C.TEXT_PRIMARY}"/>
      <circle cx="482" cy="366" r="10" fill="#0A0A0A" stroke="{C.TEXT_SECONDARY}" stroke-width="2.2"/>
      <circle cx="482" cy="366" r="3.5" fill="{C.TEXT_PRIMARY}"/>
    </g>

    <!-- Dedicated Ground Track Line -->
    <line x1="36" y1="377" x2="604" y2="377" stroke="{C.BORDER}" stroke-width="1.5" stroke-dasharray="6 4"/>
    <text x="320" y="402" text-anchor="middle" class="mono" font-size="13" fill="{C.TEXT_MUTED}">lane: emergency_patch_unit.exe // demonstration only</text>
  </g>
</svg>
'''


def build_knowledge_panel() -> str:
    """
    Builds assets/knowledge-panel.svg (640x360) — Section 13:
    Knowledge Base — Notes, experiments, and things I'm learning.
    Stacked layout for mobile & desktop legibility:
    Top: File explorer directory (learning-notes/, experiments/, project-references/, ideas/).
    Bottom: Restrained archive opening animation (> extracting knowledge..., > still learning...).
    """
    w, h = 640, 360
    dir_rows: list[str] = []
    for idx, (dname, ddesc, _path) in enumerate(C.KNOWLEDGE_DIRS):
        ry = 94 + idx * 32
        dir_rows.append(
            f'<g transform="translate(24, {ry})">'
            f'<rect x="0" y="-14" width="16" height="13" rx="2" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>'
            f'<path d="M 0 -12 H 7 L 9 -14 H 0 Z" fill="{C.TEXT_SECONDARY}"/>'
            f'<text x="26" y="-2" class="mono" font-size="15" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(dname)}</text>'
            f'<text x="218" y="-2" class="sans" font-size="14" fill="{C.TEXT_SECONDARY}">// {escape(ddesc)}</text>'
            f'</g>'
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Knowledge Base — Notes, experiments, and things I am learning">
  <title>{escape(C.KNOWLEDGE_TITLE)} — {escape(C.KNOWLEDGE_SUBTITLE)}</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    .zip-bar {{ animation: zipLoad 8s ease-in-out infinite; }}
    @keyframes zipLoad {{
      0%, 10% {{ width: 24px; }}
      55%, 88% {{ width: 320px; }}
      96%, 100% {{ width: 24px; }}
    }}
    .zip-step2 {{ animation: zStep2 8s linear infinite; }}
    @keyframes zStep2 {{
      0%, 40% {{ opacity: 0.25; }}
      50%, 90% {{ opacity: 1; }}
      96%, 100% {{ opacity: 0.25; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .zip-bar {{ animation: none !important; width: 280px !important; }}
      .zip-step2 {{ animation: none !important; opacity: 1 !important; }}
    }}
  </style>

  <!-- Outer Frame -->
  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Header Strip -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="36" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="38" x2="{w - 1}" y2="38" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="20" y="25" class="mono" font-size="14.5" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(C.KNOWLEDGE_TITLE)}</text>
  <text x="164" y="25" class="sans" font-size="14" fill="{C.TEXT_SECONDARY}">&#8212; {escape(C.KNOWLEDGE_SUBTITLE)}</text>

  <!-- Top Explorer Tree -->
  <text x="24" y="64" class="mono" font-size="13.5" fill="{C.TEXT_MUTED}">~/knowledge-base/</text>
  {"".join(dir_rows)}

  <!-- Bottom Archive Extraction Visual Concept -->
  <rect x="20" y="222" width="600" height="120" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Pixel ZIP Archive Icon -->
  <g transform="translate(40, 240)">
    <rect x="0" y="0" width="32" height="38" rx="3.5" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_PRIMARY}" stroke-width="1.3"/>
    <line x1="16" y1="2" x2="16" y2="24" stroke="{C.TEXT_SECONDARY}" stroke-width="3.2" stroke-dasharray="2.5 2.5"/>
    <rect x="11" y="24" width="10" height="7" fill="{C.TEXT_PRIMARY}"/>
  </g>
  <text x="86" y="257" class="mono" font-size="15" font-weight="700" fill="{C.TEXT_PRIMARY}">notes-archive.zip</text>
  <text x="86" y="276" class="mono" font-size="12.5" fill="{C.TEXT_MUTED}">[concept preview]</text>

  <!-- Loading Indicator -->
  <rect x="256" y="246" width="340" height="12" rx="4" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1.1"/>
  <rect x="256" y="246" width="280" height="12" rx="4" fill="{C.TEXT_PRIMARY}" class="zip-bar"/>

  <!-- Extraction Status Lines -->
  <text x="40" y="306" class="mono" font-size="14.5" fill="{C.TEXT_SECONDARY}">&gt; extracting knowledge...</text>
  <text x="310" y="306" class="mono zip-step2" font-size="14.5" font-weight="600" fill="{C.TEXT_PRIMARY}">&gt; still learning...</text>
</svg>
'''


def build_funny_quote() -> str:
    """
    Builds assets/funny-quote.svg (640x256) — Section 14:
    Trying to Understand.
    Uses the confused mascot from 31595634885785270.jpg (confused-mascot.jpg),
    hand-drawn question marks, and a spacious speech bubble in a 640px viewBox
    so the quote renders large and legible on mobile and desktop:
    "When I say Ehh, ehhh, ehhhh... like for three time, don't give up on me bro, I'm trying to understand it for real."
    """
    w, h = 640, 256
    confused_b64 = C.get_asset_base64("confused-mascot.jpg")
    mascot_img_tag = ""
    if confused_b64:
        mascot_img_tag = (
            f'<image href="data:image/jpeg;base64,{confused_b64}" '
            f'x="34" y="58" width="148" height="148" preserveAspectRatio="xMidYMid slice" '
            f'clip-path="url(#confusedClip)"/>'
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Trying to Understand: When I say Ehh, ehhh, ehhhh... like for three time, don't give up on me bro, I'm trying to understand it for real.">
  <title>Trying to Understand</title>
  <defs>
    <clipPath id="confusedClip">
      <rect x="34" y="58" width="148" height="148" rx="8"/>
    </clipPath>
  </defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}

    .head-tilt {{ animation: tilt 5s ease-in-out infinite; transform-origin: 108px 132px; }}
    @keyframes tilt {{
      0%, 100% {{ transform: rotate(0deg); }}
      50% {{ transform: rotate(-2.2deg); }}
    }}

    .q1 {{ animation: qPop1 6s ease-in-out infinite; transform-origin: 24px 68px; }}
    .q2 {{ animation: qPop2 6s ease-in-out infinite; transform-origin: 192px 64px; }}
    .q3 {{ animation: qPop3 6s ease-in-out infinite; transform-origin: 200px 104px; }}
    @keyframes qPop1 {{
      0%, 12%, 100% {{ opacity: 0.25; transform: scale(0.9); }}
      22%, 78% {{ opacity: 1; transform: scale(1.06); }}
    }}
    @keyframes qPop2 {{
      0%, 24%, 100% {{ opacity: 0.25; transform: scale(0.9); }}
      34%, 82% {{ opacity: 1; transform: scale(1.06); }}
    }}
    @keyframes qPop3 {{
      0%, 36%, 100% {{ opacity: 0.25; transform: scale(0.9); }}
      46%, 86% {{ opacity: 0.9; transform: scale(1.04); }}
    }}

    .quote-fade {{ animation: qReveal 6s ease-in-out infinite; }}
    @keyframes qReveal {{
      0% {{ opacity: 0.55; }}
      18%, 92% {{ opacity: 1; }}
      100% {{ opacity: 0.55; }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      .head-tilt, .q1, .q2, .q3, .quote-fade {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
    }}
  </style>

  <!-- Outer Frame -->
  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Top Header Strip -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="36" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="38" x2="{w - 1}" y2="38" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="20" y="25" class="mono" font-size="14.5" font-weight="700" fill="{C.TEXT_PRIMARY}">// Trying to Understand</text>
  <text x="{w - 20}" y="25" text-anchor="end" class="mono" font-size="13" fill="{C.TEXT_MUTED}">mood: confused_concentration.jpg</text>

  <!-- Left Side: Confused Mascot Reference -->
  <g class="head-tilt">
    <rect x="33" y="57" width="150" height="150" rx="9" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1.2"/>
    {mascot_img_tag}
  </g>

  <!-- Hand-drawn SVG Question Marks & Doodle Marks -->
  <g class="q1" fill="none" stroke="{C.TEXT_PRIMARY}" stroke-width="2" stroke-linecap="round">
    <path d="M 14 62 C 14 54, 26 54, 26 62 C 26 67, 20 68, 20 73"/>
    <circle cx="20" cy="79" r="1.4" fill="{C.TEXT_PRIMARY}"/>
  </g>
  <g class="q2" fill="none" stroke="{C.TEXT_PRIMARY}" stroke-width="2" stroke-linecap="round">
    <path d="M 190 60 C 190 52, 202 52, 202 60 C 202 65, 196 66, 196 71"/>
    <circle cx="196" cy="77" r="1.4" fill="{C.TEXT_PRIMARY}"/>
  </g>
  <g class="q3" fill="none" stroke="{C.TEXT_SECONDARY}" stroke-width="1.7" stroke-linecap="round">
    <path d="M 196 96 C 196 90, 205 90, 205 96 C 205 100, 200 101, 200 105"/>
    <circle cx="200" cy="110" r="1.2" fill="{C.TEXT_SECONDARY}"/>
    <line x1="188" y1="124" x2="195" y2="122"/>
    <line x1="189" y1="130" x2="197" y2="130"/>
  </g>

  <!-- Right Side: Speech Bubble with 3 Large Lines of Verbatim Text -->
  <g class="quote-fade">
    <path d="M 224 58 H 612 A 8 8 0 0 1 620 66 V 202 A 8 8 0 0 1 612 210 H 224 A 8 8 0 0 1 216 202 V 144 L 198 134 L 216 124 V 66 A 8 8 0 0 1 224 58 Z"
          fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.3"/>

    <text x="236" y="96" class="sans" font-size="16.5" font-weight="700" fill="{C.TEXT_PRIMARY}">
      &#8220;When I say Ehh, ehhh, ehhhh...
    </text>
    <text x="236" y="124" class="sans" font-size="16.5" font-weight="700" fill="{C.TEXT_PRIMARY}">
      like for three time, don&apos;t give up on me bro,
    </text>
    <text x="236" y="152" class="sans" font-size="16.5" font-weight="700" fill="{C.TEXT_PRIMARY}">
      I&apos;m trying to understand it for real.&#8221;
    </text>
    <text x="236" y="186" class="mono" font-size="12" fill="{C.TEXT_MUTED}">
      {escape(C.FUNNY_QUOTE_CAPTION)}
    </text>
  </g>
</svg>
'''


def generate_all() -> dict[str, pathlib.Path]:
    C.ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "profile-intro.svg": build_profile_intro(),
        "current-project.svg": build_current_project(),
        "skills-learning.svg": build_skills_learning(),
        "terminal-session.svg": build_terminal_session(),
        "ai-assistance.svg": build_ai_assistance(),
        "error-repair.svg": build_error_repair(),
        "knowledge-panel.svg": build_knowledge_panel(),
        "funny-quote.svg": build_funny_quote(),
    }
    written: dict[str, pathlib.Path] = {}
    for name, content in outputs.items():
        out_path = C.ASSETS_DIR / name
        out_path.write_text(content, encoding="utf-8")
        written[name] = out_path
    return written


if __name__ == "__main__":
    for k, p in generate_all().items():
        print(f"wrote {k:24s} ({p.stat().st_size:,} bytes)")
