#!/usr/bin/env python3
"""
Generates dedicated native-width (380px viewBox, 1:1 mobile scale, 1-column stacked)
mobile SVGs in assets/mobile/ for automatic <picture><source media="(max-width: 768px)">
switching on mobile phones.
Desktop (>768px) continues to load the exact 880px side-by-side SVGs in assets/*.svg.
"""
from __future__ import annotations
from html import escape
import pathlib

import config as C


def _render_mobile_dot_wordmark(start_x: float, start_y: float, dot_size: float = 3.5, pitch: float = 4.7) -> str:
    rects: list[str] = []
    word = "SLYTNX"
    letter_w = 9 * pitch
    letter_gap = 2.0 * pitch

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
    Builds assets/mobile/hero.svg (380x446):
    Native 380px phone-width layout so mobile text renders at 1:1 pixel scale without shrinking.
    """
    w, h = 380, 446
    sleepy_b64 = C.get_asset_base64("sleepy-mascot.jpg")
    bg_img_tag = ""
    if sleepy_b64:
        bg_img_tag = (
            f'<image href="data:image/jpeg;base64,{sleepy_b64}" '
            f'x="16" y="252" width="348" height="178" preserveAspectRatio="xMidYMid slice" '
            f'clip-path="url(#mobBedClip)" opacity="0.26"/>'
        )

    emblem_top = C.render_brand_emblem_svg(cx=w / 2.0, top_y=46.0, scale=0.72)
    # 6 letters * 9 + 5 * 2 = 64 cols * 4.8 = 307.2px -> start_x = (380 - 307.2)/2 = 36.4
    dot_wordmark = _render_mobile_dot_wordmark(start_x=36.4, start_y=110.0, dot_size=3.5, pitch=4.8)

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="SltyNX Hero Banner — sleep, code, repeat">
  <title>SltyNX — Sleeping Core (Mobile View)</title>
  <defs>
    <clipPath id="mobBedClip">
      <rect x="16" y="252" width="348" height="178" rx="6"/>
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
      3% {{ opacity: 1; transform: translate(6px, -2px); }}
      6% {{ opacity: 1; transform: translate(20px, 0px); }}
      9% {{ opacity: 1; transform: translate(35px, -2px); }}
      12% {{ opacity: 1; transform: translate(50px, 0px); }}
      14% {{ opacity: 1; transform: translate(58px, -1px); }}
      15%, 100% {{ opacity: 0; transform: translate(58px, -1px); }}
    }}
    .phase-climb {{ animation: climbCycle 16s linear infinite; }}
    @keyframes climbCycle {{
      0%, 13.9% {{ opacity: 0; transform: translate(0px, 0px); }}
      14% {{ opacity: 1; transform: translate(0px, 0px); }}
      18% {{ opacity: 1; transform: translate(22px, -18px); }}
      22% {{ opacity: 1; transform: translate(44px, -28px); }}
      25% {{ opacity: 1; transform: translate(54px, -24px); }}
      26%, 100% {{ opacity: 0; transform: translate(54px, -24px); }}
    }}
    .phase-settle {{ animation: settleCycle 16s linear infinite; }}
    @keyframes settleCycle {{
      0%, 24.9% {{ opacity: 0; }}
      25%, 35% {{ opacity: 1; }}
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
      55%, 62% {{ opacity: 0; transform: translate(10px, -26px); }}
      67% {{ opacity: 0.9; transform: translate(4px, -10px); }}
      80%, 100% {{ opacity: 0; transform: translate(10px, -26px); }}
    }}
    @keyframes floatZ2 {{
      0%, 42% {{ opacity: 0; transform: translate(0px, 0px); }}
      48% {{ opacity: 0.85; transform: translate(6px, -12px); }}
      60%, 66% {{ opacity: 0; transform: translate(14px, -30px); }}
      72% {{ opacity: 0.85; transform: translate(6px, -12px); }}
      85%, 100% {{ opacity: 0; transform: translate(14px, -30px); }}
    }}
    @keyframes floatZ3 {{
      0%, 46% {{ opacity: 0; transform: translate(0px, 0px); }}
      53% {{ opacity: 0.95; transform: translate(8px, -14px); }}
      66%, 70% {{ opacity: 0; transform: translate(18px, -34px); }}
      77% {{ opacity: 0.95; transform: translate(8px, -14px); }}
      90%, 100% {{ opacity: 0; transform: translate(18px, -34px); }}
    }}
    .phone-glow {{ animation: phonePulse 4s ease-in-out infinite; }}
    @keyframes phonePulse {{ 0%, 100% {{ opacity: 0.65; }} 50% {{ opacity: 0.95; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .phase-walk, .phase-climb, .phase-settle {{ display: none !important; }}
      .phase-sleep {{ opacity: 1 !important; animation: none !important; }}
      .blanket-pull, .breathe, .hdot, .cur, .phone-glow {{ animation: none !important; }}
      .z1, .z2, .z3 {{ animation: none !important; opacity: 0.85 !important; }}
    }}
  </style>

  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Top Terminal Header -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="34" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="36" x2="{w - 1}" y2="36" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="18" cy="18.5" r="4" fill="{C.TEXT_DIM}"/>
  <circle cx="32" cy="18.5" r="4" fill="{C.TEXT_DIM}"/>
  <circle cx="46" cy="18.5" r="4" fill="{C.TEXT_DIM}"/>
  <text x="62" y="23" class="mono" font-size="12.5" fill="{C.TEXT_SECONDARY}">sltynx@sleeping-core</text>
  <text x="{w - 14}" y="23" text-anchor="end" class="mono" font-size="12" fill="{C.TEXT_SECONDARY}">[{escape(C.HERO_CLOCK)}]</text>

  <!-- Centered Emblem & Dot-Matrix Wordmark -->
  {emblem_top}
  {dot_wordmark}

  <line x1="16" y1="170" x2="364" y2="170" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Big Centered Tagline -->
  <text x="{w / 2:.0f}" y="195" text-anchor="middle" class="mono" font-size="17.5" font-weight="700" fill="{C.TEXT_PRIMARY}" letter-spacing="1.2">{escape(C.HERO_TAGLINE)}</text>

  <!-- Status Badges -->
  <rect x="16" y="208" width="144" height="30" rx="5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.1"/>
  <circle cx="30" cy="223" r="4" fill="{C.TEXT_PRIMARY}"/>
  <text x="42" y="228" class="mono" font-size="13" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(C.BIO)}</text>

  <rect x="168" y="208" width="196" height="30" rx="5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.1"/>
  <text x="180" y="228" class="mono" font-size="13" fill="{C.TEXT_SECONDARY}">{escape(C.HERO_STATUS)}</text>
  <rect x="342" y="216" width="8" height="14" fill="{C.TEXT_PRIMARY}" class="cur"/>

  <!-- Animated Bedroom Scene (16..364, 252..430) -->
  <rect x="16" y="252" width="348" height="178" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>
  {bg_img_tag}

  <g clip-path="url(#mobBedClip)">
    <g transform="translate(-468, 184)">
      <rect x="492" y="76" width="56" height="64" rx="2" fill="#050505" stroke="{C.BORDER}" stroke-width="1"/>
      <line x1="520" y1="76" x2="520" y2="140" stroke="{C.BORDER_SUBTLE}" stroke-width="1"/>
      <line x1="492" y1="108" x2="548" y2="108" stroke="{C.BORDER_SUBTLE}" stroke-width="1"/>
      <path d="M 530 86 A 6.5 6.5 0 1 0 537 96 A 5 5 0 1 1 530 86 Z" fill="{C.TEXT_SECONDARY}" opacity="0.8"/>

      <polygon points="590,115 745,68 745,108 590,155" fill="#0E0E0E" stroke="{C.BORDER}" stroke-width="1.2"/>
      <polygon points="580,152 745,102 828,192 664,250" fill="#0B0B0B" stroke="{C.BORDER}" stroke-width="1.4"/>
      <polygon points="642,140 722,114 748,144 668,172" rx="6" fill="#161616" stroke="{C.TEXT_MUTED}" stroke-width="1.2"/>

      <g class="phone-glow">
        <polygon points="614,174 632,166 644,182 626,190" fill="#1F1F1F" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
        <polygon points="617,175 631,169 640,181 626,187" fill="#D8D8D8"/>
      </g>

      <g class="phase-walk">
        <ellipse cx="500" cy="232" rx="16" ry="5" fill="#050505"/>
        <rect x="492" y="212" width="6" height="16" rx="2" fill="#1C1C1C" stroke="{C.TEXT_MUTED}" stroke-width="1"/>
        <rect x="502" y="210" width="6" height="16" rx="2" fill="#1C1C1C" stroke="{C.TEXT_MUTED}" stroke-width="1"/>
        <rect x="488" y="186" width="24" height="28" rx="5" fill="#242424" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
        <circle cx="500" cy="168" r="18" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
        <path d="M 481 168 C 481 146, 519 146, 519 168 C 515 158, 505 161, 498 164 L 494 158 L 488 166 Z" fill="#1A1A1A"/>
        <line x1="504" y1="171" x2="512" y2="171" stroke="{C.BG_PRIMARY}" stroke-width="2" stroke-linecap="round"/>
      </g>

      <g class="phase-climb">
        <g transform="translate(558, 198) rotate(14)">
          <rect x="-12" y="-10" width="24" height="26" rx="5" fill="#242424" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
          <circle cx="0" cy="-26" r="17" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
          <path d="M -17 -26 C -17 -46, 17 -46, 17 -26 C 12 -34, 2 -32, -4 -28 Z" fill="#1A1A1A"/>
        </g>
      </g>

      <g class="phase-settle">
        <g transform="translate(698, 154)">
          <polygon points="-14,6 16,-6 32,18 2,30" rx="5" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
          <circle cx="-12" cy="-10" r="22" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
          <path d="M -34 -12 C -34 -38, 10 -38, 10 -10 C 6 -2, 0 -6, -4 -10 L -10 -2 L -16 -12 L -24 -4 Z" fill="#1A1A1A"/>
          <line x1="-18" y1="-3" x2="-9" y2="-4" stroke="{C.BG_PRIMARY}" stroke-width="2.2" stroke-linecap="round"/>
        </g>
      </g>

      <g class="phase-sleep">
        <g transform="translate(698, 154)">
          <path d="M 10 22 L 24 46 L 33 41 L 24 20 L 42 32 L 49 25 L 26 8 Z" fill="#171717" stroke="{C.TEXT_MUTED}" stroke-width="1.2"/>
          <g class="breathe">
            <rect x="-26" y="8" width="16" height="8" rx="3" transform="rotate(-12 -18 12)" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1.1"/>
            <rect x="14" y="-12" width="16" height="8" rx="3" transform="rotate(-22 22 -8)" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1.1"/>
            <polygon points="-14,6 16,-6 32,18 2,30" fill="#262626" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
          </g>
          <circle cx="-12" cy="-10" r="22" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
          <path d="M -34 -10 C -34 -38, 10 -38, 10 -10 C 8 0, 2 -4, -2 -8 L -8 0 L -14 -10 L -22 -2 C -28 -4, -32 -6, -34 -10 Z" fill="#1A1A1A"/>
          <line x1="-19" y1="-2" x2="-9" y2="-4" stroke="{C.BG_PRIMARY}" stroke-width="2.4" stroke-linecap="round"/>
          <g class="mono" font-weight="700" fill="{C.TEXT_PRIMARY}">
            <text x="-22" y="-34" font-size="14" class="z1">Z</text>
            <text x="-4" y="-48" font-size="17" class="z2">Zz</text>
            <text x="18" y="-64" font-size="20" class="z3">Zzz</text>
          </g>
        </g>
      </g>

      <g class="blanket-pull">
        <path d="M 654 252 C 685 215, 765 182, 828 196 L 828 260 L 664 260 Z" fill="#141414" stroke="{C.TEXT_MUTED}" stroke-width="1.3"/>
      </g>
    </g>

    <rect x="26" y="394" width="176" height="26" rx="4" fill="#000000" fill-opacity="0.88" stroke="{C.BORDER}" stroke-width="1"/>
    <text x="36" y="411" class="mono" font-size="12.5" fill="{C.TEXT_SECONDARY}">scene: bedtime_loop.sh</text>
  </g>
</svg>
'''


def build_dotmatrix_name() -> str:
    """
    Builds assets/mobile/dotmatrix-name.svg (380x240):
    Native 380px width dot-matrix simulator for crisp 1:1 mobile display.
    """
    w, h = 380, 240
    dot_size = 3.5
    pitch = 4.9
    total_cols = 69
    word_start_x = (w - (total_cols * pitch)) / 2.0
    word_start_y = 120.0

    bg_rects: list[str] = []
    for r in range(-11, 15, 2):
        gy = word_start_y + r * pitch
        if gy < 42 or gy > h - 32:
            continue
        for c in range(0, total_cols, 2):
            gx = word_start_x + c * pitch
            bg_rects.append(f'<rect x="{gx:.1f}" y="{gy:.1f}" width="{dot_size:.1f}" height="{dot_size:.1f}"/>')

    bands: list[list[str]] = [[] for _ in range(12)]
    word = "SLYTNX"
    for li, ch in enumerate(word):
        grid = C.DOT_LETTERS[ch]
        col_offset = li * 12
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

    band_groups = [
        f'<g class="dm-band b{b_idx}" fill="{C.TEXT_PRIMARY}">{"".join(rects)}</g>'
        for b_idx, rects in enumerate(bands)
    ]

    emblem_vector = C.render_brand_emblem_svg(cx=w / 2.0, top_y=50.0, scale=0.70)

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
  <title>SLYTNX — Dot-Matrix Name Simulator (Mobile)</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .grid-bg {{ fill: {C.BG_DOT_IDLE}; }}
    {"    ".join(band_css)}
    .emblem-vec {{ animation: embVec 11s linear infinite; }}
    @keyframes embVec {{ 0%, 26% {{ opacity: 0; }} 34%, 88% {{ opacity: 1; }} 95%, 100% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .dm-band, .emblem-vec {{ animation: none !important; opacity: 1 !important; fill: {C.TEXT_PRIMARY} !important; }}
    }}
  </style>

  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <rect x="1.5" y="1.5" width="{w - 3}" height="30" rx="6" fill="{C.BG_SECONDARY}"/>
  <text x="14" y="21" class="mono" font-size="12" fill="{C.TEXT_SECONDARY}">matrix://sltynx</text>
  <text x="{w - 14}" y="21" text-anchor="end" class="mono" font-size="12" fill="{C.TEXT_MUTED}">dot-convergence</text>
  <line x1="1" y1="32" x2="{w - 1}" y2="32" stroke="{C.BORDER}" stroke-width="1"/>

  <g class="grid-bg">{"".join(bg_rects)}</g>
  <g class="emblem-vec">{emblem_vector}</g>
  {"".join(band_groups)}

  <text x="{w / 2:.0f}" y="220" text-anchor="middle" class="mono" font-size="13.5" font-weight="700" fill="{C.TEXT_SECONDARY}" letter-spacing="2">SLYTNX // SLEEPING CORE</text>
</svg>
'''


def build_profile_intro() -> str:
    """
    Builds assets/mobile/profile-intro.svg (380x276):
    Native 380px width animated terminal with 14px monospace wrapped cleanly across 7 lines.
    """
    w, h = 380, 276
    intro_lines = [
        ("cmd", "$ cat profile_intro.txt", 64, 42, 47),
        ("pri", "> Just a guy who sleeps a lot,", 96, 48, 53),
        ("pri", "  codes a little, and dreams of", 120, 53, 58),
        ("pri", "  building something cool.", 144, 58, 63),
        ("sec", "> Currently a noob developer.", 176, 65, 70),
        ("sec", "  Learning as I go, breaking things", 200, 70, 75),
        ("sec", "  occasionally, & trying to learn.", 224, 75, 80),
    ]

    clips: list[str] = []
    texts: list[str] = []
    css_rules: list[str] = []

    for idx, (kind, txt, y, t0, t1) in enumerate(intro_lines):
        col = C.TEXT_PRIMARY if kind in ("cmd", "pri") else C.TEXT_SECONDARY
        fweight = ' font-weight="700"' if kind == "cmd" else ""
        clips.append(
            f'<clipPath id="mpiClip{idx}">'
            f'<rect x="14" y="{y - 18}" width="352" height="24" class="mpiline{idx}"/>'
            f'</clipPath>'
        )
        texts.append(
            f'<text x="18" y="{y}" clip-path="url(#mpiClip{idx})" class="mono" font-size="14"{fweight} fill="{col}" xml:space="preserve">{escape(txt)}</text>'
        )
        css_rules.append(
            f".mpiline{idx} {{ animation: mpiType{idx} 22s steps(36, end) infinite; }}\n"
            f"    @keyframes mpiType{idx} {{\n"
            f"      0%, 40% {{ width: 352px; }}\n"
            f"      41%, {t0}% {{ width: 0px; }}\n"
            f"      {t1}%, 100% {{ width: 352px; }}\n"
            f"    }}"
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Profile Introduction Terminal">
  <title>Profile Introduction — SltyNX (Mobile)</title>
  <defs>{"".join(clips)}</defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    {chr(10).join(css_rules)}
    .pi-cur {{ animation: piBlink 1s steps(2, start) infinite; }}
    @keyframes piBlink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .mpiline0, .mpiline1, .mpiline2, .mpiline3, .mpiline4, .mpiline5, .mpiline6 {{ animation: none !important; width: 352px !important; }}
    }}
  </style>

  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <rect x="1.5" y="1.5" width="{w - 3}" height="34" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="36" x2="{w - 1}" y2="36" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="18" cy="18.5" r="4" fill="{C.TEXT_DIM}"/>
  <circle cx="32" cy="18.5" r="4" fill="{C.TEXT_DIM}"/>
  <circle cx="46" cy="18.5" r="4" fill="{C.TEXT_DIM}"/>
  <text x="62" y="23" class="mono" font-size="12.5" fill="{C.TEXT_SECONDARY}">sltynx@sleeping-core: ~/intro</text>

  {"".join(texts)}

  <text x="18" y="256" class="mono" font-size="14" fill="{C.TEXT_MUTED}">$ </text>
  <rect x="36" y="243" width="8" height="15" fill="{C.TEXT_PRIMARY}" class="pi-cur"/>
</svg>
'''


def build_current_project() -> str:
    """
    Builds assets/mobile/current-project.svg (380x336):
    Native 380px width card with 21px title, 14.5px wrapped description, status bar,
    and full-width pixel-art Gnosis Keyboard below.
    """
    w, h = 380, 336

    keys_svg: list[str] = []
    row1 = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]
    row2 = ["A", "S", "D", "F", "G", "H", "J", "K", "L"]
    row3 = ["Z", "X", "C", "V", "B", "N", "M"]
    highlight_keys = {"G": "0.2s", "N": "0.9s", "O": "1.6s", "S": "2.3s", "I": "3.0s"}

    kb_x = 28
    kb_y = 216
    for idx, k in enumerate(row1):
        kx = kb_x + idx * 32.5
        ky = kb_y
        cls = ' class="key-press"' if k in highlight_keys else ""
        st = f' style="animation-delay:{highlight_keys[k]}"' if k in highlight_keys else ""
        keys_svg.append(
            f'<g{cls}{st}><rect x="{kx:.1f}" y="{ky}" width="28" height="21" rx="3" fill="{C.BG_ELEVATED}" stroke="{C.BORDER}" stroke-width="1"/>'
            f'<text x="{kx + 14:.1f}" y="{ky + 15}" text-anchor="middle" class="mono" font-size="11" font-weight="600" fill="{C.TEXT_SECONDARY}">{k}</text></g>'
        )
    for idx, k in enumerate(row2):
        kx = kb_x + 16 + idx * 32.5
        ky = kb_y + 25
        cls = ' class="key-press"' if k in highlight_keys else ""
        st = f' style="animation-delay:{highlight_keys[k]}"' if k in highlight_keys else ""
        keys_svg.append(
            f'<g{cls}{st}><rect x="{kx:.1f}" y="{ky}" width="28" height="21" rx="3" fill="{C.BG_ELEVATED}" stroke="{C.BORDER}" stroke-width="1"/>'
            f'<text x="{kx + 14:.1f}" y="{ky + 15}" text-anchor="middle" class="mono" font-size="11" font-weight="600" fill="{C.TEXT_SECONDARY}">{k}</text></g>'
        )
    for idx, k in enumerate(row3):
        kx = kb_x + 48 + idx * 32.5
        ky = kb_y + 50
        cls = ' class="key-press"' if k in highlight_keys else ""
        st = f' style="animation-delay:{highlight_keys[k]}"' if k in highlight_keys else ""
        keys_svg.append(
            f'<g{cls}{st}><rect x="{kx:.1f}" y="{ky}" width="28" height="21" rx="3" fill="{C.BG_ELEVATED}" stroke="{C.BORDER}" stroke-width="1"/>'
            f'<text x="{kx + 14:.1f}" y="{ky + 15}" text-anchor="middle" class="mono" font-size="11" font-weight="600" fill="{C.TEXT_SECONDARY}">{k}</text></g>'
        )
    keys_svg.append(
        f'<rect x="{kb_x}" y="{kb_y + 50}" width="42" height="21" rx="3" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>'
        f'<text x="{kb_x + 21}" y="{kb_y + 64}" text-anchor="middle" class="mono" font-size="9.5" fill="{C.TEXT_MUTED}">SHIFT</text>'
        f'<rect x="{kb_x + 280}" y="{kb_y + 50}" width="42" height="21" rx="3" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>'
        f'<text x="{kb_x + 301}" y="{kb_y + 64}" text-anchor="middle" class="mono" font-size="9.5" fill="{C.TEXT_MUTED}">DEL</text>'
        f'<rect x="{kb_x}" y="{kb_y + 75}" width="52" height="20" rx="3" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>'
        f'<text x="{kb_x + 26}" y="{kb_y + 89}" text-anchor="middle" class="mono" font-size="9.5" fill="{C.TEXT_MUTED}">?123</text>'
        f'<rect x="{kb_x + 58}" y="{kb_y + 75}" width="196" height="20" rx="3" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_MUTED}" stroke-width="1"/>'
        f'<text x="{kb_x + 156}" y="{kb_y + 89}" text-anchor="middle" class="mono" font-size="10.5" font-weight="700" fill="{C.TEXT_PRIMARY}" letter-spacing="2">GNOSIS</text>'
        f'<rect x="{kb_x + 260}" y="{kb_y + 75}" width="62" height="20" rx="3" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>'
        f'<text x="{kb_x + 291}" y="{kb_y + 89}" text-anchor="middle" class="mono" font-size="9.5" fill="{C.TEXT_SECONDARY}">ENTER</text>'
    )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Current Project: Gnosis Keyboard (In Progress)">
  <title>Current Projects — {escape(C.PROJECT_NAME)} (Mobile)</title>
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
  </style>

  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <rect x="1.5" y="1.5" width="{w - 3}" height="34" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="36" x2="{w - 1}" y2="36" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="16" y="23" class="mono" font-size="13.5" font-weight="700" fill="{C.TEXT_PRIMARY}">// Current Projects</text>
  <text x="{w - 16}" y="23" text-anchor="end" class="mono" font-size="12" fill="{C.TEXT_MUTED}">repo: {escape(C.PROJECT_REPO_NAME)}</text>

  <!-- Project Title & Status Badge -->
  <text x="18" y="68" class="sans" font-size="21" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(C.PROJECT_NAME)}</text>
  <rect x="242" y="48" width="122" height="27" rx="5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.1"/>
  <circle cx="256" cy="61.5" r="3.8" fill="{C.TEXT_PRIMARY}" class="pulse-dot"/>
  <text x="268" y="66" class="mono" font-size="12.5" font-weight="600" fill="{C.TEXT_PRIMARY}">{escape(C.PROJECT_STATUS)}</text>

  <!-- 3-Line Description for Mobile -->
  <text x="18" y="98" class="sans" font-size="14.5" fill="{C.TEXT_SECONDARY}">A custom Android keyboard focused on</text>
  <text x="18" y="120" class="sans" font-size="14.5" fill="{C.TEXT_SECONDARY}">control, customization, and a better</text>
  <text x="18" y="142" class="sans" font-size="14.5" fill="{C.TEXT_SECONDARY}">typing experience.</text>

  <!-- Status Bar -->
  <rect x="16" y="156" width="348" height="32" rx="5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.1"/>
  <text x="28" y="177" class="mono" font-size="12.5" fill="{C.TEXT_SECONDARY}">stage: active dev</text>
  <text x="172" y="177" class="mono" font-size="12.5" fill="{C.TEXT_MUTED}">|</text>
  <text x="186" y="177" class="mono" font-size="12.5" font-weight="600" fill="{C.TEXT_PRIMARY}">repo: {escape(C.PROJECT_REPO_NAME)}</text>

  <!-- Full-Width Mobile Keyboard -->
  <rect x="16" y="204" width="348" height="114" rx="7" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>
  {"".join(keys_svg)}
</svg>
'''


def build_skills_learning() -> str:
    """
    Builds assets/mobile/skills-learning.svg (380x644):
    1-Column x 8-Row full-width stack (348px wide cards inside 380px viewBox)
    so every skill title, tag pill, and description renders at full 1:1 size on phones!
    """
    w, h = 380, 644
    badges: list[str] = []
    clips: list[str] = []

    col_w = 348
    row_h = 58
    gap_y = 8
    start_x = 16
    start_y = 104

    for idx, (title, desc, tag) in enumerate(C.LEARNING_ITEMS):
        by = start_y + idx * (row_h + gap_y)
        clips.append(
            f'<clipPath id="mskClip{idx}">'
            f'<rect x="2" y="2" width="{col_w - 4}" height="{row_h - 4}" rx="5"/>'
            f'</clipPath>'
        )
        badges.append(
            f'<g transform="translate({start_x}, {by})">'
            f'<rect x="0" y="0" width="{col_w}" height="{row_h}" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>'
            f'<g clip-path="url(#mskClip{idx})">'
            f'<text x="14" y="24" class="mono" font-size="14.5" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(title)}</text>'
            f'<rect x="{col_w - 92}" y="7" width="80" height="22" rx="4" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1"/>'
            f'<text x="{col_w - 52}" y="22" text-anchor="middle" class="mono" font-size="12" fill="{C.TEXT_SECONDARY}">{escape(tag)}</text>'
            f'<text x="14" y="46" class="sans" font-size="13.5" fill="{C.TEXT_SECONDARY}">{escape(desc)}</text>'
            f'</g>'
            f'</g>'
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Skills and Tools — Beginner, Learning in Progress">
  <title>{escape(C.SKILLS_HEADING)} — {escape(C.SKILLS_LABEL)} (Mobile)</title>
  <defs>{"".join(clips)}</defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
  </style>

  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <!-- Top Header Strip -->
  <rect x="1.5" y="1.5" width="{w - 3}" height="36" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="38" x2="{w - 1}" y2="38" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="16" y="24" class="mono" font-size="14" font-weight="700" fill="{C.TEXT_PRIMARY}">// {escape(C.SKILLS_HEADING)}</text>
  <text x="{w - 16}" y="24" text-anchor="end" class="mono" font-size="11.5" fill="{C.TEXT_SECONDARY}">status: beginner</text>

  <!-- Beginner — Learning in Progress Full-Width Pill -->
  <rect x="16" y="48" width="348" height="26" rx="4" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="190" y="65" text-anchor="middle" class="mono" font-size="12.5" font-weight="600" fill="{C.TEXT_PRIMARY}">{escape(C.SKILLS_LABEL)}</text>

  <!-- Core Message -->
  <text x="16" y="93" class="sans" font-size="13.5" font-weight="600" fill="{C.TEXT_SECONDARY}">&#8220;{escape(C.SKILLS_MESSAGE)}&#8221;</text>

  <!-- 8 Single-Column Full-Width Cards -->
  {"".join(badges)}
</svg>
'''


def build_terminal_session() -> str:
    """
    Builds assets/mobile/terminal-session.svg (380x396):
    Native 380px width stacked Scene A (terminal) + Scene B (sleepy mascot at laptop).
    """
    w, h = 380, 396

    clips: list[str] = []
    texts: list[str] = []
    line_timings = [(4, 14), (18, 28), (33, 44), (49, 58), (63, 75)]

    for idx, ((kind, txt), (_t_start, _t_end)) in enumerate(zip(C.TERMINAL_SCENE_A_LINES, line_timings)):
        y = 68 + idx * 28
        col = C.TEXT_PRIMARY if kind == "cmd" else (C.TERM_ERROR if kind == "err" else C.TEXT_SECONDARY)
        fweight = ' font-weight="700"' if kind == "cmd" else ""
        clips.append(
            f'<clipPath id="mtsClip{idx}">'
            f'<rect x="16" y="{y - 18}" width="348" height="24" class="mtline{idx}"/>'
            f'</clipPath>'
        )
        texts.append(
            f'<text x="20" y="{y}" clip-path="url(#mtsClip{idx})" class="mono" font-size="14.5"{fweight} fill="{col}">{escape(txt)}</text>'
        )

    line_css = [
        f".mtline{idx} {{ animation: mtypeL{idx} 12s steps(32, end) infinite; }}\n"
        f"    @keyframes mtypeL{idx} {{\n"
        f"      0%, {t_start}% {{ width: 0px; }}\n"
        f"      {t_end}%, 92% {{ width: 348px; }}\n"
        f"      96%, 100% {{ width: 0px; }}\n"
        f"    }}"
        for idx, (t_start, t_end) in enumerate(line_timings)
    ]

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Terminal Session Scenes A and B">
  <title>Terminal Session — Running Out of Ideas (Mobile)</title>
  <defs>{"".join(clips)}</defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    {chr(10).join(line_css)}
    .thought-bubble {{ animation: bubbleShow 12s ease-in-out infinite; }}
    @keyframes bubbleShow {{
      0%, 54% {{ opacity: 0; transform: translateY(4px); }}
      60%, 92% {{ opacity: 1; transform: translateY(0px); }}
      96%, 100% {{ opacity: 0; transform: translateY(4px); }}
    }}
    .mascot-nod {{ animation: headNod 4s ease-in-out infinite; }}
    @keyframes headNod {{ 0%, 100% {{ transform: translateY(0px); }} 50% {{ transform: translateY(2px); }} }}
    .cur {{ animation: cBlink 1s steps(2, start) infinite; }}
    @keyframes cBlink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .mtline0, .mtline1, .mtline2, .mtline3, .mtline4 {{ animation: none !important; width: 348px !important; }}
      .thought-bubble {{ animation: none !important; opacity: 1 !important; }}
    }}
  </style>

  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <rect x="1.5" y="1.5" width="{w - 3}" height="34" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="36" x2="{w - 1}" y2="36" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="16" y="23" class="mono" font-size="13" font-weight="700" fill="{C.TEXT_PRIMARY}">// Development Log &amp; Story</text>
  <text x="{w - 16}" y="23" text-anchor="end" class="mono" font-size="11.5" fill="{C.TEXT_SECONDARY}">scene 01</text>

  {"".join(texts)}

  <text x="20" y="206" class="mono" font-size="14.5" fill="{C.TEXT_MUTED}">$ </text>
  <rect x="38" y="193" width="8" height="15" fill="{C.TEXT_PRIMARY}" class="cur"/>

  <line x1="16" y1="220" x2="364" y2="220" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Scene B: Mascot at Laptop -->
  <rect x="16" y="230" width="348" height="150" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>
  <line x1="32" y1="346" x2="348" y2="346" stroke="{C.BORDER}" stroke-width="1.5"/>

  <rect x="52" y="326" width="18" height="20" rx="2" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_MUTED}" stroke-width="1.2"/>
  <path d="M 70 330 C 75 330, 75 342, 70 342" fill="none" stroke="{C.TEXT_MUTED}" stroke-width="1.2"/>

  <g class="mascot-nod">
    <rect x="150" y="304" width="48" height="42" rx="8" fill="#222222" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
    <circle cx="174" cy="274" r="26" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
    <path d="M 147 274 C 147 240, 201 240, 201 274 C 195 260, 184 264, 176 270 L 170 260 L 162 270 L 154 262 Z" fill="#1A1A1A"/>
    <line x1="162" y1="278" x2="170" y2="278" stroke="{C.BG_PRIMARY}" stroke-width="2.4" stroke-linecap="round"/>
    <line x1="178" y1="278" x2="186" y2="278" stroke="{C.BG_PRIMARY}" stroke-width="2.4" stroke-linecap="round"/>
  </g>

  <polygon points="114,308 168,308 176,344 122,344" fill="#141414" stroke="{C.TEXT_SECONDARY}" stroke-width="1.3"/>
  <rect x="118" y="342" width="76" height="4" rx="1.5" fill="{C.TEXT_SECONDARY}"/>

  <g class="thought-bubble">
    <circle cx="208" cy="260" r="3" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
    <circle cx="218" cy="252" r="4.5" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
    <rect x="226" y="238" width="128" height="36" rx="6" fill="{C.BG_PRIMARY}" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
    <text x="290" y="261" text-anchor="middle" class="mono" font-size="14" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(C.MASCOT_THOUGHT_BUBBLE)}</text>
  </g>

  <text x="190" y="368" text-anchor="middle" class="mono" font-size="12.5" fill="{C.TEXT_MUTED}">status: staring at blank editor</text>
</svg>
'''


def build_ai_assistance() -> str:
    """
    Builds assets/mobile/ai-assistance.svg (380x496):
    Native 380px width 1-column stack:
    - 3 full-width AI service rows (348px wide each) with integrated popup pills on the right
    - Full-width terminal response box
    - Focused mascot at laptop
    """
    w, h = 380, 496

    rows_svg: list[str] = []
    for idx, ((name, _sub), ptext) in enumerate(zip(C.AI_SERVICES, C.AI_POPUPS)):
        ry = 48 + idx * 58
        if idx == 0:
            icon = f'<path d="M 38 {ry+16} V {ry+34} M 29 {ry+25} H 47 M 31 {ry+18} L 45 {ry+32} M 45 {ry+18} L 31 {ry+32}" stroke="{C.TEXT_PRIMARY}" stroke-width="1.6"/>'
        elif idx == 1:
            icon = f'<polygon points="38,{ry+15} 41.5,{ry+22} 49,{ry+25} 41.5,{ry+28} 38,{ry+35} 34.5,{ry+28} 27,{ry+25} 34.5,{ry+22}" fill="none" stroke="{C.TEXT_PRIMARY}" stroke-width="1.5"/>'
        else:
            icon = f'<polygon points="38,{ry+16} 46,{ry+20.5} 46,{ry+29.5} 38,{ry+34} 30,{ry+29.5} 30,{ry+20.5}" fill="none" stroke="{C.TEXT_PRIMARY}" stroke-width="1.5"/>'

        rows_svg.append(
            f'<g>'
            f'<rect x="16" y="{ry}" width="348" height="50" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>'
            f'{icon}'
            f'<text x="58" y="{ry + 30}" class="sans" font-size="14.5" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(name)}</text>'
            f'<g class="pop{idx}">'
            f'<rect x="192" y="{ry + 10}" width="162" height="30" rx="4" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_SECONDARY}" stroke-width="1" stroke-dasharray="3 2"/>'
            f'<text x="273" y="{ry + 29}" text-anchor="middle" class="mono" font-size="12" font-weight="600" fill="{C.TEXT_PRIMARY}">{escape(ptext)}</text>'
            f'</g>'
            f'</g>'
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Asking AI for Help and Implementing Solution">
  <title>Terminal Session — Asking AI for Help (Mobile)</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    .pop0 {{ animation: popSeq0 12s ease-in-out infinite; }}
    .pop1 {{ animation: popSeq1 12s ease-in-out infinite; }}
    .pop2 {{ animation: popSeq2 12s ease-in-out infinite; }}
    @keyframes popSeq0 {{ 0%, 5% {{ opacity: 0.25; }} 10%, 34% {{ opacity: 1; }} 40%, 100% {{ opacity: 0.35; }} }}
    @keyframes popSeq1 {{ 0%, 22% {{ opacity: 0.25; }} 28%, 54% {{ opacity: 1; }} 60%, 100% {{ opacity: 0.35; }} }}
    @keyframes popSeq2 {{ 0%, 40% {{ opacity: 0.25; }} 46%, 76% {{ opacity: 1; }} 82%, 100% {{ opacity: 0.35; }} }}
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

  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <rect x="1.5" y="1.5" width="{w - 3}" height="34" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="36" x2="{w - 1}" y2="36" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="16" y="23" class="mono" font-size="13" font-weight="700" fill="{C.TEXT_PRIMARY}">// Development Log &amp; Story</text>
  <text x="{w - 16}" y="23" text-anchor="end" class="mono" font-size="11.5" fill="{C.TEXT_SECONDARY}">scene 02 // AI hint</text>

  <!-- 3 Stacked Full-Width AI Service Cards -->
  {"".join(rows_svg)}

  <!-- Terminal Assistance Output -->
  <rect x="16" y="226" width="348" height="102" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>
  <text x="30" y="254" class="mono resp0" font-size="14.5" font-weight="700" fill="{C.TERM_SUCCESS}">&gt; hint received</text>
  <text x="30" y="282" class="mono resp1" font-size="14.5" fill="{C.TEXT_PRIMARY}">&gt; trying to understand...</text>
  <text x="30" y="310" class="mono resp2" font-size="14.5" fill="{C.TEXT_SECONDARY}">&gt; implementing solution...</text>

  <!-- Focused Mascot Scene -->
  <rect x="16" y="340" width="348" height="140" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>
  <line x1="32" y1="448" x2="348" y2="448" stroke="{C.BORDER}" stroke-width="1.5"/>

  <g transform="translate(114, 392)">
    <rect x="-22" y="20" width="44" height="36" rx="7" fill="#242424" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
    <circle cx="0" cy="-6" r="24" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
    <path d="M -24 -6 C -24 -36, 24 -36, 24 -6 C 18 -18, 8 -14, 2 -8 L -4 -18 L -11 -8 L -18 -16 Z" fill="#1A1A1A"/>
    <line x1="-11" y1="-5" x2="-4" y2="-3" stroke="{C.BG_PRIMARY}" stroke-width="2" stroke-linecap="round"/>
    <line x1="4" y1="-3" x2="11" y2="-5" stroke="{C.BG_PRIMARY}" stroke-width="2" stroke-linecap="round"/>
    <circle cx="-7" cy="0" r="2" fill="{C.BG_PRIMARY}"/>
    <circle cx="7" cy="0" r="2" fill="{C.BG_PRIMARY}"/>
  </g>

  <polygon points="56,414 106,414 114,446 64,446" fill="#161616" stroke="{C.TEXT_PRIMARY}" stroke-width="1.3"/>
  <rect x="60" y="444" width="70" height="4" rx="1.5" fill="{C.TEXT_SECONDARY}"/>

  <rect x="158" y="378" width="194" height="34" rx="5" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1.1" class="focus-badge"/>
  <text x="255" y="400" text-anchor="middle" class="mono focus-badge" font-size="12.5" font-weight="600" fill="{C.TEXT_PRIMARY}">focus: reading docs...</text>

  <text x="190" y="468" text-anchor="middle" class="mono" font-size="12.5" fill="{C.TEXT_MUTED}">status: actually making sense now</text>
</svg>
'''


def build_error_repair() -> str:
    """
    Builds assets/mobile/error-repair.svg (380x420):
    Native 380px width stacked error terminal + AI Construction Truck lane.
    """
    w, h = 380, 420
    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Simulated Error &amp; Repair">
  <title>Simulated Error &amp; Repair (Mobile)</title>
  <defs>
    <clipPath id="mTruckClip">
      <rect x="16" y="236" width="348" height="168" rx="6"/>
    </clipPath>
  </defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .err-line {{ animation: showErr 14s linear infinite; }}
    @keyframes showErr {{ 0%, 4% {{ opacity: 0; }} 6%, 92% {{ opacity: 1; }} 97%, 100% {{ opacity: 0; }} }}
    .req-line {{ animation: showReq 14s linear infinite; }}
    @keyframes showReq {{ 0%, 16% {{ opacity: 0; }} 20%, 92% {{ opacity: 1; }} 97%, 100% {{ opacity: 0; }} }}
    .fix-line {{ animation: showFix 14s linear infinite; }}
    @keyframes showFix {{ 0%, 46% {{ opacity: 0; }} 50%, 92% {{ opacity: 1; }} 97%, 100% {{ opacity: 0; }} }}
    .ok-line {{ animation: showOk 14s linear infinite; }}
    @keyframes showOk {{ 0%, 68% {{ opacity: 0; }} 72%, 92% {{ opacity: 1; }} 97%, 100% {{ opacity: 0; }} }}
    .prog-fill {{ animation: progBar 14s ease-in-out infinite; }}
    @keyframes progBar {{
      0%, 46% {{ width: 0px; fill: {C.TEXT_MUTED}; }}
      68% {{ width: 230px; fill: {C.TEXT_PRIMARY}; }}
      72%, 92% {{ width: 230px; fill: {C.TERM_SUCCESS}; }}
      97%, 100% {{ width: 0px; }}
    }}
    .truck-rig {{ animation: truckDrive 14s ease-in-out infinite; }}
    @keyframes truckDrive {{
      0%, 20% {{ transform: translateX(200px); opacity: 0; }}
      24% {{ opacity: 1; }}
      36%, 74% {{ transform: translateX(0px); opacity: 1; }}
      88% {{ transform: translateX(-220px); opacity: 1; }}
      92%, 100% {{ transform: translateX(-240px); opacity: 0; }}
    }}
    .worker-fix {{ animation: workerAct 14s linear infinite; }}
    @keyframes workerAct {{ 0%, 36% {{ opacity: 0; }} 40%, 68% {{ opacity: 1; }} 72%, 100% {{ opacity: 0; }} }}
    .warn-badge {{ animation: warnState 14s linear infinite; }}
    @keyframes warnState {{ 0%, 5% {{ opacity: 0; }} 8%, 68% {{ opacity: 1; }} 72%, 100% {{ opacity: 0; }} }}
    .fixed-badge {{ animation: showOk 14s linear infinite; }}
    @media (prefers-reduced-motion: reduce) {{
      .err-line, .req-line, .fix-line, .ok-line, .fixed-badge, .truck-rig, .worker-fix {{ animation: none !important; opacity: 1 !important; transform: none !important; }}
      .warn-badge {{ display: none !important; }}
      .prog-fill {{ animation: none !important; width: 230px !important; fill: {C.TERM_SUCCESS} !important; }}
    }}
  </style>

  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <rect x="1.5" y="1.5" width="{w - 3}" height="34" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="36" x2="{w - 1}" y2="36" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="16" y="23" class="mono" font-size="13.5" font-weight="700" fill="{C.TEXT_PRIMARY}">// Simulated Error &amp; Repair</text>
  <text x="{w - 16}" y="23" text-anchor="end" class="mono" font-size="11.5" fill="{C.TEXT_SECONDARY}">debug-sim</text>

  <text x="20" y="66" class="mono err-line" font-size="14.5" font-weight="700" fill="{C.TERM_ERROR}">! error: something went wrong</text>
  <text x="20" y="94" class="mono err-line" font-size="14" fill="{C.TEXT_SECONDARY}">&gt; diagnosis: developer confusion</text>
  <text x="20" y="122" class="mono req-line" font-size="14" fill="{C.TEXT_SECONDARY}">&gt; requesting assistance...</text>
  <text x="20" y="150" class="mono fix-line" font-size="14" fill="{C.TEXT_PRIMARY}">&gt; applying fix...</text>

  <g class="fix-line">
    <rect x="20" y="164" width="230" height="13" rx="3.5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
    <rect x="20" y="164" width="230" height="13" rx="3.5" fill="{C.TERM_SUCCESS}" class="prog-fill"/>
    <text x="260" y="175" class="mono" font-size="12" fill="{C.TEXT_MUTED}">repair_job</text>
  </g>

  <text x="20" y="206" class="mono ok-line" font-size="14" font-weight="700" fill="{C.TERM_SUCCESS}">&#10003; build successful (simulated)</text>

  <line x1="16" y1="224" x2="364" y2="224" stroke="{C.BORDER}" stroke-width="1"/>

  <rect x="16" y="236" width="348" height="168" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>

  <g clip-path="url(#mTruckClip)">
    <g transform="translate(54, 298)">
      <circle cx="0" cy="0" r="20" fill="#E5E5E5" stroke="{C.BORDER}" stroke-width="1.2"/>
      <path d="M -20 0 C -20 -26, 20 -26, 20 0 C 14 -10, 4 -8, -2 -4 L -8 -12 L -14 -4 Z" fill="#1A1A1A"/>
      <line x1="-9" y1="2" x2="-3" y2="2" stroke="{C.BG_PRIMARY}" stroke-width="2"/>
      <line x1="3" y1="2" x2="9" y2="2" stroke="{C.BG_PRIMARY}" stroke-width="2"/>
      <text x="24" y="-6" class="mono warn-badge" font-size="14" font-weight="700" fill="{C.TEXT_SECONDARY}">?</text>
    </g>

    <g class="warn-badge">
      <rect x="104" y="290" width="66" height="44" rx="4" fill="#140C0C" stroke="{C.TERM_ERROR}" stroke-width="1.3"/>
      <polygon points="137,298 127,316 147,316" fill="none" stroke="{C.TERM_WARN}" stroke-width="1.4"/>
      <text x="137" y="314" text-anchor="middle" class="mono" font-size="10" font-weight="700" fill="{C.TERM_WARN}">!</text>
      <text x="137" y="328" text-anchor="middle" class="mono" font-size="9.5" font-weight="600" fill="{C.TERM_ERROR}">ERR_01</text>
    </g>

    <g class="fixed-badge">
      <rect x="104" y="290" width="66" height="44" rx="4" fill="#0B140E" stroke="{C.TERM_SUCCESS}" stroke-width="1.3"/>
      <text x="137" y="313" text-anchor="middle" class="mono" font-size="14" font-weight="700" fill="{C.TERM_SUCCESS}">&#10003;</text>
      <text x="137" y="327" text-anchor="middle" class="mono" font-size="9.5" font-weight="700" fill="{C.TERM_SUCCESS}">FIXED</text>
    </g>

    <g class="worker-fix">
      <rect x="180" y="338" width="12" height="18" rx="2" fill="#2A2A2A" stroke="{C.TEXT_SECONDARY}" stroke-width="1"/>
      <circle cx="186" cy="331" r="6" fill="#E5E5E5"/>
      <path d="M 178 330 C 178 323, 194 323, 194 330 Z" fill="{C.TERM_WARN}"/>
      <line x1="182" y1="340" x2="170" y2="324" stroke="{C.TEXT_PRIMARY}" stroke-width="2.2" stroke-linecap="round"/>
      <text x="172" y="318" class="mono" font-size="11" fill="{C.TERM_WARN}">*</text>
    </g>

    <g class="truck-rig">
      <rect x="234" y="294" width="114" height="32" rx="3" fill="{C.BG_PRIMARY}" stroke="{C.TERM_WARN}" stroke-width="1.3"/>
      <text x="291" y="314" text-anchor="middle" class="mono" font-size="12" font-weight="700" fill="{C.TEXT_PRIMARY}">[ AI ASSIST ]</text>
      <rect x="228" y="326" width="122" height="24" rx="2" fill="#1C1C1C" stroke="{C.TEXT_SECONDARY}" stroke-width="1.2"/>
      <polygon points="198,328 210,308 228,308 228,350 198,350" fill="#262626" stroke="{C.TEXT_PRIMARY}" stroke-width="1.2"/>
      <rect x="214" y="302" width="8" height="5" rx="1.5" fill="{C.TERM_WARN}"/>
      <circle cx="214" cy="352" r="9" fill="#0A0A0A" stroke="{C.TEXT_SECONDARY}" stroke-width="2"/>
      <circle cx="264" cy="352" r="9" fill="#0A0A0A" stroke="{C.TEXT_SECONDARY}" stroke-width="2"/>
      <circle cx="324" cy="352" r="9" fill="#0A0A0A" stroke="{C.TEXT_SECONDARY}" stroke-width="2"/>
    </g>

    <line x1="26" y1="362" x2="354" y2="362" stroke="{C.BORDER}" stroke-width="1.5" stroke-dasharray="6 4"/>
    <text x="190" y="388" text-anchor="middle" class="mono" font-size="12" fill="{C.TEXT_MUTED}">lane: emergency_patch_unit.exe</text>
  </g>
</svg>
'''


def build_knowledge_panel() -> str:
    """
    Builds assets/mobile/knowledge-panel.svg (380x424):
    Native 380px width 1-column stack of directory cards + archive extraction card.
    """
    w, h = 380, 424
    dir_cards: list[str] = []
    for idx, (dname, ddesc, _path) in enumerate(C.KNOWLEDGE_DIRS):
        ry = 50 + idx * 58
        dir_cards.append(
            f'<g transform="translate(16, {ry})">'
            f'<rect x="0" y="0" width="348" height="50" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.1"/>'
            f'<rect x="14" y="11" width="14" height="11" rx="1.5" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_SECONDARY}" stroke-width="1.1"/>'
            f'<text x="36" y="21" class="mono" font-size="14" font-weight="700" fill="{C.TEXT_PRIMARY}">{escape(dname)}</text>'
            f'<text x="14" y="41" class="sans" font-size="13" fill="{C.TEXT_SECONDARY}">{escape(ddesc)}</text>'
            f'</g>'
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Knowledge Base">
  <title>{escape(C.KNOWLEDGE_TITLE)} (Mobile)</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    .zip-bar {{ animation: zipLoad 8s ease-in-out infinite; }}
    @keyframes zipLoad {{ 0%, 10% {{ width: 24px; }} 55%, 88% {{ width: 312px; }} 96%, 100% {{ width: 24px; }} }}
    .zip-step2 {{ animation: zStep2 8s linear infinite; }}
    @keyframes zStep2 {{ 0%, 40% {{ opacity: 0.25; }} 50%, 90% {{ opacity: 1; }} 96%, 100% {{ opacity: 0.25; }} }}
  </style>

  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <rect x="1.5" y="1.5" width="{w - 3}" height="34" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="36" x2="{w - 1}" y2="36" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="16" y="23" class="mono" font-size="14" font-weight="700" fill="{C.TEXT_PRIMARY}">// {escape(C.KNOWLEDGE_TITLE)}</text>
  <text x="{w - 16}" y="23" text-anchor="end" class="mono" font-size="12" fill="{C.TEXT_MUTED}">~/knowledge-base/</text>

  {"".join(dir_cards)}

  <!-- Bottom Archive Extraction Card -->
  <rect x="16" y="288" width="348" height="120" rx="6" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.2"/>
  <g transform="translate(32, 302)">
    <rect x="0" y="0" width="28" height="34" rx="3" fill="{C.BG_ELEVATED}" stroke="{C.TEXT_PRIMARY}" stroke-width="1.2"/>
    <line x1="14" y1="2" x2="14" y2="22" stroke="{C.TEXT_SECONDARY}" stroke-width="3" stroke-dasharray="2 2"/>
    <rect x="10" y="22" width="8" height="6" fill="{C.TEXT_PRIMARY}"/>
  </g>
  <text x="72" y="317" class="mono" font-size="14.5" font-weight="700" fill="{C.TEXT_PRIMARY}">notes-archive.zip</text>
  <text x="72" y="334" class="mono" font-size="12" fill="{C.TEXT_MUTED}">[concept preview]</text>

  <rect x="32" y="348" width="316" height="11" rx="3.5" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <rect x="32" y="348" width="260" height="11" rx="3.5" fill="{C.TEXT_PRIMARY}" class="zip-bar"/>

  <text x="32" y="382" class="mono" font-size="13" fill="{C.TEXT_SECONDARY}">&gt; extracting knowledge...</text>
  <text x="32" y="400" class="mono zip-step2" font-size="13" font-weight="700" fill="{C.TEXT_PRIMARY}">&gt; still learning...</text>
</svg>
'''


def build_funny_quote() -> str:
    """
    Builds assets/mobile/funny-quote.svg (380x348):
    Native 380px width stacked layout:
    Top: Centered 128x128 confused mascot + hand-drawn ? marks.
    Bottom: Full-width speech bubble with 15.5px bold verbatim quote.
    """
    w, h = 380, 348
    confused_b64 = C.get_asset_base64("confused-mascot.jpg")
    mascot_img_tag = ""
    if confused_b64:
        mascot_img_tag = (
            f'<image href="data:image/jpeg;base64,{confused_b64}" '
            f'x="126" y="48" width="128" height="128" preserveAspectRatio="xMidYMid slice" '
            f'clip-path="url(#mConfusedClip)"/>'
        )

    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Trying to Understand: When I say Ehh, ehhh, ehhhh... like for three time, don't give up on me bro, I'm trying to understand it for real.">
  <title>Trying to Understand (Mobile)</title>
  <defs>
    <clipPath id="mConfusedClip">
      <rect x="126" y="48" width="128" height="128" rx="8"/>
    </clipPath>
  </defs>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    .head-tilt {{ animation: tilt 5s ease-in-out infinite; transform-origin: 190px 112px; }}
    @keyframes tilt {{ 0%, 100% {{ transform: rotate(0deg); }} 50% {{ transform: rotate(-2.2deg); }} }}
  </style>

  <rect x="0" y="0" width="{w}" height="{h}" rx="8" fill="{C.BG_PRIMARY}"/>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1.2"/>

  <rect x="1.5" y="1.5" width="{w - 3}" height="34" rx="6" fill="{C.BG_SECONDARY}"/>
  <line x1="1" y1="36" x2="{w - 1}" y2="36" stroke="{C.BORDER}" stroke-width="1"/>
  <text x="16" y="23" class="mono" font-size="14" font-weight="700" fill="{C.TEXT_PRIMARY}">// Trying to Understand</text>

  <!-- Centered Confused Mascot -->
  <g class="head-tilt">
    <rect x="125" y="47" width="130" height="130" rx="9" fill="{C.BG_PRIMARY}" stroke="{C.BORDER}" stroke-width="1.2"/>
    {mascot_img_tag}
  </g>

  <!-- Question Marks Around Mascot -->
  <g fill="none" stroke="{C.TEXT_PRIMARY}" stroke-width="2" stroke-linecap="round">
    <path d="M 98 62 C 98 52, 112 52, 112 62 C 112 68, 105 69, 105 75"/>
    <circle cx="105" cy="82" r="1.5" fill="{C.TEXT_PRIMARY}"/>
    <path d="M 268 58 C 268 48, 282 48, 282 58 C 282 64, 275 65, 275 71"/>
    <circle cx="275" cy="78" r="1.5" fill="{C.TEXT_PRIMARY}"/>
  </g>

  <!-- Full-Width Speech Bubble Below Mascot -->
  <path d="M 24 196 H 178 L 190 182 L 202 196 H 356 A 8 8 0 0 1 364 204 V 324 A 8 8 0 0 1 356 332 H 24 A 8 8 0 0 1 16 324 V 204 A 8 8 0 0 1 24 196 Z"
        fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1.3"/>

  <text x="190" y="230" text-anchor="middle" class="sans" font-size="15.5" font-weight="700" fill="{C.TEXT_PRIMARY}">
    &#8220;When I say Ehh, ehhh, ehhhh...
  </text>
  <text x="190" y="256" text-anchor="middle" class="sans" font-size="15.5" font-weight="700" fill="{C.TEXT_PRIMARY}">
    like for three time, don&apos;t give up on me
  </text>
  <text x="190" y="282" text-anchor="middle" class="sans" font-size="15.5" font-weight="700" fill="{C.TEXT_PRIMARY}">
    bro, I&apos;m trying to understand it for real.&#8221;
  </text>
  <text x="190" y="314" text-anchor="middle" class="mono" font-size="11.5" fill="{C.TEXT_MUTED}">
    // reading documentation at 3 AM
  </text>
</svg>
'''


def build_footer() -> str:
    """
    Builds assets/mobile/footer.svg (380x168):
    Native 380px width closing section for mobile.
    """
    w, h = 380, 168
    emblem = C.render_brand_emblem_svg(cx=w / 2.0, top_y=16.0, scale=0.54)
    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="SLYTNX Footer">
  <title>SLYTNX Footer (Mobile)</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .sans {{ font-family: {C.FONT_SANS}; }}
    .cur {{ animation: blink 1.2s steps(1) infinite; }}
    @keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
  </style>
  <rect x="0" y="0" width="{w}" height="{h}" rx="7" fill="{C.BG_PRIMARY}"/>
  <line x1="16" y1="2" x2="{w - 16}" y2="2" stroke="{C.BORDER}" stroke-width="1.2"/>

  {emblem}

  <text x="{w / 2:.0f}" y="84" text-anchor="middle" class="mono" font-size="17" font-weight="700" fill="{C.TEXT_PRIMARY}" letter-spacing="4">{escape(C.FOOTER_WORDMARK)}</text>
  <text x="{w / 2:.0f}" y="108" text-anchor="middle" class="mono" font-size="14" fill="{C.TEXT_SECONDARY}" letter-spacing="1.5">{escape(C.FOOTER_TAGLINE)}</text>
  <text x="{w / 2:.0f}" y="132" text-anchor="middle" class="sans" font-size="14.5" font-weight="600" fill="{C.TEXT_PRIMARY}">{escape(C.FOOTER_THANKS)}</text>
  <text x="{w / 2 - 6:.0f}" y="154" text-anchor="middle" class="mono" font-size="13" fill="{C.TEXT_MUTED}">{escape(C.FOOTER_STATUS)}</text>
  <rect x="{w / 2 + 52:.0f}" y="142" width="7" height="13" fill="{C.TEXT_MUTED}" class="cur"/>
</svg>
'''


def build_unified_terminal() -> str:
    """
    Combines Skills / Tools, Development Log & Story (Scenes 1 & 2),
    Simulated Error & Repair, Knowledge Base, and Trying to Understand
    one after another inside a single mobile terminal (380px wide).
    """
    return C.combine_into_single_terminal(
        [
            build_skills_learning(),
            build_terminal_session(),
            build_ai_assistance(),
            build_error_repair(),
            build_knowledge_panel(),
            build_funny_quote(),
        ],
        w=380,
        header_title="sltynx@sleeping-core: ~/workspace",
        header_right="[unified]",
    )


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
        "mobile/unified-terminal.svg": build_unified_terminal(),
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
