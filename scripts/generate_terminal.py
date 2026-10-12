#!/usr/bin/env python3
"""
Generates the profile content, terminal storytelling, error-repair construction truck,
knowledge base, and funny quote SVGs:
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


def build_current_project() -> str:
    """
    Builds assets/current-project.svg (880x185) — Section 9:
    Gnosis Keyboard (In Progress), description, repository path,
    original pixel-art Android keyboard illustration, and honest non-percentage status indicator.
    """
    w, h = 880, 185

    # Build a small pixel-art keyboard on the right side (x=590..844, y=42..152)
    keys_svg: list[str] = []
    row1 = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]
    row2 = ["A", "S", "D", "F", "G", "H", "J", "K", "L"]
    row3 = ["Z", "X", "C", "V", "B", "N", "M"]

    # Highlight specific keys ("G", "N", "O", "S", "I") with subtle sequential key-press animation
    highlight_keys = {"G": "0.2s", "N": "0.9s", "O": "1.6s", "S": "2.3s", "I": "3.0s"}

    for idx, k in enumerate(row1):
        kx = 602 + idx * 23
        ky = 58
        cls = ' class="key-press"' if k in highlight_keys else ""
        st = f' style="animation-delay:{highlight_keys[k]}"' if k in highlight_keys else ""
        keys_svg.append(
            f'<g{cls}{st}><rect x="{kx}" y="{ky}" width="20" height="20" rx="3" fill="{C.BG_ELEVATED}" stroke="{C.BORDER}" stroke-width="1"/>'
            f'<text x="{kx + 10}" y="{ky + 14}" text-anchor="middle" class="mono" font-size="9.5" fill="{C.TEXT_SECONDARY}">{k}</text></g>'
        )
    for idx, k in enumerate(row2):
        kx = 613 + idx * 23
        ky = 82
        cls = ' class="key-press"' if k in highlight_keys else ""
        st = f' style="animation-delay:{highlight_keys[k]}"' if k in highlight_keys else ""
        keys_svg.append(
            f'<g{cls}{st}><rect x="{kx}" y="{ky}" width="20" height="20" rx="3" fill="{C.BG_ELEVATED}" stroke="{C.BORDER}" stroke-width="1"/>'
            f'<text x="{kx + 10}" y="{ky + 14}" text-anchor="middle" class="mono" font-size="9.5" fill="{C.TEXT_SECONDARY}">{k}</text></g>'
        )
    for idx, k in enumerate(row3):
        kx = 636 + idx * 23
        ky = 106
        cls = ' class="key-press"' if k in highlight_keys else ""
        st = f' style="animation-delay:{highlight_keys[k]}"' if k in highlight_keys else ""
        keys_svg.append(
            f'<g{cls}{st}><rect x="{kx}" y="{ky}" width="20" height="20" rx="3" fill="{C.BG_ELEVATED}" stroke="{C.BORDER}" stroke-width="1"/>'
            f'<text x="{kx + 10}" y="{ky + 14}" text-anchor="middle" class="mono" font-size="9.5" fill="{C.TEXT_SECONDARY}">{k}</text></g>'
        )
    # Modifier keys & Spacebar
    keys_svg.append(
        f'<rect x="602" y="106" width="30" height="20" rx="3" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>'
        f'<text x="617" y="119" text-anchor="middle" class="mono" font-size="8.5" fill="{C.TEXT_MUTED}">SHIFT</text>'
        f'<rect x="800" y="106" width="30" height="20" rx="3" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>'
        f'<text x="815" y="119" text-anchor="middle" class="mono" font-size="8.5" fill="{C.TEXT_MUTED}">DEL</text>'
        f'<rect x="602" y="130" width="38" height="18" rx="3" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>'
        f'<text x="621" y="142" text-anchor="middle" class="mono" font-size="8" fill="{C.TEXT_MUTED}">?123</text>'
        f'<rect x="644" y="130" width="136" height="18" rx="3" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_MUTED}" stroke-width="1"/>'
        f'<text x="712" y="142" text-anchor="middle" class="mono" font-size="8.5" fill="{C.TEXT_PRIMARY}" letter-spacing="2">GNOSIS</text>'
        f'<rect x="784" y="130" width="46" height="18" rx="3" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>'
        f'<text x="807" y="142" text-anchor="middle" class="mono" font-size="8" fill="{C.TEXT_SECONDARY}">ENTER</text>'
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
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Section Header Strip -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="32" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="34" x2="{w - 1}" y2="34" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="24" y="22" class="mono" font-size="12" font-weight="700" fill="{C.TEXT_PRIMARY}">// Current Projects</text>
  <text x="{w - 24}" y="22" text-anchor="end" class="mono" font-size="11" fill="{C.TEXT_MUTED}">repo: {escape(C.PROJECT_REPO_NAME)}</text>

  <!-- Left Content Area -->
  <!-- Project Title & Status Badge -->
  <text x="24" y="68" class="sans" font-size="20" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(C.PROJECT_NAME)}</text>

  <rect x="198" y="50" width="106" height="24" rx="4" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="212" cy="62" r="3.5" fill="{C.TEXT_PRIMARY}" class="pulse-dot"/>
  <text x="224" y="66" class="mono" font-size="11" fill="{C.TEXT_PRIMARY}">{escape(C.PROJECT_STATUS)}</text>

  <!-- Description (2 clean lines within left column) -->
  <text x="24" y="98" class="sans" font-size="13.5" fill="{C.TEXT_SECONDARY}">A custom Android keyboard focused on control, customization,</text>
  <text x="24" y="118" class="sans" font-size="13.5" fill="{C.TEXT_SECONDARY}">and a better typing experience.</text>

  <!-- Non-percentage Honest Development Status Bar -->
  <rect x="24" y="136" width="520" height="28" rx="4" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="36" y="154" class="mono" font-size="11.5" fill="{C.TEXT_SECONDARY}">stage: active development</text>
  <text x="230" y="154" class="mono" font-size="11.5" fill="{C.TEXT_MUTED}">|</text>
  <text x="246" y="154" class="mono" font-size="11.5" fill="{C.TEXT_PRIMARY}">github.com/SltyNX/Gnosis-Keyboard-Data &#8594;</text>

  <!-- Vertical Divider -->
  <line x1="568" y1="34" x2="568" y2="184" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Right Pixel-Art Keyboard Illustration -->
  <rect x="590" y="46" width="252" height="114" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
  {"".join(keys_svg)}
</svg>
'''


def build_skills_learning() -> str:
    """
    Builds assets/skills-learning.svg (880x215) — Section 10:
    Communicates honestly that SltyNX is a beginner currently learning step by step.
    No fake proficiency percentages or circular skill meters.
    """
    w, h = 880, 215
    badges: list[str] = []

    # 2 rows x 4 columns of compact outlined badges
    col_w = 200
    row_h = 54
    gap_x = 12
    gap_y = 12
    start_x = 22
    start_y = 86

    for idx, (title, desc, tag) in enumerate(C.LEARNING_ITEMS):
        r = idx // 4
        c = idx % 4
        bx = start_x + c * (col_w + gap_x)
        by = start_y + r * (row_h + gap_y)
        badges.append(
            f'<g transform="translate({bx}, {by})">'
            f'<rect x="0" y="0" width="{col_w}" height="{row_h}" rx="5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>'
            f'<text x="12" y="21" class="mono" font-size="11.5" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(title)}</text>'
            f'<text x="{col_w - 10}" y="20" text-anchor="end" class="mono" font-size="9.5" fill="{C.TEXT_MUTED}">[{escape(tag)}]</text>'
            f'<text x="12" y="39" class="sans" font-size="10.5" fill="{C.TEXT_SECONDARY}">{escape(desc)}</text>'
            f'</g>'
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Skills and Tools — Beginner, Learning in Progress">
  <title>{escape(C.SKILLS_HEADING)} — {escape(C.SKILLS_LABEL)}</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
  </style>

  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Top Header Strip -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="34" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="36" x2="{w - 1}" y2="36" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="24" y="23" class="mono" font-size="13" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(C.SKILLS_HEADING)}</text>

  <!-- Beginner — Learning in Progress Badge -->
  <rect x="614" y="6" width="244" height="22" rx="4" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="736" y="21" text-anchor="middle" class="mono" font-size="11" fill="{C.TEXT_PRIMARY}">{escape(C.SKILLS_LABEL)}</text>

  <!-- Honest Core Message -->
  <text x="24" y="64" class="sans" font-size="13.5" fill="{C.TEXT_SECONDARY}">&#8220;{escape(C.SKILLS_MESSAGE)}&#8221;</text>
  <text x="{w - 24}" y="64" text-anchor="end" class="mono" font-size="11" fill="{C.TEXT_MUTED}">// no fake proficiency meters</text>

  <!-- 8 Compact Outlined Learning Inventory Badges -->
  {"".join(badges)}
</svg>
'''


def build_terminal_session() -> str:
    """
    Builds assets/terminal-session.svg (880x280) — Section 11, Scenes A & B:
    Scene A (Left): Animated terminal typing:
      $ start-project
      > opening the editor...
      > thinking of an idea...
      > no ideas found.
      > searching for motivation...
    Scene B (Right): Sleepy mascot sitting in front of a laptop, pausing with '...what now?' thought bubble.
    """
    w, h = 880, 280

    # Build line-by-line / character-by-character clipPath reveal animations over a 12s cycle
    clips: list[str] = []
    texts: list[str] = []

    line_timings = [
        (4, 14),   # $ start-project
        (18, 28),  # > opening the editor...
        (33, 44),  # > thinking of an idea...
        (49, 58),  # > no ideas found.
        (63, 75),  # > searching for motivation...
    ]

    for idx, ((kind, txt), (t_start, t_end)) in enumerate(zip(C.TERMINAL_SCENE_A_LINES, line_timings)):
        y = 78 + idx * 34
        col = C.TEXT_PRIMARY if kind == "cmd" else (C.TERM_ERROR if kind == "err" else C.TEXT_SECONDARY)
        clips.append(
            f'<clipPath id="tsClip{idx}">'
            f'<rect x="24" y="{y - 18}" width="460" height="26" class="tline{idx}"/>'
            f'</clipPath>'
        )
        texts.append(
            f'<text x="28" y="{y}" clip-path="url(#tsClip{idx})" class="mono" font-size="13.5" fill="{col}">{escape(txt)}</text>'
        )

    line_css: list[str] = []
    for idx, (t_start, t_end) in enumerate(line_timings):
        line_css.append(
            f".tline{idx} {{ animation: typeL{idx} 12s steps(28, end) infinite; }}\n"
            f"    @keyframes typeL{idx} {{\n"
            f"      0%, {t_start - 0.5:.1f}% {{ width: 0px; }}\n"
            f"      {t_end:.1f}%, 92% {{ width: 460px; }}\n"
            f"      97%, 100% {{ width: 0px; }}\n"
            f"    }}"
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Animated Terminal Session — Scene A and Scene B: Running Out of Ideas">
  <title>Terminal Session — A Developer Running Out of Ideas (Scenes A &amp; B)</title>
  <defs>
    {"".join(clips)}
  </defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    {"    ".join(line_css)}
    .cur {{ animation: blink 1s steps(1) infinite; }}
    @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}

    .thought-bubble {{ animation: bubbleShow 12s ease-in-out infinite; }}
    @keyframes bubbleShow {{
      0%, 52% {{ opacity: 0; transform: translateY(4px); }}
      58%, 90% {{ opacity: 1; transform: translateY(0px); }}
      96%, 100% {{ opacity: 0; transform: translateY(4px); }}
    }}

    .mascot-nod {{ animation: mNod 6s ease-in-out infinite; transform-origin: 684px 175px; }}
    @keyframes mNod {{
      0%, 100% {{ transform: rotate(0deg); }}
      50% {{ transform: rotate(-2deg); }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      .tline0, .tline1, .tline2, .tline3, .tline4 {{ animation: none !important; width: 460px !important; }}
      .thought-bubble {{ animation: none !important; opacity: 1 !important; }}
      .mascot-nod, .cur {{ animation: none !important; }}
    }}
  </style>

  <!-- Outer Frame -->
  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Top Terminal Bar -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="32" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="34" x2="{w - 1}" y2="34" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="20" cy="17.5" r="4" fill="{C.TEXT_DIM}"/>
  <circle cx="34" cy="17.5" r="4" fill="{C.TEXT_DIM}"/>
  <circle cx="48" cy="17.5" r="4" fill="{C.TEXT_DIM}"/>
  <text x="68" y="22" class="mono" font-size="11.5" fill="{C.TEXT_SECONDARY}">sltynx@desk: ~/projects (scene 01 // running out of ideas)</text>

  <!-- =================================================================== -->
  <!-- SCENE A (LEFT): Terminal Typing Sequence                            -->
  <!-- =================================================================== -->
  {"".join(texts)}

  <!-- Blinking Terminal Cursor on bottom prompt line -->
  <text x="28" y="246" class="mono" font-size="13.5" fill="{C.TEXT_MUTED}">$ </text>
  <rect x="44" y="233" width="8" height="15" fill="{C.TEXT_PRIMARY}" class="cur"/>

  <!-- Vertical Divider -->
  <line x1="516" y1="34" x2="516" y2="279" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- =================================================================== -->
  <!-- SCENE B (RIGHT): Sleepy Mascot at Laptop + "...what now?" Bubble    -->
  <!-- =================================================================== -->
  <rect x="536" y="48" width="324" height="214" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Desk Surface -->
  <line x1="548" y1="224" x2="848" y2="224" stroke="{C.BORDER}" stroke-width="1.5"/>

  <!-- Coffee Mug on Desk -->
  <rect x="572" y="206" width="16" height="18" rx="2" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_MUTED}" stroke-width="1.2"/>
  <path d="M 588 210 C 593 210, 593 220, 588 220" fill="none" stroke="{C.TEXT_MUTED}" stroke-width="1.2"/>

  <!-- Sleepy Mascot Sitting Behind Laptop -->
  <g class="mascot-nod">
    <!-- Torso -->
    <rect x="658" y="182" width="48" height="42" rx="8" fill="#222222" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
    <!-- Chibi Head & Dark Bangs -->
    <circle cx="682" cy="152" r="26" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
    <path d="M 655 152 C 655 118, 709 118, 709 152 C 703 138, 692 142, 684 148 L 678 138 L 670 148 L 662 140 Z" fill="#1A1A1A" stroke="{C.TEXT_MUTED}" stroke-width="1.1"/>
    <!-- Sleepy / Blank Expression Eyes Looking at Screen -->
    <line x1="670" y1="156" x2="678" y2="156" stroke="{C.BG_PRIMARY}" stroke-width="2.4" stroke-linecap="round"/>
    <line x1="686" y1="156" x2="694" y2="156" stroke="{C.BG_PRIMARY}" stroke-width="2.4" stroke-linecap="round"/>
    <!-- Small sweat drop -->
    <path d="M 702 146 Q 705 152 702 154 Q 699 152 702 146 Z" fill="{C.TEXT_SECONDARY}"/>
  </g>

  <!-- Laptop on Desk in Front of Mascot -->
  <polygon points="622,186 676,186 684,222 630,222" fill="#141414" stroke="{C.TEXT_SECONDARY}" stroke-width="1.3"/>
  <!-- Glowing Apple/Logo dot on laptop lid -->
  <polygon points="653,200 649,207 657,207" fill="{C.TEXT_PRIMARY}"/>
  <!-- Laptop Base -->
  <rect x="626" y="220" width="76" height="4" rx="1.5" fill="{C.TEXT_SECONDARY}"/>

  <!-- Thought Bubble: "...what now?" -->
  <g class="thought-bubble">
    <circle cx="716" cy="122" r="3" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
    <circle cx="726" cy="110" r="4.5" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
    <rect x="724" y="66" width="122" height="34" rx="6" fill="{C.BG_PRIMARY}" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
    <text x="785" y="88" text-anchor="middle" class="mono" font-size="12.5" fill="{C.TEXT_PRIMARY}">{escape(C.MASCOT_THOUGHT_BUBBLE)}</text>
  </g>

  <text x="698" y="248" text-anchor="middle" class="mono" font-size="10.5" fill="{C.TEXT_MUTED}">status: staring at blank editor</text>
</svg>
'''


def build_ai_assistance() -> str:
    """
    Builds assets/ai-assistance.svg (880x285) — Section 11, Scenes C & D:
    Scene C: Asking AI for help (Claude — Sonnet, Gemini, ChatGPT) + sequential dot-matrix
             notification popups ('asking for a hint...', 'idea detected?', 'trying again...').
    Scene D: Terminal response ('> hint received', '> trying to understand...', '> implementing solution...')
             with mascot looking focused.
    """
    w, h = 880, 285

    # Three AI service cards across top-left (x=24..510, y=50..112)
    service_cards: list[str] = []
    for idx, (name, sub) in enumerate(C.AI_SERVICES):
        sx = 24 + idx * 164
        sy = 50
        # Distinct neutral geometric symbol per service (asterisk, 4-point star, hex node)
        if idx == 0:
            icon = f'<path d="M {sx+22} {sy+18} V {sy+34} M {sx+14} {sy+26} H {sx+30} M {sx+16} {sy+20} L {sx+28} {sy+32} M {sx+28} {sy+20} L {sx+16} {sy+32}" stroke="{C.TEXT_PRIMARY}" stroke-width="1.5"/>'
        elif idx == 1:
            icon = f'<polygon points="{sx+22},{sy+16} {sx+25},{sy+23} {sx+32},{sy+26} {sx+25},{sy+29} {sx+22},{sy+36} {sx+19},{sy+29} {sx+12},{sy+26} {sx+19},{sy+23}" fill="none" stroke="{C.TEXT_PRIMARY}" stroke-width="1.4"/>'
        else:
            icon = f'<polygon points="{sx+22},{sy+17} {sx+30},{sy+21.5} {sx+30},{sy+30.5} {sx+22},{sy+35} {sx+14},{sy+30.5} {sx+14},{sy+21.5}" fill="none" stroke="{C.TEXT_PRIMARY}" stroke-width="1.4"/>'

        service_cards.append(
            f'<g class="ai-node n{idx}">'
            f'<rect x="{sx}" y="{sy}" width="152" height="52" rx="5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>'
            f'{icon}'
            f'<text x="{sx + 40}" y="{sy + 23}" class="sans" font-size="12" font-weight="600" fill="{C.TEXT_PRIMARY}">{escape(name)}</text>'
            f'<text x="{sx + 40}" y="{sy + 39}" class="mono" font-size="9.5" fill="{C.TEXT_MUTED}">{escape(sub)}</text>'
            f'</g>'
        )

    # Sequential dot-matrix notification popups (y=118..148)
    popups_svg: list[str] = []
    for idx, ptext in enumerate(C.AI_POPUPS):
        px = 24 + idx * 164
        py = 114
        popups_svg.append(
            f'<g class="popup pop{idx}">'
            f'<rect x="{px}" y="{py}" width="152" height="28" rx="4" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_SECONDARY}" stroke-width="1" stroke-dasharray="3 2"/>'
            f'<rect x="{px + 10}" y="{py + 11}" width="5" height="5" fill="{C.TEXT_PRIMARY}"/>'
            f'<text x="{px + 22}" y="{py + 18}" class="mono" font-size="10.5" fill="{C.TEXT_PRIMARY}">{escape(ptext)}</text>'
            f'</g>'
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Asking AI for Help and Implementing Solution (Scenes C and D)">
  <title>Terminal Session — Asking AI for Help &amp; Implementing Solution (Scenes C &amp; D)</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}

    .pop0 {{ animation: popSeq0 12s ease-in-out infinite; }}
    .pop1 {{ animation: popSeq1 12s ease-in-out infinite; }}
    .pop2 {{ animation: popSeq2 12s ease-in-out infinite; }}
    @keyframes popSeq0 {{
      0%, 5% {{ opacity: 0; transform: translateY(-4px); }}
      10%, 34% {{ opacity: 1; transform: translateY(0px); }}
      40%, 100% {{ opacity: 0.25; transform: translateY(0px); }}
    }}
    @keyframes popSeq1 {{
      0%, 22% {{ opacity: 0; transform: translateY(-4px); }}
      28%, 54% {{ opacity: 1; transform: translateY(0px); }}
      60%, 100% {{ opacity: 0.25; transform: translateY(0px); }}
    }}
    @keyframes popSeq2 {{
      0%, 40% {{ opacity: 0; transform: translateY(-4px); }}
      46%, 76% {{ opacity: 1; transform: translateY(0px); }}
      82%, 100% {{ opacity: 0.25; transform: translateY(0px); }}
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
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Top Terminal Header -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="32" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="34" x2="{w - 1}" y2="34" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="20" cy="17.5" r="4" fill="{C.TEXT_DIM}"/>
  <circle cx="34" cy="17.5" r="4" fill="{C.TEXT_DIM}"/>
  <circle cx="48" cy="17.5" r="4" fill="{C.TEXT_DIM}"/>
  <text x="68" y="22" class="mono" font-size="11.5" fill="{C.TEXT_SECONDARY}">sltynx@desk: ~/projects (scene 02 // asking AI for a hint)</text>

  <!-- =================================================================== -->
  <!-- SCENE C (LEFT TOP): Three AI Reference Nodes & Dot-Matrix Popups    -->
  <!-- =================================================================== -->
  {"".join(service_cards)}
  {"".join(popups_svg)}

  <!-- =================================================================== -->
  <!-- SCENE D (LEFT BOTTOM): Terminal Assistance Output                   -->
  <!-- =================================================================== -->
  <rect x="24" y="154" width="480" height="110" rx="5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="38" y="182" class="mono resp0" font-size="13.5" fill="{C.TERM_SUCCESS}">&gt; hint received</text>
  <text x="38" y="210" class="mono resp1" font-size="13.5" fill="{C.TEXT_PRIMARY}">&gt; trying to understand...</text>
  <text x="38" y="238" class="mono resp2" font-size="13.5" fill="{C.TEXT_SECONDARY}">&gt; implementing solution...</text>

  <!-- Vertical Divider -->
  <line x1="524" y1="34" x2="524" y2="284" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- =================================================================== -->
  <!-- SCENE D (RIGHT): Mascot Focusing & Typing at Laptop                 -->
  <!-- =================================================================== -->
  <rect x="544" y="50" width="312" height="214" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <line x1="556" y1="224" x2="844" y2="224" stroke="{C.BORDER}" stroke-width="1.5"/>

  <!-- Focused Mascot Leaning Forward Slightly -->
  <g transform="translate(692, 160)">
    <!-- Torso leaning in -->
    <rect x="-24" y="22" width="48" height="42" rx="8" fill="#242424" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
    <!-- Head -->
    <circle cx="0" cy="-8" r="26" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
    <path d="M -27 -8 C -27 -42, 27 -42, 27 -8 C 21 -22, 10 -18, 2 -12 L -4 -22 L -12 -12 L -20 -20 Z" fill="#1A1A1A" stroke="{C.TEXT_MUTED}" stroke-width="1.1"/>
    <!-- Focused Determined Eyes & Brows -->
    <line x1="-13" y1="-8" x2="-4" y2="-6" stroke="{C.BG_PRIMARY}" stroke-width="2" stroke-linecap="round"/>
    <line x1="4" y1="-6" x2="13" y2="-8" stroke="{C.BG_PRIMARY}" stroke-width="2" stroke-linecap="round"/>
    <circle cx="-8" cy="-3" r="2.2" fill="{C.BG_PRIMARY}"/>
    <circle cx="8" cy="-3" r="2.2" fill="{C.BG_PRIMARY}"/>
    <!-- Small Focus Marks Around Head -->
    <g class="focus-badge" stroke="{C.TEXT_PRIMARY}" stroke-width="1.4" stroke-linecap="round">
      <line x1="-38" y1="-22" x2="-32" y2="-18"/>
      <line x1="-40" y1="-12" x2="-33" y2="-11"/>
      <line x1="38" y1="-22" x2="32" y2="-18"/>
      <line x1="40" y1="-12" x2="33" y2="-11"/>
    </g>
  </g>

  <!-- Laptop on Desk -->
  <polygon points="628,186 682,186 690,222 636,222" fill="#161616" stroke="{C.TEXT_PRIMARY}" stroke-width="1.3"/>
  <rect x="632" y="220" width="76" height="4" rx="1.5" fill="{C.TEXT_SECONDARY}"/>

  <!-- Status Badge Above Mascot -->
  <rect x="598" y="66" width="204" height="26" rx="4" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1" class="focus-badge"/>
  <text x="700" y="83" text-anchor="middle" class="mono focus-badge" font-size="11" fill="{C.TEXT_PRIMARY}">focus: reading the docs...</text>

  <text x="700" y="248" text-anchor="middle" class="mono" font-size="10.5" fill="{C.TEXT_MUTED}">status: actually making sense now</text>
</svg>
'''


def build_error_repair() -> str:
    """
    Builds assets/error-repair.svg (880x275) — Section 12:
    Error Animation — The AI Construction Truck.
    1. Terminal displays simulated error message:
       ! error: something went wrong
       > diagnosis: developer confusion
       > requesting assistance...
       > applying fix...
       ✓ build successful (in this simulation)
    2. Warning indicator appears, mascot looks confused.
    3. Pixel-art construction truck carrying an [AI ASSIST] sign drives in along a dedicated
       bottom repair lane (never overlapping terminal text or exceeding bounds).
    4. Miniature worker inspects the error with wrench/repair sparks.
    5. Progress indicator completes and simulated fixed state appears.
    """
    w, h = 880, 275

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Simulated Error Animation — The AI Construction Truck">
  <title>Error Animation — The AI Construction Truck (Simulated)</title>
  <defs>
    <clipPath id="truckLaneClip">
      <rect x="432" y="42" width="434" height="222" rx="6"/>
    </clipPath>
  </defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}

    /* 14s deterministic error and construction truck repair loop */
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
    @keyframes fixLine {{
      0%, 46% {{ opacity: 0; }}
      50%, 92% {{ opacity: 1; }}
      97%, 100% {{ opacity: 0; }}
    }}
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
      68% {{ width: 220px; fill: {C.TEXT_PRIMARY}; }}
      72%, 92% {{ width: 220px; fill: {C.TERM_SUCCESS}; }}
      97%, 100% {{ width: 0px; }}
    }}

    /* Truck drives in from right (x=320 offset -> x=0 stop -> exits left) */
    .truck-rig {{ animation: truckDrive 14s ease-in-out infinite; }}
    @keyframes truckDrive {{
      0%, 20% {{ transform: translateX(280px); opacity: 0; }}
      24% {{ opacity: 1; }}
      36%, 74% {{ transform: translateX(0px); opacity: 1; }}
      88% {{ transform: translateX(-290px); opacity: 1; }}
      92%, 100% {{ transform: translateX(-310px); opacity: 0; }}
    }}

    /* Worker and wrench repair action while truck is parked (38% - 68%) */
    .worker-fix {{ animation: workerAct 14s linear infinite; }}
    @keyframes workerAct {{
      0%, 36% {{ opacity: 0; }}
      40%, 68% {{ opacity: 1; }}
      72%, 100% {{ opacity: 0; }}
    }}

    .wrench-turn {{ animation: wrenchRot 0.8s ease-in-out infinite; transform-origin: 572px 192px; }}
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
      .prog-fill {{ animation: none !important; width: 220px !important; fill: {C.TERM_SUCCESS} !important; }}
      .truck-rig {{ animation: none !important; transform: translateX(0px) !important; opacity: 1 !important; }}
      .worker-fix {{ animation: none !important; opacity: 1 !important; }}
      .wrench-turn {{ animation: none !important; }}
    }}
  </style>

  <!-- Outer Frame -->
  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Top Terminal Header -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="32" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="34" x2="{w - 1}" y2="34" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="20" cy="17.5" r="4" fill="{C.TEXT_DIM}"/>
  <circle cx="34" cy="17.5" r="4" fill="{C.TEXT_DIM}"/>
  <circle cx="48" cy="17.5" r="4" fill="{C.TEXT_DIM}"/>
  <text x="68" y="22" class="mono" font-size="11.5" fill="{C.TEXT_SECONDARY}">sltynx@desk: ~/debug-simulation (error &amp; repair demo)</text>
  <text x="{w - 24}" y="22" text-anchor="end" class="mono" font-size="10.5" fill="{C.TEXT_MUTED}">[simulated sequence]</text>

  <!-- =================================================================== -->
  <!-- LEFT SIDE (24..412): Simulated Terminal Output & Progress Bar       -->
  <!-- =================================================================== -->
  <text x="28" y="68" class="mono err-line" font-size="13.5" font-weight="600" fill="{C.TERM_ERROR}">! error: something went wrong</text>
  <text x="28" y="98" class="mono err-line" font-size="13" fill="{C.TEXT_SECONDARY}">&gt; diagnosis: developer confusion</text>
  <text x="28" y="128" class="mono req-line" font-size="13" fill="{C.TEXT_SECONDARY}">&gt; requesting assistance...</text>
  <text x="28" y="158" class="mono fix-line" font-size="13" fill="{C.TEXT_PRIMARY}">&gt; applying fix...</text>

  <!-- Simulated Repair Progress Bar -->
  <g class="fix-line">
    <rect x="28" y="174" width="220" height="12" rx="3" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
    <rect x="28" y="174" width="220" height="12" rx="3" fill="{C.TERM_SUCCESS}" class="prog-fill"/>
    <text x="258" y="184" class="mono" font-size="11" fill="{C.TEXT_MUTED}">repair_job</text>
  </g>

  <!-- Restrained Simulated Success Line -->
  <text x="28" y="218" class="mono ok-line" font-size="13.5" font-weight="600" fill="{C.TERM_SUCCESS}">&#10003; build successful (in this simulation)</text>
  <text x="28" y="248" class="mono" font-size="10.5" fill="{C.TEXT_MUTED}">// demonstration only &#8212; no real build harmed</text>

  <!-- Vertical Separator -->
  <line x1="420" y1="34" x2="420" y2="274" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- =================================================================== -->
  <!-- RIGHT SIDE (432..866): Puzzled Mascot + Pixel AI Construction Truck -->
  <!-- =================================================================== -->
  <rect x="432" y="42" width="434" height="220" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>

  <g clip-path="url(#truckLaneClip)">
    <!-- Top Section inside Right Panel: Puzzled Mascot + Error Module Box -->
    <!-- Small Puzzled Mascot Avatar -->
    <g transform="translate(480, 96)">
      <circle cx="0" cy="0" r="20" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
      <path d="M -20 0 C -20 -26, 20 -26, 20 0 C 14 -10, 4 -8, -2 -4 L -8 -12 L -14 -4 Z" fill="#1A1A1A"/>
      <line x1="-9" y1="2" x2="-3" y2="2" stroke="{C.BG_PRIMARY}" stroke-width="2"/>
      <line x1="3" y1="2" x2="9" y2="2" stroke="{C.BG_PRIMARY}" stroke-width="2"/>
      <text x="24" y="-8" class="mono warn-badge" font-size="13" font-weight="700" fill="{C.TEXT_SECONDARY}">?</text>
    </g>

    <!-- Error / Build Module Box on Work Track -->
    <g class="warn-badge">
      <rect x="520" y="138" width="66" height="42" rx="4" fill="#140C0C" stroke="{C.TERM_ERROR}" stroke-width="1.3"/>
      <polygon points="553,146 543,164 563,164" fill="none" stroke="{C.TERM_WARN}" stroke-width="1.4"/>
      <text x="553" y="162" text-anchor="middle" class="mono" font-size="10" font-weight="700" fill="{C.TERM_WARN}">!</text>
      <text x="553" y="175" text-anchor="middle" class="mono" font-size="8.5" fill="{C.TERM_ERROR}">ERR_01</text>
    </g>

    <!-- Fixed Module State -->
    <g class="fixed-badge">
      <rect x="520" y="138" width="66" height="42" rx="4" fill="#0B140E" stroke="{C.TERM_SUCCESS}" stroke-width="1.3"/>
      <text x="553" y="160" text-anchor="middle" class="mono" font-size="13" font-weight="700" fill="{C.TERM_SUCCESS}">&#10003;</text>
      <text x="553" y="174" text-anchor="middle" class="mono" font-size="8.5" fill="{C.TERM_SUCCESS}">FIXED</text>
    </g>

    <!-- Miniature Pixel Worker + Toolbox + Wrench Inspecting the Problem -->
    <g class="worker-fix">
      <!-- Red/Grey Pixel Toolbox -->
      <rect x="588" y="198" width="18" height="12" rx="1" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
      <line x1="592" y1="198" x2="602" y2="198" stroke="{C.TEXT_PRIMARY}" stroke-width="2"/>
      <!-- Worker body -->
      <rect x="570" y="190" width="12" height="18" rx="2" fill="#2A2A2A" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
      <!-- Worker head & safety hard-hat -->
      <circle cx="576" cy="183" r="6" fill="#E5E5E5"/>
      <path d="M 568 182 C 568 175, 584 175, 584 182 Z" fill="{C.TERM_WARN}"/>
      <!-- Animated Wrench & Sparks -->
      <g class="wrench-turn">
        <line x1="572" y1="192" x2="560" y2="176" stroke="{C.TEXT_PRIMARY}" stroke-width="2.2" stroke-linecap="round"/>
        <circle cx="559" cy="175" r="3" fill="none" stroke="{C.TEXT_PRIMARY}" stroke-width="1.5"/>
      </g>
      <text x="562" y="168" class="mono" font-size="10" fill="{C.TERM_WARN}">*</text>
      <text x="576" y="166" class="mono" font-size="9" fill="{C.TEXT_PRIMARY}">+</text>
    </g>

    <!-- Pixel-Art AI Construction Truck on Dedicated Track -->
    <g class="truck-rig">
      <!-- Cargo Signboard: [ AI ASSIST ] -->
      <rect x="652" y="148" width="114" height="32" rx="3" fill="{C.BG_PRIMARY}" stroke="{C.TERM_WARN}" stroke-width="1.3"/>
      <text x="709" y="168" text-anchor="middle" class="mono" font-size="11" font-weight="700" fill="{C.TEXT_PRIMARY}">[ AI ASSIST ]</text>

      <!-- Truck Bed / Chassis -->
      <rect x="646" y="180" width="124" height="24" rx="2" fill="#1C1C1C" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
      <!-- Hazard stripes on bumper -->
      <line x1="654" y1="186" x2="660" y2="198" stroke="{C.TERM_WARN}" stroke-width="2"/>
      <line x1="666" y1="186" x2="672" y2="198" stroke="{C.TERM_WARN}" stroke-width="2"/>
      <line x1="678" y1="186" x2="684" y2="198" stroke="{C.TERM_WARN}" stroke-width="2"/>

      <!-- Truck Cab (Facing Left toward the error module) -->
      <polygon points="614,182 626,162 646,162 646,204 614,204" fill="#262626" stroke="{C.TEXT_PRIMARY}" stroke-width="1.2"/>
      <!-- Cab Window -->
      <polygon points="619,180 628,166 642,166 642,180" fill="#090909" stroke="{C.BORDER}" stroke-width="1"/>
      <!-- Amber Roof Beacon -->
      <rect x="631" y="156" width="8" height="5" rx="1.5" fill="{C.TERM_WARN}"/>

      <!-- Wheels -->
      <circle cx="632" cy="206" r="9" fill="#0A0A0A" stroke="{C.TEXT_SECONDARY}" stroke-width="2"/>
      <circle cx="632" cy="206" r="3" fill="{C.TEXT_PRIMARY}"/>
      <circle cx="682" cy="206" r="9" fill="#0A0A0A" stroke="{C.TEXT_SECONDARY}" stroke-width="2"/>
      <circle cx="682" cy="206" r="3" fill="{C.TEXT_PRIMARY}"/>
      <circle cx="744" cy="206" r="9" fill="#0A0A0A" stroke="{C.TEXT_SECONDARY}" stroke-width="2"/>
      <circle cx="744" cy="206" r="3" fill="{C.TEXT_PRIMARY}"/>
    </g>

    <!-- Dedicated Ground Track Line -->
    <line x1="444" y1="216" x2="854" y2="216" stroke="{C.BORDER}" stroke-width="1.5" stroke-dasharray="6 4"/>
    <text x="649" y="244" text-anchor="middle" class="mono" font-size="10.5" fill="{C.TEXT_MUTED}">lane: emergency_patch_unit.exe</text>
  </g>
</svg>
'''


def build_knowledge_panel() -> str:
    """
    Builds assets/knowledge-panel.svg (880x220) — Section 13:
    Knowledge Base — Notes, experiments, and things I'm learning.
    Left: File explorer / terminal directory (learning-notes/, experiments/, project-references/, ideas/).
    Right: Restrained archive opening animation ending with:
      > extracting knowledge...
      > still learning...
    """
    w, h = 880, 220
    dir_rows: list[str] = []
    for idx, (dname, ddesc, _path) in enumerate(C.KNOWLEDGE_DIRS):
        ry = 86 + idx * 30
        dir_rows.append(
            f'<g transform="translate(28, {ry})">'
            f'<rect x="0" y="-12" width="14" height="11" rx="1.5" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_SECONDARY}" stroke-width="1.1"/>'
            f'<path d="M 0 -10 H 6 L 8 -12 H 0 Z" fill="{C.TEXT_SECONDARY}"/>'
            f'<text x="22" y="-2" class="mono" font-size="12.5" font-weight="600" fill="{C.TEXT_PRIMARY}">{escape(dname)}</text>'
            f'<text x="186" y="-2" class="sans" font-size="12" fill="{C.TEXT_SECONDARY}">// {escape(ddesc)}</text>'
            f'</g>'
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Knowledge Base — Notes, experiments, and things I am learning">
  <title>{escape(C.KNOWLEDGE_TITLE)} — {escape(C.KNOWLEDGE_SUBTITLE)}</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    .zip-bar {{ animation: zipLoad 8s ease-in-out infinite; }}
    @keyframes zipLoad {{
      0%, 10% {{ width: 18px; }}
      55%, 88% {{ width: 224px; }}
      96%, 100% {{ width: 18px; }}
    }}
    .zip-step2 {{ animation: zStep2 8s linear infinite; }}
    @keyframes zStep2 {{
      0%, 40% {{ opacity: 0.25; }}
      50%, 90% {{ opacity: 1; }}
      96%, 100% {{ opacity: 0.25; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .zip-bar {{ animation: none !important; width: 180px !important; }}
      .zip-step2 {{ animation: none !important; opacity: 1 !important; }}
    }}
  </style>

  <!-- Outer Frame -->
  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Header Strip -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="32" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="34" x2="{w - 1}" y2="34" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="24" y="22" class="mono" font-size="12.5" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(C.KNOWLEDGE_TITLE)}</text>
  <text x="150" y="22" class="sans" font-size="12" fill="{C.TEXT_SECONDARY}">&#8212; {escape(C.KNOWLEDGE_SUBTITLE)}</text>

  <!-- Left Explorer Tree -->
  <text x="28" y="56" class="mono" font-size="11.5" fill="{C.TEXT_MUTED}">~/knowledge-base/</text>
  {"".join(dir_rows)}

  <!-- Vertical Separator -->
  <line x1="556" y1="34" x2="556" y2="219" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Right Side: Archive Extraction Visual Concept -->
  <rect x="576" y="48" width="280" height="154" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Pixel ZIP Archive Icon -->
  <g transform="translate(596, 64)">
    <rect x="0" y="0" width="28" height="34" rx="3" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_PRIMARY}" stroke-width="1.2"/>
    <line x1="14" y1="2" x2="14" y2="22" stroke="{C.TEXT_SECONDARY}" stroke-width="3" stroke-dasharray="2 2"/>
    <rect x="10" y="22" width="8" height="6" fill="{C.TEXT_PRIMARY}"/>
  </g>
  <text x="636" y="79" class="mono" font-size="12" font-weight="600" fill="{C.TEXT_PRIMARY}">notes-archive.zip</text>
  <text x="636" y="95" class="mono" font-size="10.5" fill="{C.TEXT_MUTED}">[concept preview]</text>

  <!-- Loading Indicator -->
  <rect x="596" y="112" width="240" height="10" rx="3" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <rect x="596" y="112" width="180" height="10" rx="3" fill="{C.TEXT_PRIMARY}" class="zip-bar"/>

  <!-- Extraction Status Lines -->
  <text x="596" y="150" class="mono" font-size="12" fill="{C.TEXT_SECONDARY}">&gt; extracting knowledge...</text>
  <text x="596" y="174" class="mono zip-step2" font-size="12" fill="{C.TEXT_PRIMARY}">&gt; still learning...</text>
</svg>
'''


def build_funny_quote() -> str:
    """
    Builds assets/funny-quote.svg (880x230) — Section 14:
    Trying to Understand.
    Uses the confused mascot from 31595634885785270.jpg (confused-mascot.jpg),
    adds 2-3 hand-drawn question marks with a subtle pop, tiny thoughtful head tilt,
    and restrained speech bubble displaying:
    "When I say Ehh, ehhh, ehhhh... like for the third time, don't give up on me bro, I'm trying to understand it for real."
    """
    w, h = 880, 230
    confused_b64 = C.get_asset_base64("confused-mascot.jpg")
    mascot_img_tag = ""
    if confused_b64:
        mascot_img_tag = (
            f'<image href="data:image/jpeg;base64,{confused_b64}" '
            f'x="44" y="48" width="144" height="144" preserveAspectRatio="xMidYMid slice" '
            f'clip-path="url(#confusedClip)"/>'
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Trying to Understand: When I say Ehh, ehhh, ehhhh... like for the third time, don't give up on me bro, I'm trying to understand it for real.">
  <title>Trying to Understand</title>
  <defs>
    <clipPath id="confusedClip">
      <rect x="44" y="48" width="144" height="144" rx="8"/>
    </clipPath>
  </defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}

    .head-tilt {{ animation: tilt 5s ease-in-out infinite; transform-origin: 116px 120px; }}
    @keyframes tilt {{
      0%, 100% {{ transform: rotate(0deg); }}
      50% {{ transform: rotate(-2.2deg); }}
    }}

    .q1 {{ animation: qPop1 6s ease-in-out infinite; transform-origin: 34px 62px; }}
    .q2 {{ animation: qPop2 6s ease-in-out infinite; transform-origin: 198px 58px; }}
    .q3 {{ animation: qPop3 6s ease-in-out infinite; transform-origin: 206px 96px; }}
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
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Top Header Strip -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="32" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="34" x2="{w - 1}" y2="34" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="24" y="22" class="mono" font-size="12" font-weight="700" fill="{C.TEXT_PRIMARY}">// Trying to Understand</text>
  <text x="{w - 24}" y="22" text-anchor="end" class="mono" font-size="11" fill="{C.TEXT_MUTED}">mood: confused_concentration.jpg</text>

  <!-- Left Side: Confused Mascot Reference + Restrained Hand-Drawn Question Marks -->
  <g class="head-tilt">
    <rect x="43" y="47" width="146" height="146" rx="9" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1.2"/>
    {mascot_img_tag}
  </g>

  <!-- Hand-drawn SVG Question Marks & Doodle Marks -->
  <g class="q1" fill="none" stroke="{C.TEXT_PRIMARY}" stroke-width="1.8" stroke-linecap="round">
    <path d="M 24 54 C 24 46, 36 46, 36 54 C 36 59, 30 60, 30 65"/>
    <circle cx="30" cy="71" r="1.2" fill="{C.TEXT_PRIMARY}"/>
  </g>
  <g class="q2" fill="none" stroke="{C.TEXT_PRIMARY}" stroke-width="1.8" stroke-linecap="round">
    <path d="M 196 52 C 196 44, 208 44, 208 52 C 208 57, 202 58, 202 63"/>
    <circle cx="202" cy="69" r="1.2" fill="{C.TEXT_PRIMARY}"/>
  </g>
  <g class="q3" fill="none" stroke="{C.TEXT_SECONDARY}" stroke-width="1.5" stroke-linecap="round">
    <path d="M 204 88 C 204 82, 213 82, 213 88 C 213 92, 208 93, 208 97"/>
    <circle cx="208" cy="102" r="1" fill="{C.TEXT_SECONDARY}"/>
    <!-- Small hand-drawn concentration ticks -->
    <line x1="194" y1="116" x2="201" y2="114"/>
    <line x1="195" y1="122" x2="203" y2="122"/>
  </g>

  <!-- Right Side: Restrained Speech Bubble with Pointer -->
  <g class="quote-fade">
    <path d="M 244 66 H 844 A 8 8 0 0 1 852 74 V 182 A 8 8 0 0 1 844 190 H 244 A 8 8 0 0 1 236 182 V 132 L 218 122 L 236 112 V 74 A 8 8 0 0 1 244 66 Z"
          fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>

    <text x="262" y="106" class="sans" font-size="15.5" font-weight="600" fill="{C.TEXT_PRIMARY}">
      &#8220;When I say Ehh, ehhh, ehhhh... like for the third time,
    </text>
    <text x="262" y="134" class="sans" font-size="15.5" font-weight="600" fill="{C.TEXT_PRIMARY}">
      don&apos;t give up on me bro, I&apos;m trying to understand it for real.&#8221;
    </text>
    <text x="262" y="166" class="mono" font-size="11.5" fill="{C.TEXT_MUTED}">
      {escape(C.FUNNY_QUOTE_CAPTION)}
    </text>
  </g>
</svg>
'''


def generate_all() -> dict[str, pathlib.Path]:
    C.ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
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
