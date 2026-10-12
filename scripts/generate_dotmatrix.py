#!/usr/bin/env python3
"""
Generates assets/dotmatrix-name.svg:
Deterministic square-dot-matrix name simulator for SLYTNX (Section 6).
"""
from __future__ import annotations
import pathlib

import config as C


def build_dotmatrix_name() -> str:
    """
    Builds assets/dotmatrix-name.svg (880x235):
    Animation sequence (11s cycle):
      1. Sparse square-dot grid appears on a pure #000000 background (0.0s - 0.8s).
      2. Individual dots illuminate in a controlled sequence across columns (0.8s - 2.2s).
      3. Dots activate to construct each letter of SLYTNX (1.2s - 3.0s).
      4. The triangular emblem forms above the wordmark (2.4s - 3.6s).
      5. Completed logo stays clearly readable for >5.5 seconds (3.6s - 9.4s).
      6. A subtle horizontal scan sweeps across the completed logo (5.4s - 6.8s).
      7. Pauses before resetting cleanly (9.4s - 11.0s).
    """
    w, h = 880, 286

    dot_size = 5.2
    pitch = 7.6

    # Wordmark geometry: 6 letters, each 9 cols wide, 3 cols gap between letters
    # Total cols for wordmark = 6 * 9 + 5 * 3 = 54 + 15 = 69 cols
    # Total width = 69 * 7.6 = 524.4px -> start_x = (880 - 524.4) / 2 = 177.8
    total_cols = 69
    word_start_x = (w - (total_cols * pitch)) / 2.0
    word_start_y = 144.0

    # Background sparse matrix grid (every 2nd cell in the display window so SVG stays fast & crisp)
    bg_rects: list[str] = []
    for r in range(-12, 16, 2):
        gy = word_start_y + r * pitch
        if gy < 46 or gy > h - 34:
            continue
        for c in range(-4, total_cols + 4, 2):
            gx = word_start_x + c * pitch
            if gx < 32 or gx > w - 36:
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
    emb_rows = len(C.DOT_EMBLEM)
    emb_cols = len(C.DOT_EMBLEM[0])
    emb_pitch = 4.8
    emb_dot = 3.3
    emb_start_x = (w - emb_cols * emb_pitch) / 2.0
    emb_start_y = 54.0
    for r, row in enumerate(C.DOT_EMBLEM):
        for c, cell in enumerate(row):
            if cell == "#":
                ex = emb_start_x + c * emb_pitch
                ey = emb_start_y + r * emb_pitch
                emblem_dots.append(
                    f'<rect x="{ex:.1f}" y="{ey:.1f}" width="{emb_dot:.1f}" height="{emb_dot:.1f}"/>'
                )

    # Geometric wireframe overlay that locks over the emblem dots once formed
    emblem_vector = C.render_brand_emblem_svg(cx=w / 2.0, top_y=52.0, scale=0.78)

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
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="7" fill="none" stroke="{C.BORDER}" stroke-width="1"/>

  <!-- Subtle Header Metadata -->
  <text x="24" y="24" class="mono" font-size="11" fill="{C.TEXT_MUTED}">matrix://sltynx-display [69x11 square-dot array]</text>
  <text x="{w - 24}" y="24" text-anchor="end" class="mono" font-size="11" fill="{C.TEXT_MUTED}">mode: dot-convergence</text>
  <line x1="1" y1="34" x2="{w - 1}" y2="34" stroke="{C.BORDER_SUBTLE}" stroke-width="1"/>

  <!-- 1. Sparse Background Dot Field -->
  <g class="grid-bg">{"".join(bg_rects)}</g>

  <!-- 2. Emblem Dot-Matrix & Vector Lock-In Above Wordmark -->
  <g class="emblem-dots">{"".join(emblem_dots)}</g>
  <g class="emblem-vec">{emblem_vector}</g>

  <!-- 3. Active SLYTNX Dot-Matrix Wordmark Bands -->
  {"".join(band_groups)}

  <!-- 4. Subtle Horizontal Scanline Pass -->
  <rect x="165" y="46" width="18" height="202" fill="{C.TEXT_PRIMARY}" class="scan-bar"/>

  <!-- Bottom Caption -->
  <text x="{w / 2:.0f}" y="264" text-anchor="middle" class="mono" font-size="11.5" fill="{C.TEXT_SECONDARY}" letter-spacing="2">SLYTNX // SLEEPING CORE</text>
</svg>
'''


def build_monitor_top() -> str:
    """
    Builds assets/monitor-top.svg (188x22):
    Top CRT/terminal monitor header bar that sits inside <kbd> directly above the live
    visitorbadge.io PROFILE VIEWS badge.
    """
    w, h = 188, 22
    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Profile Views Monitor Header">
  <title>monitor://views</title>
  <style>
    .mono {{ font-family: {C.FONT_MONO}; }}
    .live-dot {{ animation: lPulse 2s ease-in-out infinite; }}
    @keyframes lPulse {{ 0%, 100% {{ opacity: 0.4; }} 50% {{ opacity: 1; }} }}
  </style>
  <rect x="0" y="0" width="{w}" height="{h}" rx="3" fill="{C.BG_PRIMARY}"/>
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="2.5" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="10" cy="11" r="2.6" fill="{C.TEXT_DIM}"/>
  <circle cx="19" cy="11" r="2.6" fill="{C.TEXT_DIM}"/>
  <circle cx="28" cy="11" r="2.6" fill="{C.TEXT_DIM}"/>
  <text x="38" y="14.5" class="mono" font-size="9.5" font-weight="700" fill="{C.TEXT_SECONDARY}">tty://views</text>
  <circle cx="146" cy="11" r="2.5" fill="{C.TERM_SUCCESS}" class="live-dot"/>
  <text x="178" y="14.5" text-anchor="end" class="mono" font-size="9" fill="{C.TEXT_MUTED}">LIVE</text>
</svg>
'''


def build_monitor_stand() -> str:
    """
    Builds assets/monitor-stand.svg (204x28):
    Small monitor bottom chin with power LED, neck, and desk stand base below <kbd>.
    """
    w, h = 204, 28
    cx = w / 2.0
    return f'''<svg {C.SVG_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Monitor Stand">
  <title>Monitor Stand</title>
  <style>
    .pwr-led {{ animation: pwrGlow 3s ease-in-out infinite; }}
    @keyframes pwrGlow {{ 0%, 100% {{ opacity: 0.45; }} 50% {{ opacity: 1; }} }}
  </style>
  <rect x="0" y="0" width="{w}" height="{h}" fill="{C.BG_PRIMARY}" fill-opacity="0"/>
  <!-- Monitor Chin Bezel -->
  <rect x="6" y="0" width="{w - 12}" height="7" rx="2" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <circle cx="{w - 18}" cy="3.5" r="1.8" fill="{C.TERM_SUCCESS}" class="pwr-led"/>
  <!-- Monitor Neck -->
  <polygon points="{cx - 18:.0f},7 {cx + 18:.0f},7 {cx + 24:.0f},20 {cx - 24:.0f},20" fill="{C.BG_SECONDARY}" stroke="{C.BORDER}" stroke-width="1"/>
  <line x1="{cx - 10:.0f}" y1="11" x2="{cx + 10:.0f}" y2="11" stroke="{C.BORDER_SUBTLE}" stroke-width="1"/>
  <line x1="{cx - 12:.0f}" y1="15" x2="{cx + 12:.0f}" y2="15" stroke="{C.BORDER_SUBTLE}" stroke-width="1"/>
  <!-- Monitor Base Stand -->
  <rect x="{cx - 56:.0f}" y="20" width="112" height="6" rx="3" fill="{C.BG_ELEVATED}" stroke="{C.BORDER}" stroke-width="1.1"/>
  <rect x="{cx - 36:.0f}" y="22" width="72" height="2" rx="1" fill="{C.BG_PRIMARY}"/>
</svg>
'''


def generate_all() -> dict[str, pathlib.Path]:
    C.ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    outputs = {
        "dotmatrix-name.svg": build_dotmatrix_name(),
        "monitor-top.svg": build_monitor_top(),
        "monitor-stand.svg": build_monitor_stand(),
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
