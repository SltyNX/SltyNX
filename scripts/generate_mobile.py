#!/usr/bin/env python3
"""
Generates dedicated mobile-optimized (640px stacked, large-font) SVGs in assets/mobile/
for automatic <picture><source media="(max-width: 768px)"> switching on mobile devices.
"""
from __future__ import annotations
from html import escape
import pathlib

import config as C



def build_dotmatrix_name() -> str:
    """
    Builds assets/dotmatrix-name.svg (640x240):
    Animation sequence (11s cycle):
      1. Sparse square-dot grid appears on a pure #000000 background (0.0s - 0.8s).
      2. Individual dots illuminate in a controlled sequence across columns (0.8s - 2.2s).
      3. Dots activate to construct each letter of SLYTNX (1.2s - 3.0s).
      4. The triangular emblem forms above the wordmark (2.4s - 3.6s).
      5. Completed logo stays clearly readable for >5.5 seconds (3.6s - 9.4s).
      6. A subtle horizontal scan sweeps across the completed logo (5.4s - 6.8s).
      7. Pauses before resetting cleanly (9.4s - 11.0s).
    """
    w, h = 640, 240

    dot_size = 5.4
    pitch = 7.8

    # Wordmark geometry: 6 letters, each 9 cols wide, 3 cols gap between letters
    # Total cols for wordmark = 6 * 9 + 5 * 3 = 69 cols
    # Total width = 69 * 7.8 = 538.2px -> start_x = (640 - 538.2) / 2 = 50.9
    total_cols = 69
    word_start_x = (w - (total_cols * pitch)) / 2.0
    word_start_y = 118.0

    # Background sparse matrix grid (every 2nd cell in the display window so SVG stays fast & crisp)
    bg_rects: list[str] = []
    for r in range(-9, 13, 2):
        gy = word_start_y + r * pitch
        if gy < 44 or gy > h - 28:
            continue
        for c in range(-2, total_cols + 3, 2):
            gx = word_start_x + c * pitch
            if gx < 20 or gx > w - 24:
                continue
            bg_rects.append(f'<rect x="{gx:.1f}" y="{gy:.1f}" width="{dot_size:.1f}" height="{dot_size:.1f}"/>')

    # Active SLYTNX letter dots grouped into 12 deterministic timing bands (b0..b11)
    bands: list[list[str]] = [[] for _ in range(12)]
    word = "SLYTNX"
    for li, ch in enumerate(word):
        grid = C.DOT_LETTERS[ch]
        col_offset = li * 12  # 9 cols + 3 gap
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                if cell != "#":
                    continue
                global_col = col_offset + c
                dx = word_start_x + global_col * pitch
                dy = word_start_y + r * pitch
                band_idx = min(11, (global_col * 12) // total_cols)
                bands[band_idx].append(
                    f'<rect x="{dx:.1f}" y="{dy:.1f}" width="{dot_size:.1f}" height="{dot_size:.1f}"/>'
                )

    band_groups: list[str] = []
    for b_idx, rects in enumerate(bands):
        band_groups.append(
            f'<g class="dm-band b{b_idx}" fill="{C.TEXT_PRIMARY}">{"".join(rects)}</g>'
        )

    # Emblem above wordmark: dot-matrix points + crisp geometric triple-triangle lock-in
    emblem_dots: list[str] = []
    emb_cols = len(C.DOT_EMBLEM[0])
    emb_pitch = 4.8
    emb_dot = 3.4
    emb_start_x = (w - emb_cols * emb_pitch) / 2.0
    emb_start_y = 42.0
    for r, row in enumerate(C.DOT_EMBLEM):
        for c, cell in enumerate(row):
            if cell == "#":
                ex = emb_start_x + c * emb_pitch
                ey = emb_start_y + r * emb_pitch
                emblem_dots.append(
                    f'<rect x="{ex:.1f}" y="{ey:.1f}" width="{emb_dot:.1f}" height="{emb_dot:.1f}"/>'
                )

    # Geometric wireframe overlay that locks over the emblem dots once formed
    emblem_vector = C.render_brand_emblem_svg(cx=w / 2.0, top_y=40.0, scale=0.78)

    # Generate CSS rules for the 12 bands (staggered activation between 6% and 26% of 11s loop)
    band_css: list[str] = []
    for b_idx in range(12):
        start_pct = 6 + b_idx * 1.6
        pre_pct = max(1.0, start_pct - 2.0)
        lock_pct = start_pct + 4.0
        scan_pct = 48.0 + b_idx * 1.4
        band_css.append(
            f".b{b_idx} {{ animation: dmB{b_idx} 11s linear infinite; }}\n"
            f"    @keyframes dmB{b_idx} {{\n"
            f"      0%, {pre_pct:.1f}% {{ opacity: 0.08; fill: {C.TEXT_MUTED}; }}\n"
            f"      {start_pct:.1f}% {{ opacity: 0.55; fill: {C.TEXT_SECONDARY}; }}\n"
            f"      {lock_pct:.1f}%, {scan_pct - 1.5:.1f}% {{ opacity: 1; fill: {C.TEXT_PRIMARY}; }}\n"
            f"      {scan_pct:.1f}% {{ opacity: 1; fill: #FFFFFF; }}\n"
            f"      {scan_pct + 2.0:.1f}%, 88% {{ opacity: 1; fill: {C.TEXT_PRIMARY}; }}\n"
            f"      95%, 100% {{ opacity: 0.08; fill: {C.TEXT_MUTED}; }}\n"
            f"    }}"
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="SLYTNX Animated Dot-Matrix Name Simulator">
  <title>SLYTNX — Dot-Matrix Name Simulator</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .grid-bg {{ fill: {C.BG_DOT_IDLE}; animation: gridInit 11s linear infinite; }}
    @keyframes gridInit {{
      0% {{ opacity: 0.35; }}
      6%, 90% {{ opacity: 1; }}
      96%, 100% {{ opacity: 0.35; }}
    }}
    {"    ".join(band_css)}
    .emblem-dots {{ fill: {C.TEXT_PRIMARY}; animation: embDots 11s linear infinite; }}
    @keyframes embDots {{
      0%, 20% {{ opacity: 0.06; }}
      26% {{ opacity: 0.65; }}
      32%, 88% {{ opacity: 0.95; }}
      95%, 100% {{ opacity: 0.06; }}
    }}
    .emblem-vec {{ animation: embVec 11s linear infinite; }}
    @keyframes embVec {{
      0%, 26% {{ opacity: 0; }}
      34%, 88% {{ opacity: 1; }}
      95%, 100% {{ opacity: 0; }}
    }}
    .scan-bar {{ animation: scanSweep 11s linear infinite; }}
    @keyframes scanSweep {{
      0%, 46% {{ opacity: 0; transform: translateX(0px); }}
      48% {{ opacity: 0.22; transform: translateX(0px); }}
      66% {{ opacity: 0.22; transform: translateX(540px); }}
      68%, 100% {{ opacity: 0; transform: translateX(540px); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .grid-bg, .dm-band, .emblem-dots, .emblem-vec {{ animation: none !important; opacity: 1 !important; fill: {C.TEXT_PRIMARY} !important; }}
      .scan-bar {{ display: none !important; }}
    }}
  </style>

  <!-- Outer Frame -->
  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Header Metadata -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="32" rx="6" fill="{C.BG_SECONDARY}"/>
  <text x="18" y="22" class="mono" font-size="13" fill="{C.TEXT_SECONDARY}">matrix://sltynx [69x11 dot-array]</text>
  <text x="{w - 18}" y="22" text-anchor="end" class="mono" font-size="13" fill="{C.TEXT_MUTED}">mode: dot-convergence</text>
  <line x1="1" y1="34" x2="{w - 1}" y2="34" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- 1. Sparse Background Dot Field -->
  <g class="grid-bg">{"".join(bg_rects)}</g>

  <!-- 2. Emblem Dot-Matrix & Vector Lock-In Above Wordmark -->
  <g class="emblem-dots">{"".join(emblem_dots)}</g>
  <g class="emblem-vec">{emblem_vector}</g>

  <!-- 3. Active SLYTNX Dot-Matrix Wordmark Bands -->
  {"".join(band_groups)}

  <!-- 4. Subtle Horizontal Scanline Pass -->
  <rect x="44" y="40" width="18" height="170" fill="{C.TEXT_PRIMARY}" class="scan-bar"/>

  <!-- Bottom Caption -->
  <text x="{w / 2:.0f}" y="226" text-anchor="middle" class="mono" font-size="14" font-weight="700" fill="{C.TEXT_SECONDARY}" letter-spacing="2.5">SLYTNX // SLEEPING CORE</text>
</svg>
'''





def build_sltynx_logo() -> str:
    """
    Builds assets/sltynx-logo.svg:
    Clean, scalable monochrome white vector reproduction of Asset B on pure #000000.
    Also serves as the static fallback for the dot-matrix name simulator.
    """
    w, h = 640, 240
    emblem = C.render_brand_emblem_svg(cx=w / 2.0, top_y=28.0, scale=1.0)
    wordmark = C.render_geometric_wordmark_svg(start_x=110.0, top_y=128.0, scale=0.86)

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="SLYTNX monochrome emblem and wordmark">
  <title>SLYTNX Brand Logo</title>
  <rect x="0" y="0" width="{w}" height="{h}" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>
  {emblem}
  {wordmark}
</svg>
'''


def _render_hero_dot_wordmark(start_x: float, start_y: float, dot_size: float = 4.5, pitch: float = 6.0) -> str:
    """
    Renders SLYTNX in the hero banner using discrete square dots
    (11 rows x 9 cols per letter) so each letter is genuinely formed from square pixels.
    """
    rects: list[str] = []
    word = "SLYTNX"
    letter_w = 9 * pitch
    letter_gap = 2.2 * pitch

    for li, ch in enumerate(word):
        grid = C.DOT_LETTERS[ch]
        lx = start_x + li * (letter_w + letter_gap)
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                dx = lx + c * pitch
                dy = start_y + r * pitch
                if cell == "#":
                    delay = (li * 0.15 + r * 0.03) % 2.0
                    rects.append(
                        f'<rect x="{dx:.1f}" y="{dy:.1f}" width="{dot_size:.1f}" height="{dot_size:.1f}" '
                        f'fill="{C.TEXT_PRIMARY}" class="hdot" style="animation-delay:{delay:.2f}s"/>'
                    )
                else:
                    rects.append(
                        f'<rect x="{dx:.1f}" y="{dy:.1f}" width="{dot_size:.1f}" height="{dot_size:.1f}" '
                        f'fill="{C.BG_DOT_IDLE}"/>'
                    )
    return '<g class="hero-dot-wordmark">' + "".join(rects) + "</g>"


def build_hero() -> str:
    """
    Builds assets/hero.svg (640x430):
    Mobile-first high-legibility layout:
    Top section:
      - Large Triangular SltyNX emblem + discrete dot-matrix SLYTNX wordmark
      - Subtitle: sleep > code > repeat (19px bold)
      - Secondary terminal details: Sleeping Core, status: sleeping..., clock [03:14 AM],
        blinking cursor, crescent moon & sleeping-cat doodle.
    Bottom section:
      - Full-width (600x196) continuous 16s seamless looping animation of the sleepy mascot
        walking toward the bed, climbing onto the mattress, lying down on the pillow, pulling
        the blanket up, closing its eyes, breathing subtly, and emitting floating pixel Z / Zz / Zzz
        effects, preserving the likeness and scene from Asset A (sleepy-mascot.jpg).
    """
    w, h = 640, 430
    sleepy_b64 = C.get_asset_base64("sleepy-mascot.jpg")
    bg_img_tag = ""
    if sleepy_b64:
        bg_img_tag = (
            f'<image href="data:image/jpeg;base64,{sleepy_b64}" '
            f'x="20" y="218" width="600" height="194" preserveAspectRatio="xMidYMid slice" '
            f'clip-path="url(#bedSceneClip)" opacity="0.24" class="ref-vignette"/>'
        )

    emblem_left = C.render_brand_emblem_svg(cx=66.0, top_y=52.0, scale=0.82)
    dot_wordmark = _render_hero_dot_wordmark(start_x=126.0, start_y=60.0, dot_size=4.5, pitch=6.0)

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="SltyNX Hero Banner — sleep, code, repeat">
  <title>SltyNX — Sleeping Core (sleep &gt; code &gt; repeat)</title>
  <defs>
    <clipPath id="bedSceneClip">
      <rect x="20" y="218" width="600" height="194" rx="6"/>
    </clipPath>
  </defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    .cur {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}

    .hdot {{ animation: dotPulse 6s ease-in-out infinite; }}
    @keyframes dotPulse {{
      0%, 85%, 100% {{ fill: {C.TEXT_PRIMARY}; opacity: 1; }}
      92% {{ fill: #BDBDBD; opacity: 0.78; }}
    }}

    .phase-walk {{ animation: walkCycle 16s linear infinite; }}
    @keyframes walkCycle {{
      0% {{ opacity: 0; transform: translate(0px, 0px); }}
      3% {{ opacity: 1; transform: translate(12px, -2px); }}
      6% {{ opacity: 1; transform: translate(38px, 0px); }}
      9% {{ opacity: 1; transform: translate(68px, -2px); }}
      12% {{ opacity: 1; transform: translate(96px, 0px); }}
      14% {{ opacity: 1; transform: translate(116px, -1px); }}
      15%, 100% {{ opacity: 0; transform: translate(116px, -1px); }}
    }}

    .phase-climb {{ animation: climbCycle 16s linear infinite; }}
    @keyframes climbCycle {{
      0%, 13.9% {{ opacity: 0; transform: translate(0px, 0px); }}
      14% {{ opacity: 1; transform: translate(0px, 0px); }}
      18% {{ opacity: 1; transform: translate(32px, -18px); }}
      22% {{ opacity: 1; transform: translate(64px, -28px); }}
      25% {{ opacity: 1; transform: translate(82px, -24px); }}
      26%, 100% {{ opacity: 0; transform: translate(82px, -24px); }}
    }}

    .phase-settle {{ animation: settleCycle 16s linear infinite; }}
    @keyframes settleCycle {{
      0%, 24.9% {{ opacity: 0; }}
      25% {{ opacity: 1; }}
      35% {{ opacity: 1; }}
      36%, 100% {{ opacity: 0; }}
    }}

    .phase-sleep {{ animation: sleepCycle 16s linear infinite; }}
    @keyframes sleepCycle {{
      0%, 34.9% {{ opacity: 0; }}
      36%, 92% {{ opacity: 1; }}
      98%, 100% {{ opacity: 0; }}
    }}

    .breathe {{ animation: chestBreathe 3.2s ease-in-out infinite; }}
    @keyframes chestBreathe {{
      0%, 100% {{ transform: translateY(0px); }}
      50% {{ transform: translateY(-2px); }}
    }}

    .blanket-pull {{ animation: blanketUp 16s ease-in-out infinite; }}
    @keyframes blanketUp {{
      0%, 25% {{ transform: translate(16px, 14px); }}
      35%, 92% {{ transform: translate(0px, 0px); }}
      98%, 100% {{ transform: translate(16px, 14px); }}
    }}

    .z1 {{ animation: floatZ1 16s linear infinite; }}
    .z2 {{ animation: floatZ2 16s linear infinite; }}
    .z3 {{ animation: floatZ3 16s linear infinite; }}
    @keyframes floatZ1 {{
      0%, 38% {{ opacity: 0; transform: translate(0px, 0px); }}
      43% {{ opacity: 0.9; transform: translate(4px, -10px); }}
      55% {{ opacity: 0; transform: translate(10px, -28px); }}
      62% {{ opacity: 0; transform: translate(0px, 0px); }}
      67% {{ opacity: 0.9; transform: translate(4px, -10px); }}
      80% {{ opacity: 0; transform: translate(10px, -28px); }}
      100% {{ opacity: 0; }}
    }}
    @keyframes floatZ2 {{
      0%, 42% {{ opacity: 0; transform: translate(0px, 0px); }}
      48% {{ opacity: 0.85; transform: translate(6px, -12px); }}
      60% {{ opacity: 0; transform: translate(14px, -32px); }}
      66% {{ opacity: 0; transform: translate(0px, 0px); }}
      72% {{ opacity: 0.85; transform: translate(6px, -12px); }}
      85% {{ opacity: 0; transform: translate(14px, -32px); }}
      100% {{ opacity: 0; }}
    }}
    @keyframes floatZ3 {{
      0%, 46% {{ opacity: 0; transform: translate(0px, 0px); }}
      53% {{ opacity: 0.95; transform: translate(8px, -14px); }}
      66% {{ opacity: 0; transform: translate(18px, -38px); }}
      70% {{ opacity: 0; transform: translate(0px, 0px); }}
      77% {{ opacity: 0.95; transform: translate(8px, -14px); }}
      90% {{ opacity: 0; transform: translate(18px, -38px); }}
      100% {{ opacity: 0; }}
    }}

    .phone-glow {{ animation: phonePulse 4s ease-in-out infinite; }}
    @keyframes phonePulse {{
      0%, 100% {{ opacity: 0.65; }}
      50% {{ opacity: 0.95; }}
    }}

    @media (prefers-reduced-motion: reduce) {{
      .phase-walk, .phase-climb, .phase-settle {{ display: none !important; }}
      .phase-sleep {{ opacity: 1 !important; animation: none !important; }}
      .blanket-pull, .breathe, .hdot, .cur, .phone-glow {{ animation: none !important; }}
      .z1, .z2, .z3 {{ animation: none !important; opacity: 0.85 !important; }}
    }}
  </style>

  <!-- Outer Pure Black Canvas & Crisp Terminal Border -->
  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Top Terminal Bar -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="36" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="38" x2="{w - 1}" y2="38" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="22" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <circle cx="38" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <circle cx="54" cy="19.5" r="4.5" fill="{C.TEXT_DIM}"/>
  <text x="74" y="24" class="mono" font-size="13.5" fill="{C.TEXT_SECONDARY}">sltynx@sleeping-core: ~/profile</text>

  <!-- Top-Right Clock & Moon Indicator -->
  <g transform="translate(490, 11)">
    <path d="M 10 2 A 6.5 6.5 0 1 0 16 12.5 A 5.2 5.2 0 1 1 10 2 Z" fill="{C.TEXT_SECONDARY}"/>
    <rect x="22" y="4" width="2" height="2" fill="{C.TEXT_MUTED}"/>
    <rect x="27" y="9" width="2" height="2" fill="{C.TEXT_MUTED}"/>
    <text x="34" y="13" class="mono" font-size="13" fill="{C.TEXT_SECONDARY}">[{escape(C.HERO_CLOCK)}]</text>
  </g>

  <!-- ===================================================================== -->
  <!-- TOP SECTION: Emblem, Dot-Matrix Wordmark, Tagline & Status Badges     -->
  <!-- ===================================================================== -->
  {emblem_left}
  {dot_wordmark}

  <line x1="20" y1="142" x2="620" y2="142" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Tagline: sleep > code > repeat -->
  <text x="24" y="168" class="mono" font-size="18.5" font-weight="700" fill="{C.TEXT_PRIMARY}" letter-spacing="1.2">{escape(C.HERO_TAGLINE)}</text>

  <!-- Status Badges Row -->
  <rect x="280" y="150" width="148" height="28" rx="4" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="294" cy="164" r="4" fill="{C.TEXT_PRIMARY}"/>
  <text x="306" y="169" class="mono" font-size="13.5" font-weight="600" fill="{C.TEXT_PRIMARY}">{escape(C.BIO)}</text>

  <rect x="436" y="150" width="184" height="28" rx="4" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="448" y="169" class="mono" font-size="13.5" fill="{C.TEXT_SECONDARY}">{escape(C.HERO_STATUS)}</text>
  <rect x="602" y="157" width="8" height="14" fill="{C.TEXT_PRIMARY}" class="cur"/>

  <!-- Sub-caption + Sleeping Cat Doodle -->
  <text x="24" y="198" class="mono" font-size="13" fill="{C.TEXT_MUTED}">// low-energy mode enabled &#8226; learning step by step</text>
  <g transform="translate(466, 185)" stroke="{C.TEXT_MUTED}" stroke-width="1.3" fill="none">
    <path d="M 2 14 C 2 6, 22 6, 22 14 Z" fill="{C.BG_SECONDARY}"/>
    <path d="M 5 8 L 3 3 L 8 6 M 19 8 L 21 3 L 16 6"/>
    <path d="M 22 13 C 27 13, 28 9, 25 8"/>
    <text x="34" y="13" class="mono" font-size="12.5" fill="{C.TEXT_MUTED}" stroke="none">cat: also asleep</text>
  </g>

  <!-- ===================================================================== -->
  <!-- BOTTOM SECTION: Animated Sleepy Mascot Bedroom Scene (20..620)        -->
  <!-- ===================================================================== -->
  <rect x="20" y="218" width="600" height="194" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>
  {bg_img_tag}

  <g clip-path="url(#bedSceneClip)">
    <!-- Night Window & Moon in Bedroom Background -->
    <rect x="46" y="232" width="76" height="82" rx="3" fill="#050505" stroke="{C.BORDER}" stroke-width="1.2"/>
    <line x1="84" y1="232" x2="84" y2="314" stroke="{C.BORDER_SUBTLE}" stroke-width="1"/>
    <line x1="46" y1="273" x2="122" y2="273" stroke="{C.BORDER_SUBTLE}" stroke-width="1"/>
    <path d="M 96 244 A 8 8 0 1 0 105 256 A 6.5 6.5 0 1 1 96 244 Z" fill="{C.TEXT_SECONDARY}" opacity="0.8"/>
    <rect x="60" y="248" width="2.5" height="2.5" fill="{C.TEXT_MUTED}"/>
    <rect x="68" y="288" width="2.5" height="2.5" fill="{C.TEXT_MUTED}"/>

    <!-- Isometric/Angled Bed Frame & Bookshelf Headboard (shifted for 600px wide bedroom) -->
    <g transform="translate(-236, 152)">
      <!-- Headboard with stacked books -->
      <polygon points="590,115 745,68 745,108 590,155" fill="#0E0E0E" stroke="{C.BORDER}" stroke-width="1.2"/>
      <rect x="612" y="102" width="22" height="14" transform="skewY(-16)" fill="#181818" stroke="{C.BORDER}" stroke-width="1"/>
      <rect x="615" y="96" width="20" height="7" transform="skewY(-16)" fill="#222222" stroke="{C.BORDER}" stroke-width="1"/>
      <line x1="685" y1="88" x2="685" y2="112" stroke="{C.BORDER}" stroke-width="2"/>
      <line x1="691" y1="86" x2="691" y2="110" stroke="{C.TEXT_MUTED}" stroke-width="2"/>
      <line x1="697" y1="84" x2="697" y2="108" stroke="{C.BORDER}" stroke-width="2"/>

      <!-- Mattress Surface -->
      <polygon points="580,152 745,102 836,196 664,258" fill="#0B0B0B" stroke="{C.BORDER}" stroke-width="1.4"/>
      <polygon points="580,152 664,258 664,274 580,168" fill="#060606" stroke="{C.BORDER}" stroke-width="1.2"/>

      <!-- Soft Rectangular Pillow on Mattress -->
      <polygon points="642,140 722,114 748,144 668,172" rx="6" fill="#161616" stroke="{C.TEXT_MUTED}" stroke-width="1.2"/>

      <!-- Glowing Smartphone next to Pillow -->
      <g class="phone-glow">
        <polygon points="614,174 632,166 644,182 626,190" fill="#1F1F1F" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
        <polygon points="617,175 631,169 640,181 626,187" fill="#D8D8D8"/>
        <circle cx="632" cy="182" r="1.3" fill="{C.BG_PRIMARY}"/>
      </g>

      <!-- PHASE 1: Mascot Walking Toward Bed -->
      <g class="phase-walk">
        <ellipse cx="440" cy="236" rx="18" ry="5" fill="#050505"/>
        <rect x="432" y="216" width="6" height="16" rx="2" fill="#1C1C1C" stroke="{C.TEXT_MUTED}" stroke-width="1"/>
        <rect x="442" y="214" width="6" height="16" rx="2" fill="#1C1C1C" stroke="{C.TEXT_MUTED}" stroke-width="1"/>
        <rect x="428" y="190" width="24" height="28" rx="5" fill="#242424" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
        <rect x="423" y="194" width="6" height="18" rx="3" fill="#242424" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
        <rect x="451" y="194" width="6" height="18" rx="3" fill="#242424" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
        <circle cx="440" cy="172" r="19" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
        <path d="M 421 172 C 421 150, 459 150, 459 172 C 455 162, 445 165, 438 168 L 434 162 L 428 170 Z" fill="#1A1A1A" stroke="{C.TEXT_MUTED}" stroke-width="1"/>
        <line x1="444" y1="175" x2="452" y2="175" stroke="{C.BG_PRIMARY}" stroke-width="2" stroke-linecap="round"/>
      </g>

      <!-- PHASE 2: Mascot Climbing Onto Bed -->
      <g class="phase-climb">
        <g transform="translate(558, 198) rotate(14)">
          <rect x="-10" y="14" width="7" height="14" rx="2" fill="#1C1C1C" stroke="{C.TEXT_MUTED}" stroke-width="1"/>
          <rect x="2" y="10" width="7" height="14" rx="2" fill="#1C1C1C" stroke="{C.TEXT_MUTED}" stroke-width="1"/>
          <rect x="-12" y="-10" width="24" height="26" rx="5" fill="#242424" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
          <circle cx="0" cy="-26" r="18" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
          <path d="M -17 -26 C -17 -46, 17 -46, 17 -26 C 12 -34, 2 -32, -4 -28 Z" fill="#1A1A1A" stroke="{C.TEXT_MUTED}" stroke-width="1"/>
          <line x1="3" y1="-23" x2="10" y2="-23" stroke="{C.BG_PRIMARY}" stroke-width="2" stroke-linecap="round"/>
        </g>
      </g>

      <!-- PHASE 3: Mascot Settling onto Pillow -->
      <g class="phase-settle">
        <g transform="translate(698, 154)">
          <path d="M 10 22 L 24 44 L 32 40 L 24 18 L 38 32 L 46 26 L 26 8 Z" fill="#171717" stroke="{C.TEXT_MUTED}" stroke-width="1.2"/>
          <polygon points="-14,6 16,-6 32,18 2,30" rx="5" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
          <rect x="-24" y="10" width="14" height="7" rx="3" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
          <rect x="14" y="-12" width="14" height="7" rx="3" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
          <circle cx="-12" cy="-10" r="23" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
          <path d="M -34 -12 C -34 -38, 10 -38, 10 -10 C 6 -2, 0 -6, -4 -10 L -10 -2 L -16 -12 L -24 -4 Z" fill="#1A1A1A" stroke="{C.TEXT_MUTED}" stroke-width="1.1"/>
          <line x1="-18" y1="-3" x2="-9" y2="-4" stroke="{C.BG_PRIMARY}" stroke-width="2.2" stroke-linecap="round"/>
        </g>
      </g>

      <!-- PHASE 4: Sleeping on Pillow + Breathing + Zzz -->
      <g class="phase-sleep">
        <g transform="translate(698, 154)">
          <path d="M 10 22 L 24 46 L 33 41 L 24 20 L 42 32 L 49 25 L 26 8 Z" fill="#171717" stroke="{C.TEXT_MUTED}" stroke-width="1.2"/>
          <circle cx="28" cy="45" r="3.5" fill="#D8D8D8"/>
          <circle cx="47" cy="29" r="3.5" fill="#D8D8D8"/>

          <g class="breathe">
            <rect x="-26" y="8" width="16" height="8" rx="3" transform="rotate(-12 -18 12)" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1.1"/>
            <circle cx="-27" cy="13" r="3.5" fill="#E5E5E5"/>
            <rect x="14" y="-12" width="16" height="8" rx="3" transform="rotate(-22 22 -8)" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1.1"/>
            <circle cx="30" cy="-11" r="3.5" fill="#E5E5E5"/>
            <polygon points="-14,6 16,-6 32,18 2,30" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
          </g>

          <circle cx="-12" cy="-10" r="23" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
          <path d="M -34 -10 C -34 -38, 10 -38, 10 -10 C 8 0, 2 -4, -2 -8 L -8 0 L -14 -10 L -22 -2 C -28 -4, -32 -6, -34 -10 Z" fill="#1A1A1A" stroke="{C.TEXT_MUTED}" stroke-width="1.1"/>
          <line x1="-19" y1="-2" x2="-9" y2="-4" stroke="{C.BG_PRIMARY}" stroke-width="2.4" stroke-linecap="round"/>

          <!-- Floating Pixel-Style Z / Zz / Zzz Animation (relative to sleeping mascot at 698,154) -->
          <g class="mono" font-weight="700" fill="{C.TEXT_PRIMARY}">
            <text x="-22" y="-36" font-size="14" class="z1">Z</text>
            <text x="-4" y="-52" font-size="17" class="z2">Zz</text>
            <text x="18" y="-70" font-size="21" class="z3">Zzz</text>
          </g>
        </g>
      </g>

      <!-- Blanket at Foot of Bed -->
      <g class="blanket-pull">
        <path d="M 654 256 C 685 215, 765 182, 834 196 L 836 268 L 664 268 Z" fill="#141414" stroke="{C.TEXT_MUTED}" stroke-width="1.3"/>
        <path d="M 684 242 C 715 218, 762 204, 808 212" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>
      </g>
    </g>

    <!-- Scene HUD Overlay inside Bedroom Bottom-Left -->
    <rect x="34" y="376" width="188" height="26" rx="4" fill="#000000" fill-opacity="0.86" stroke="{C.BORDER}" stroke-width="1"/>
    <text x="46" y="394" class="mono" font-size="13" fill="{C.TEXT_SECONDARY}">scene: bedtime_loop.sh</text>
  </g>
</svg>
'''


def build_telegram_button() -> str:
    """
    Builds assets/telegram-button.svg (440x76):
    Prominent, mobile-friendly Telegram action button on #000000 with thin grey border,
    recognizable Telegram paper-plane icon, 'Message me on Telegram', and '@SltyNX_X'.
    """
    w, h = 440, 76
    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Message me on Telegram @SltyNX_X">
  <title>{escape(C.TELEGRAM_CTA)} ({escape(C.TELEGRAM_USERNAME)})</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    .border-pulse {{ animation: bPulse 4s ease-in-out infinite; }}
    @keyframes bPulse {{
      0%, 100% {{ stroke: {C.BORDER}; }}
      50% {{ stroke: {C.TEXT_SECONDARY}; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .border-pulse {{ animation: none !important; }}
    }}
  </style>
  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1.5" y="1.5" width="{w - 3}" height="{h - 3}" rx="7" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.4" class="border-pulse"/>

  <!-- Icon Box -->
  <rect x="16" y="14" width="48" height="48" rx="6" fill="{C.BG_ELEVATED}" stroke="{C.BORDER}" stroke-width="1.2"/>
  <!-- Recognizable Telegram Paper Plane Icon -->
  <g transform="translate(40, 38) scale(1.2)">
    <path d="M -11 -1 L 10 -9 L 6 10 L 0 5.5 L -4 9 L -4 3.5 L 5 -4.5 L -6 2 Z" fill="{C.TEXT_PRIMARY}"/>
  </g>

  <!-- Primary & Secondary Text -->
  <text x="78" y="34" class="sans" font-size="17.5" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(C.TELEGRAM_CTA)}</text>
  <text x="78" y="56" class="mono" font-size="14.5" fill="{C.TEXT_SECONDARY}">{escape(C.TELEGRAM_USERNAME)}</text>

  <!-- Right Arrow Indicator Pill -->
  <rect x="346" y="23" width="76" height="30" rx="5" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1.2"/>
  <text x="384" y="43" text-anchor="middle" class="mono" font-size="13.5" font-weight="600" fill="{C.TEXT_PRIMARY}">open &#8594;</text>
</svg>
'''


def build_footer() -> str:
    """
    Builds assets/footer.svg (640x170):
    Mobile-optimized closing section featuring the original triangular SltyNX emblem,
    SLYTNX, sleep • code • create, Thanks for visiting!, Still loading...,
    and a small sleeping-cat & crescent moon doodle.
    """
    w, h = 640, 170
    emblem = C.render_brand_emblem_svg(cx=w / 2.0, top_y=16.0, scale=0.56)
    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="SLYTNX — sleep, code, create. Thanks for visiting! Still loading...">
  <title>SLYTNX Footer — {escape(C.FOOTER_TAGLINE)}</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    .cur {{ animation: blink 1.2s steps(1) infinite; }}
    @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .cur {{ animation: none !important; }} }}
  </style>
  <rect x="0" y="0" width="{w}" height="{h}" rx="7" fill="{C.BG_PRIMARY}"/>
  <line x1="20" y1="2" x2="{w - 20}" y2="2" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Left Crescent Moon Doodle -->
  <g transform="translate(36, 26)">
    <path d="M 12 2 A 9 9 0 1 0 21 16 A 7.2 7.2 0 1 1 12 2 Z" fill="none" stroke="{C.TEXT_MUTED}" stroke-width="1.4"/>
    <rect x="28" y="4" width="2.5" height="2.5" fill="{C.TEXT_DIM}"/>
    <rect x="34" y="12" width="2" height="2" fill="{C.TEXT_DIM}"/>
  </g>

  <!-- Centered Triangular SltyNX Emblem -->
  {emblem}

  <!-- Wordmark & Taglines -->
  <text x="{w / 2:.0f}" y="86" text-anchor="middle" class="mono" font-size="18" font-weight="700" fill="{C.TEXT_PRIMARY}" letter-spacing="4">{escape(C.FOOTER_WORDMARK)}</text>
  <text x="{w / 2:.0f}" y="110" text-anchor="middle" class="mono" font-size="14.5" fill="{C.TEXT_SECONDARY}" letter-spacing="1.5">{escape(C.FOOTER_TAGLINE)}</text>
  <text x="{w / 2:.0f}" y="134" text-anchor="middle" class="sans" font-size="15" font-weight="600" fill="{C.TEXT_PRIMARY}">{escape(C.FOOTER_THANKS)}</text>

  <!-- Still loading... with blinking terminal cursor -->
  <text x="{w / 2 - 6:.0f}" y="156" text-anchor="middle" class="mono" font-size="13.5" fill="{C.TEXT_MUTED}">{escape(C.FOOTER_STATUS)}</text>
  <rect x="{w / 2 + 54:.0f}" y="144" width="7" height="13" fill="{C.TEXT_MUTED}" class="cur"/>

  <!-- Right Sleeping Cat Doodle -->
  <g transform="translate(556, 130)" stroke="{C.TEXT_MUTED}" stroke-width="1.4" fill="none">
    <path d="M 0 16 C 0 7, 22 7, 22 16 Z" fill="{C.BG_SECONDARY}"/>
    <path d="M 3 10 L 1 4 L 7 7 M 19 10 L 21 4 L 15 7"/>
    <text x="26" y="12" class="mono" font-size="11.5" fill="{C.TEXT_MUTED}" stroke="none">zZz</text>
  </g>
</svg>
'''





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
    mob_dir = C.ASSETS_DIR / "mobile"
    mob_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "mobile/hero.svg": build_hero(),
        "mobile/dotmatrix-name.svg": build_dotmatrix_name(),
        "mobile/profile-intro.svg": build_profile_intro(),
        "mobile/current-project.svg": build_current_project(),
        "mobile/skills-learning.svg": build_skills_learning(),
        "mobile/terminal-session.svg": build_terminal_session(),
        "mobile/ai-assistance.svg": build_ai_assistance(),
        "mobile/error-repair.svg": build_error_repair(),
        "mobile/knowledge-panel.svg": build_knowledge_panel(),
        "mobile/funny-quote.svg": build_funny_quote(),
        "mobile/footer.svg": build_footer(),
    }
    written: dict[str, pathlib.Path] = {}
    for rel_name, content in outputs.items():
        out_path = C.ASSETS_DIR / rel_name
        out_path.write_text(content, encoding="utf-8")
        written[rel_name] = out_path
    return written


if __name__ == "__main__":
    for k, p in generate_all().items():
        print(f"wrote {k:32s} ({p.stat().st_size:,} bytes)")
